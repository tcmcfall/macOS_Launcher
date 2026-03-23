# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo("id")
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_VERSION = ADDON.getAddonInfo("version")

ADDON_ICON = xbmc.translatePath("special://home/addons/%s/resources/media/icon.png" % ADDON_ID)
ADDON_FANART = xbmc.translatePath("special://home/addons/%s/resources/media/fanart.jpg" % ADDON_ID)

PROFILE_DIR = xbmc.translatePath(ADDON.getAddonInfo("profile"))
FAV_DIR = PROFILE_DIR + "favorites/"
CACHE_DIR = PROFILE_DIR + "cache/"
ART_DIR = CACHE_DIR + "artwork/"
