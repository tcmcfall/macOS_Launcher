# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from typing import Dict

import xbmcgui
import xbmcplugin

from .constants import ADDON, ADDON_ID, ADDON_ICON, ADDON_FANART
from .apps import discover_apps
from .favorites import list_saved
from .artwork import get_app_art

def _url(base: str, params: Dict[str, str]) -> str:
    return base + "?" + urlencode(params)

def root_ui(handle: int, base_url: str) -> None:
    xbmcplugin.setPluginCategory(handle, ADDON.getAddonInfo("name"))
    xbmcplugin.setContent(handle, "files")

    for label, params in [
        (ADDON.getLocalizedString(30003) or "macOS Applications", {"a": "apps"}),
        (ADDON.getLocalizedString(30002) or "Saved Favorites", {"a": "favs"}),
    ]:
        li = xbmcgui.ListItem(label=label)
        li.setArt({"thumb": ADDON_ICON, "poster": ADDON_ICON, "fanart": ADDON_FANART, "icon": ADDON_ICON})
        xbmcplugin.addDirectoryItem(handle, _url(base_url, params), li, isFolder=True)

    xbmcplugin.endOfDirectory(handle, succeeded=True, cacheToDisc=False)

def apps_ui(handle: int, base_url: str) -> None:
    xbmcplugin.setPluginCategory(handle, "macOS Applications")
    xbmcplugin.setContent(handle, "files")

    # IMPORTANT: do not generate artwork here; only use cached if present.
    for a in discover_apps():
        name, path = a["name"], a["path"]
        li = xbmcgui.ListItem(label=name)

        art = get_app_art(path, generate=False)
        if art:
            li.setArt({"thumb": art, "icon": art, "poster": art, "fanart": ADDON_FANART})
        else:
            li.setArt({"thumb": ADDON_ICON, "icon": ADDON_ICON, "poster": ADDON_ICON, "fanart": ADDON_FANART})

        cm = [
            (ADDON.getLocalizedString(30004) or "Add to Saved Favorites", f'RunPlugin("{_url(base_url, {"a":"save_fav","path":path})}")'),
            (ADDON.getLocalizedString(30006) or "Add to Kodi Favorites", f'RunPlugin("{_url(base_url, {"a":"add_kodi_fav","path":path,"name":name})}")'),
            (ADDON.getLocalizedString(30007) or "Refresh artwork (generate now)", f'RunPlugin("{_url(base_url, {"a":"refresh_art","path":path})}")'),
        ]
        li.addContextMenuItems(cm, replaceItems=False)

        xbmcplugin.addDirectoryItem(handle, _url(base_url, {"a": "launch", "path": path}), li, isFolder=False)

    xbmcplugin.endOfDirectory(handle, succeeded=True, cacheToDisc=False)

def favs_ui(handle: int, base_url: str) -> None:
    xbmcplugin.setPluginCategory(handle, "Saved Favorites")
    xbmcplugin.setContent(handle, "files")

    for item in list_saved():
        name, path = item["name"], item["path"]
        li = xbmcgui.ListItem(label=name)

        # Favorites list is small; allow generation to improve UX.
        art = get_app_art(path, generate=True)
        if art:
            li.setArt({"thumb": art, "icon": art, "poster": art, "fanart": ADDON_FANART})
        else:
            li.setArt({"thumb": ADDON_ICON, "icon": ADDON_ICON, "poster": ADDON_ICON, "fanart": ADDON_FANART})

        cm = [
            (ADDON.getLocalizedString(30005) or "Remove from Saved Favorites", f'RunPlugin("{_url(base_url, {"a":"remove_fav","path":path})}")'),
            (ADDON.getLocalizedString(30006) or "Add to Kodi Favorites", f'RunPlugin("{_url(base_url, {"a":"add_kodi_fav","path":path,"name":name})}")'),
            (ADDON.getLocalizedString(30007) or "Refresh artwork (generate now)", f'RunPlugin("{_url(base_url, {"a":"refresh_art","path":path})}")'),
        ]
        li.addContextMenuItems(cm, replaceItems=False)

        xbmcplugin.addDirectoryItem(handle, _url(base_url, {"a": "launch", "path": path}), li, isFolder=False)

    xbmcplugin.endOfDirectory(handle, succeeded=True, cacheToDisc=False)
