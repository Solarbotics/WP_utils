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

ToDO:
- Read in the list from saved file (copied from the database field)
- Make it human-readable (I find a newline before each "a:[0-9]*.," regex does nicely)
- Select which entry to disable
- Write out the disabled entry to log file for later re-inclusion (even manually
- re-write out a fresh list, with a:xx = new total number of plugins, and each list_element having a sequential "a:xx" element followed by the remaining datafields
     This list then can be re-written to the database directly to disable the plugins in question.

Spec: Dave Hrynkiw, April 11 2020
"""