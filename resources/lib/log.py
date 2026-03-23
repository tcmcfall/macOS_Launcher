# -*- coding: utf-8 -*-
import xbmc
from .constants import ADDON_ID

def info(msg: str) -> None:
    xbmc.log(f"[{ADDON_ID}] {msg}", xbmc.LOGINFO)

def warn(msg: str) -> None:
    xbmc.log(f"[{ADDON_ID}] {msg}", xbmc.LOGWARNING)

def error(msg: str) -> None:
    xbmc.log(f"[{ADDON_ID}] {msg}", xbmc.LOGERROR)
