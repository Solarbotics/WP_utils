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