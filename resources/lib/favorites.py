# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET
from typing import Dict, List

import xbmc

from .constants import FAV_DIR
from .util import ensure_dir, sha1, read_json, write_json
from .log import warn

def _fav_file(app_path: str) -> str:
    ensure_dir(FAV_DIR)
    return os.path.join(FAV_DIR, sha1(app_path) + ".json")

def list_saved() -> List[Dict[str, str]]:
    ensure_dir(FAV_DIR)
    out: List[Dict[str, str]] = []
    for fn in sorted(os.listdir(FAV_DIR)):
        if fn.endswith(".json"):
            p = os.path.join(FAV_DIR, fn)
            data = read_json(p, {})
            if isinstance(data, dict) and data.get("path") and data.get("name"):
                out.append(data)
    return out

def save_favorite(name: str, app_path: str) -> None:
    ensure_dir(FAV_DIR)
    write_json(_fav_file(app_path), {"name": name, "path": app_path})

def remove_favorite(app_path: str) -> bool:
    try:
        os.remove(_fav_file(app_path))
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        warn(f"remove_favorite err: {e}")
        return False

def _favourites_xml_path() -> str:
    return xbmc.translatePath("special://profile/favourites.xml")

def _plugin_url_for_launch(app_path: str) -> str:
    from urllib.parse import quote_plus
    return f"plugin://plugin.program.macoslauncher/?a=launch&path={quote_plus(app_path)}"

def sync_kodi_favorites_with_saved() -> int:
    saved = list_saved()
    if not saved:
        return 0

    path = _favourites_xml_path()
    root = ET.Element("favourites")
    if os.path.isfile(path):
        try:
            root = ET.parse(path).getroot()
        except Exception:
            root = ET.Element("favourites")

    existing = set((fav.get("name") or "", (fav.text or "").strip()) for fav in root.findall("favourite"))

    added = 0
    for item in saved:
        name = item["name"]
        plugin_url = _plugin_url_for_launch(item["path"])
        if (name, plugin_url) in existing:
            continue
        fav_el = ET.SubElement(root, "favourite")
        fav_el.set("name", name)
        fav_el.text = plugin_url
        added += 1

    if added:
        tmp = path + ".tmp"
        try:
            ET.ElementTree(root).write(tmp, encoding="utf-8", xml_declaration=True)
            os.replace(tmp, path)
        except Exception as e:
            warn(f"write favourites.xml failed: {e}")
            try:
                if os.path.exists(tmp): os.remove(tmp)
            except Exception:
                pass

    return added
