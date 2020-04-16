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

Spec: Dave Hrynkiw, April 11 2020
"""
import argparse
import re
from datetime import datetime
import os


# get the defaults from command line
def get_cli_arguments():
    parser = argparse.ArgumentParser(description='Wordpress wp_options manipulator')

    parser.add_argument('-i', '--input', type=argparse.FileType('r'), required=False, metavar='file',
                        help='WP file containing wp_options',
                        default='wp_options.txt')
    parser.add_argument('-o', '--output', type=str, required=False, metavar='file', help='WP file output file',
                        default='wp_options_new.txt')
    parser.add_argument('-l', '--list', required=False, help='Display Plugins list', action='store_true')

    subparsers = parser.add_subparsers(dest='func')
    delplugin_parser = subparsers.add_parser('del')
    delplugin_parser.add_argument('numbers', type=int, nargs='*')
    listplugin_parser = subparsers.add_parser('list')
    listplugin_parser.add_argument('vals', type=str, nargs='*')
    return parser.parse_args()


args = get_cli_arguments()
# Process the input file
for line in args.input:
    # print("Line: {}".format(line)) #Disable when done debugging

    match = re.search(r"^a:.*{(.*)", line)  # strip off the preamble "a:0{" from the datafield entry
    result = match.group(1).rstrip('; }')  # strip off the matching end "}"
    result = re.split('i:', result)  # break down the link by the index value (which kills the value 'i:')
    result.remove('')  # delete the initial blank entry
    result = ["i:" + s for s in result]  # add the stripped 'i:' back to the elements

def print_plugin_list(plugin_list):
    for i, r in enumerate(plugin_list, 0):
        plugin_name = (re.search(r'(?<=")(.*)(?=")', plugin_list[i]).group())  # .group() gets the plugin values
        plugin_length = (re.search(r'(?<=")(.*)(?=")', plugin_list[i]).span())  # .span() gets start & end of match
        plugin_length1 = plugin_length[1] - plugin_length[0]  # calculate length of plugin name (needed)
        print("{}: {}".format(i, plugin_name))  # Print an indexed list of plugins to choose from.


# If is a list request, just pump out the list with an index number
if args.list or args.func == 'list':
    print_plugin_list(result)

# If its a delete request, cycle through the list, and delete the lines by index number
if args.func == 'del':
    numbers = args.numbers
    for n in numbers:
        print(result[n])
    ans = input("***Confirm***: Remove these plugins from the list (y/N)?: ")
    if ans == 'Y' or ans == 'y':
        print("Confirmed")
        # check for and create a backup file from the sourcefile name
        if not os.path.exists(args.input.name + '.backup'):
            with open(args.input.name + '.backup', 'w'):
                pass

        with open(args.input.name + '.backup', 'a') as backupfile:
            backupdate = datetime.now()
            for n in numbers:
                # print("{},{}".format(backupdate, result[n]))
                print("{},{}".format(backupdate, result[n]), file=backupfile)
            print("Deleted plugins backup data written")

        # Do the actual delete from the data list
        for m in numbers:
            # print("{}={}".format(m, result[m]))
            del result[m]

        #Recreate the list

        #print_plugin_list(result)
        with open(args.output, 'w') as outputfile:
            output_list_prefix="a:"+str(len(result))+":{"    #set up the preamble
            print(output_list_prefix, file=outputfile, end = '')
            for i, r in enumerate(result, 0):
                plugin_name = (re.search(r'(?<=")(.*)(?=")', result[i]).group())  # .group() gets the plugin values
                plugin_length_tuple = (re.search(r'(?<=")(.*)(?=")', result[i]).span())  # .span() gets start & end of match
                plugin_length = plugin_length_tuple[1] - plugin_length_tuple[0]  # calculate length of plugin name (needed)needed
                print("i:{};s:{}:\"{}\";".format(i,plugin_length,plugin_name), file=outputfile, end = '')
            print("}", file=outputfile, end = '')
        print("{} written with new string to dump into wp_options / active_plugins field".format(args.output))
    else:
        print("Cancelled")