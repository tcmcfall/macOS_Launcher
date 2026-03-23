# -*- coding: utf-8 -*-
import os
from typing import Dict, List

from .constants import ADDON
from .log import info

def _enabled_dirs() -> List[str]:
    dirs: List[str] = []
    if ADDON.getSettingBool("include_applications"):
        dirs.append("/Applications")
    if ADDON.getSettingBool("include_system_applications"):
        dirs.append("/System/Applications")
    if ADDON.getSettingBool("include_user_applications"):
        home = os.path.expanduser("~")
        dirs.append(os.path.join(home, "Applications"))
    return [d for d in dirs if os.path.isdir(d)]

def _is_hidden(entry: str) -> bool:
    return entry.startswith(".")

def discover_apps() -> List[Dict[str, str]]:
    show_hidden = ADDON.getSettingBool("show_hidden_apps")
    found: Dict[str, str] = {}

    for root in _enabled_dirs():
        try:
            for entry in os.listdir(root):
                if not entry.endswith(".app"):
                    continue
                if (not show_hidden) and _is_hidden(entry):
                    continue
                full = os.path.join(root, entry)
                if os.path.isdir(full):
                    found[full] = os.path.splitext(entry)[0]
        except Exception as e:
            info(f"App scan error in {root}: {e}")

    return [{"name": n, "path": p} for p, n in sorted(found.items(), key=lambda kv: kv[1].lower())]
