__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2016, AllThingsTalk"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@allthingstalk.com"
__status__ = "Prototype"  # "Development", or "Production"

import os
import json
import re
from kivy.properties import dpi2px

#toggleButton_normal = "images\up_button.png"
#toggleButton_down = "images\down_button.png"
#toggleButton_size = (41, 60)

#gauge_gauge = "images/controls/gauge/cadran.png"
#gauge_needle = "images/controls/gauge/needle.png"

#hor_slider_size = (100, 40)
#ver_slider_size = (40, 100)

skinTypes = {}                  # dictionary of all skin types. value is dictionary of skin names + skin

def loadSkins(path):
    """load all the available skins from disk"""
    global skinTypes
    skinTypes = {}                                  # clear any prev values.
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            skins = {}
            skinTypes[dir] = skins
            for root2, dirs2, files2 in os.walk(os.path.join(root, dir)):
                for skinName in dirs2:
                    with open(os.path.join(root2, skinName, 'definition.json')) as data_file:
                        skin = json.load(data_file)
                        skin['path'] = os.path.join(root2, skinName)
                        skin['name'] = skinName
                        skins[skinName] = skin


def getAvailableSkins(type):
    skins = skinTypes[type]
    return [value for name, value in skins.iteritems()]

def getSkin(type, asset):
    """get the skin for the specified control type and state.
    The asset can overwrite default values"""
    skins = skinTypes[type]
    if skins:
        if asset and asset.skin and "name" in asset.skin:
            return skins[asset.skin["name"]]
        else:
            return skins["default"]

def metricToPixels(value):
    result = None
    if isinstance(value, basestring):
        match = re.match(r"([0-9]+)([a-z]+)", value, re.I)
        if match:
            res = match.groups()
            return dpi2px(res[0], res[1])
    elif type(value) is int:
        return value
    return 100

def getControlSize(skin, asset):
    """get the size of control. The asset can overwrite it."""
    if skin:
        if asset and asset.skin and "size" in asset.skin:
            width = metricToPixels(skin['size'][0])
            height = metricToPixels(skin['size'][1])
            return (width * float(asset.skin["size"]), height * float(asset.skin["size"]))
        return (skin["size"][0], skin["size"][1])

    return (100, 100)



def getVar(skin, asset, name):
    if asset and asset.skin and name in asset.skin:
        return asset.skin[name]
    return skin[name]

def getMinimum(type, value, typeInfo):
    if type in ["slider", "gauge"]:
        if 'minimum' in typeInfo:
            result = typeInfo['minimum']
        elif value > 0:
            result = 0
        else:
            result = value * 2
        return result

def getMaximum(type, value, typeInfo):
    if type in ["slider", "gauge"]:
        if 'maximum' in typeInfo:
            result = typeInfo['maximum']
        elif value > 0:
            result = value * 2
        else:
            result = 0
        return result

def getStep(type, typeInfo):
    if type == "slider":
        if typeInfo['type'] == "number":
            return 0.1
        else:
            return 1                                    # we need to make certain that for integers, we use a step size of 1