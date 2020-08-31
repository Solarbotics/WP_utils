wp_options_plugins.py
A utility for managing what plugins are active within the wordpress
database.

If you have a bad plugin lock you out of the admin-side of wordpress,
you can often disable it by (s)ftp and renaming the directory, effectively
breaking it temporarily so you can reclaim access. EXCEPT this does
not work well with containerized servers, like Pantheon where you can
only work with file-structures very limited beyon the "dev" environment.

To disable a plugin from a TEST or LIVE environment, you have to access
the database directly, under the "wp_options" table, "active_plugins" field.

Managing this structure isn't easy, requiring a few hoop-jumps to do effectively.

Using phpmyadmin:
1. Navigate to the database your WP instance uses
2. Filter for the wp_options table (may be a few pages into your database table list)
3. "Filter Rows" for "active_plugins" (again, may be a few pages down)
4. Copy the content of "option_value" out to a textfile (default "wp_options.txt" is expected) to run against the python script

In your shell, show what plugins you have by:
$ python3 wp_options_plugins.py list