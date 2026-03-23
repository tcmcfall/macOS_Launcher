# -*- coding: utf-8 -*-
# Artwork policy (critical to avoid timeouts):
# - Directory listings MUST be fast. Do NOT generate artwork for every app during listing.
# - We only return an existing cached PNG unless generate=True is explicitly requested.
#
# Generation is triggered by:
# - Context menu "Refresh artwork (generate now)"
# - Saved Favorites view (small list) can generate if desired (caller decides)

import os
import time
import glob
from typing import Optional

from .constants import ADDON, ART_DIR
from .util import ensure_dir, sha1
from .log import warn
from .macos import run

def _cache_path_for(app_path: str) -> str:
    ensure_dir(ART_DIR)
    return os.path.join(ART_DIR, sha1(app_path) + ".png")

def _is_cache_valid(path: str) -> bool:
    if not os.path.exists(path):
        return False
    max_age_days = int(ADDON.getSetting("art_cache_max_age_days") or "30")
    if max_age_days <= 0:
        return True
    age = time.time() - os.path.getmtime(path)
    return age <= (max_age_days * 86400)

def clear_cache() -> None:
    if not os.path.isdir(ART_DIR):
        return
    for f in glob.glob(os.path.join(ART_DIR, "*.png")):
        try:
            os.remove(f)
        except Exception:
            pass

def get_app_art(app_path: str, *, generate: bool=False, force_refresh: bool=False) -> Optional[str]:
    cache_path = _cache_path_for(app_path)

    # Fast path: existing cache
    if (not force_refresh) and _is_cache_valid(cache_path):
        return cache_path

    # If generation is not explicitly requested, do NOT do expensive work (prevents UI timeout).
    if not generate:
        return cache_path if os.path.isfile(cache_path) else None

    ensure_dir(os.path.dirname(cache_path))
    prefer_icns = ADDON.getSettingBool("prefer_icns")
    fallback_ql = ADDON.getSettingBool("fallback_quicklook")

    if prefer_icns:
        icns = _find_icns(app_path)
        if icns and _icns_to_png(icns, cache_path):
            return cache_path

    if fallback_ql and _quicklook_png(app_path, cache_path):
        return cache_path

    return None

def _find_icns(app_path: str) -> Optional[str]:
    res_dir = os.path.join(app_path, "Contents", "Resources")
    if not os.path.isdir(res_dir):
        return None
    preferred = os.path.join(res_dir, "AppIcon.icns")
    if os.path.isfile(preferred):
        return preferred
    icns_files = sorted(glob.glob(os.path.join(res_dir, "*.icns")))
    return icns_files[0] if icns_files else None

def _icns_to_png(icns_path: str, out_png: str) -> bool:
    tmp_dir = out_png + ".iconset"
    try:
        if os.path.isdir(tmp_dir):
            _rm_tree(tmp_dir)
        rc, _, _ = run(["/usr/bin/iconutil", "-c", "iconset", icns_path, "-o", tmp_dir])
        if rc != 0 or not os.path.isdir(tmp_dir):
            _rm_tree(tmp_dir)
            return False

        pngs = sorted(glob.glob(os.path.join(tmp_dir, "*.png")))
        if not pngs:
            _rm_tree(tmp_dir)
            return False

        def score(p: str) -> int:
            b = os.path.basename(p)
            s = 0
            for tok in ["1024", "512", "256", "128", "64", "32", "16"]:
                if tok in b:
                    s += int(tok) * 10
            try:
                s += int(os.path.getsize(p) / 1024)
            except Exception:
                pass
            return s

        best = sorted(pngs, key=score, reverse=True)[0]
        rc, _, _ = run(["/usr/bin/sips", "-s", "format", "png", best, "--out", out_png])
        _rm_tree(tmp_dir)
        return rc == 0 and os.path.isfile(out_png)
    except Exception as e:
        warn(f"icns_to_png exception: {e}")
        _rm_tree(tmp_dir)
        return False

def _quicklook_png(app_path: str, out_png: str) -> bool:
    out_dir = out_png + ".ql"
    try:
        if os.path.isdir(out_dir):
            _rm_tree(out_dir)
        os.makedirs(out_dir, exist_ok=True)
        rc, _, _ = run(["/usr/bin/qlmanage", "-t", "-s", "512", "-o", out_dir, app_path])
        if rc != 0:
            _rm_tree(out_dir)
            return False

        thumbs = sorted(glob.glob(os.path.join(out_dir, "*.png")))
        if not thumbs:
            _rm_tree(out_dir)
            return False

        os.replace(thumbs[0], out_png)
        _rm_tree(out_dir)
        return os.path.isfile(out_png)
    except Exception as e:
        warn(f"quicklook exception: {e}")
        _rm_tree(out_dir)
        return False

def _rm_tree(path: str) -> None:
    try:
        if os.path.isfile(path):
            os.remove(path)
            return
        for root, dirs, files in os.walk(path, topdown=False):
            for f in files:
                try: os.remove(os.path.join(root, f))
                except Exception: pass
            for d in dirs:
                try: os.rmdir(os.path.join(root, d))
                except Exception: pass
        try: os.rmdir(path)
        except Exception: pass
    except Exception:
        pass
