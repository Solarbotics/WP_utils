"""This field is a serialized string as defined (using the following
as example) as:
    a:2:{i:0,s:10:"plugin.php";i:1,s:17:"anotherplugin.php";}
    a:2 = 2 plugins active
    :{
        i:0 (= 0th plugin in list)
        ,
        s:10 (= name of plugin string length (10 chars))
        :
        "plugin.php"
    ;
        i:1 (= 1st plugin in list)
        ,
        s:17 (= string length)
        :
        "anotherplugin.php"
    ;)
Some help:
https://wordpress.stackexchange.com/questions/45109/how-to-make-sense-of-the-active-plugins-option-value-to-enable-and-disable-certa
"""
"""
ToDO:
- Read in the list from saved file (copied from the database field)
- Make it human-readable (I find a newline before each "a:[0-9]*.," regex does nicely)
- Select which entry to disable
- Write out the disabled entry to log file for later re-inclusion (even manually
- re-write out a fresh list, with a:xx = new total number of plugins, and each list_element having a sequential "a:xx" element followed by the remaining datafields
     This list then can be re-written to the database directly to disable the plugins in question.

Spec: Dave Hrynkiw, April 11 2020
"""
import argparse
import re
from phpserialize import serialize, unserialize
# import os
# print(os.getcwd())

# get the defaults from command line
def get_cli_arguments():
    parser = argparse.ArgumentParser(description='Wordpress wp_options manipulator')
    parser.add_argument('-i', '--input', type=argparse.FileType('r'), required=False, metavar='file', help='WP file containing wp_options',
                        default='wp_options.txt')
    parser.add_argument('-o', '--output', type=str, required=False, metavar='file',  help='WP file output file',
                        default='wp_options_new.txt')
    parser.add_argument('-l', '--list', type=str, required=False, help='Display Plugins list')
    parser.add_argument('-d', '--delete', type=str, required=False, help='Delete Plugins by number')
    return parser.parse_args()

args = get_cli_arguments()

# Process the input file
for line in args.input:
    print("Line: {}".format(line)) #Disable when done debugging

    match = re.search(r"^a:.*{(.*)",line)   # strip off the preamble "a:0{" from the datafield entry
    result = match.group(1).rstrip('; }')   # strip off the matching end "}"
    #print("Result={}".format(result))
    result = re.split('i:',result)          # break down the link by the index value (which kills the value 'i:')
    result.remove('')                       # delete the initial blank entry
    #print(result)
    result = ["i:" + s for s in result]     # add the stripped 'i:' back to the elements
    print(result)
    # for i in range(len(result)):
    #     print("Element {}={}".format(i,result[i]))
    #     plugin_name=(re.search(r'(?<=")(.*)(?=")', result[i]).group())    #.group() gets the value, span() gets the start, end of match
    #     plugin_length=(re.search(r'(?<=")(.*)(?=")', result[i]).span())
    #     plugin_length1 = plugin_length[1] - plugin_length[0]
    #     print("name={}, span={}, len={}".format(plugin_name,plugin_length, plugin_length1))


def print_plugin_list(plugin_list):
    for i,r in enumerate(plugin_list, 0):
        plugin_name=(re.search(r'(?<=")(.*)(?=")', plugin_list[i]).group())      #.group() gets the plugin values
        plugin_length=(re.search(r'(?<=")(.*)(?=")', plugin_list[i]).span())     #.span() gets start & end of match
        plugin_length1 = plugin_length[1] - plugin_length[0]                # calculate length of plugin name (needed)
        #print("name={}, span={}, len={}".format(plugin_name,plugin_length, plugin_length1))
        print("{}: {}".format(i, plugin_name))   # Print an indexed list of plugins to choose from.



