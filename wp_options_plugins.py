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
    return parser.parse_args()

args = get_cli_arguments()

for line in args.input:
    print("Line: {}".format(line))
    print(line.split('{'))
    pattern = re.compile(r"^a:\d*:(.*)")
    match = pattern.search(line)
    result = match.group(1)
    #print("Regex:\n{}".format(match.group(1)))
    print()






#print("input path: {0}".format(args.input))
# for line in args.input:
# #    print (line.strip())
#     print(unserialize(line))

# Parse the serialized string
