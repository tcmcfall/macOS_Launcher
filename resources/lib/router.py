# -*- coding: utf-8 -*-
import sys
from urllib.parse import parse_qs, unquote_plus

import xbmcgui

from .constants import ADDON
from .log import warn
from .ui import root_ui, apps_ui, favs_ui
from .favorites import save_favorite, remove_favorite, sync_kodi_favorites_with_saved
from .artwork import get_app_art, clear_cache
from .macos import hide_kodi, activate_kodi, open_app_wait

def _params() -> dict:
    if len(sys.argv) < 3 or not sys.argv[2]:
        return {}
    q = sys.argv[2]
    if q.startswith("?"):
        q = q[1:]
    return {k: v[0] for k, v in parse_qs(q).items() if v}

def _notify(msg: str) -> None:
    xbmcgui.Dialog().notification(ADDON.getAddonInfo("name"), msg, xbmcgui.NOTIFICATION_INFO, 2500)

def route() -> None:
    base_url = sys.argv[0]
    handle = int(sys.argv[1])
    p = _params()
    a = p.get("a", "")

    try:
        if a in ("", "root"):
            root_ui(handle, base_url); return
        if a == "apps":
            apps_ui(handle, base_url); return
        if a == "favs":
            favs_ui(handle, base_url); return
        if a == "launch":
            _launch(p.get("path","")); return
        if a == "save_fav":
            path = p.get("path","")
            if path:
                name = _best_name(path)
                save_favorite(name, path)
                sync_kodi_favorites_with_saved()
                _notify(f"Saved favorite: {name}")
            return
        if a == "remove_fav":
            path = p.get("path","")
            if path and remove_favorite(path):
                _notify("Removed from Saved Favorites")
            return
        if a == "add_kodi_fav":
            # harden by saving first; then sync favourites.xml
            path = p.get("path","")
            name = p.get("name") or _best_name(path)
            if path:
                save_favorite(name, path)
                sync_kodi_favorites_with_saved()
                _notify("Added to Kodi Favorites")
            return
        if a == "refresh_art":
            path = p.get("path","")
            if path:
                get_app_art(path, generate=True, force_refresh=True)
                _notify("Artwork refreshed")
            return
        if a == "clear_cache":
            clear_cache()
            _notify("Artwork cache cleared")
            return

        warn(f"Unknown action: {a}")
        root_ui(handle, base_url)

    except Exception as e:
        warn(f"route exception: {e}")
        xbmcgui.Dialog().ok(ADDON.getAddonInfo("name"), "An error occurred:", str(e))

def _best_name(app_path: str) -> str:
    import os
    b = os.path.basename(app_path)
    return b[:-4] if b.lower().endswith(".app") else b

def _launch(app_path: str) -> None:
    if not app_path:
        raise ValueError("Missing path parameter")

    try:
        activate_kodi()
    except Exception:
        pass

    hide_kodi()
    ok = open_app_wait(app_path)
    activate_kodi()

    if not ok:
        xbmcgui.Dialog().notification(ADDON.getAddonInfo("name"), "Failed to launch app.", xbmcgui.NOTIFICATION_ERROR, 3500)
