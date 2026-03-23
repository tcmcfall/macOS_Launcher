# -*- coding: utf-8 -*-
# macOS Launcher for Kodi (plugin.program.macoslauncher)
#
# Notes:
# - Kodi opens this add-on as a pluginsource (plugin://...), even when listed under Program add-ons,
#   because <provides>executable</provides> is declared in addon.xml (matches means of v1.8.0).
# - Keep the entrypoint minimal; all routing lives in resources/lib/router.py.

from resources.lib.router import route

if __name__ == "__main__":
    route()
