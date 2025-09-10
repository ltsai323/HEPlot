#!/usr/bin/env python3

### DrawPlotableWithCMSFormat.py inCONF.yaml dataORmc=mc commonINPUTfile=hi.root xLABEL=asdf
import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import logging
from pprint import pformat

log = logging.getLogger(__name__)


import math
import mplhep as hep
from uncertainties import ufloat, unumpy
from MyROOTPlotSetup.DrawObj_TGraphAsymmError import DrawObj_TGraphAsymmError
from MyROOTPlotSetup.DrawObj_TH1F             import DrawObj_TH1F
from MyROOTPlotSetup.DrawObj_TextLabelTH1F    import DrawObj_TextLabelTH1F
INFO_CMS_PRELIMIILARY_2022EE        = {'label':'Prelimilary', 'data':True , 'lumi':27.01, 'year':'2022EE'       , 'loc':2, 'com': 13.6}
INFO_CMS_PRELIMIILARY_Simulations   = {'label':''           , 'data':False, 'lumi':None , 'year':'Psuedodata'   , 'loc':2, 'com':13.6}

def DrawObjFactory(plotable, commonINPUTfile:str = None):
    Type = plotable['type']
    if commonINPUTfile is None or commonINPUTfile == '': ## once common input file put, ignore the original recorded input file
        pass
    else:
        plotable['file'] = commonINPUTfile
    if Type == DrawObj_TGraphAsymmError.name:
        return DrawObj_TGraphAsymmError(plotable)
    if Type == DrawObj_TH1F            .name:
        return DrawObj_TH1F            (plotable)
    if Type == DrawObj_TextLabelTH1F   .name:
        return DrawObj_TextLabelTH1F   (plotable)
    raise IOError(f'[InvalidType] "{ plotable["type"] }" is an invalid plotable type. Please check yaml file')

def nested_set(element, value, *keys):
    def set_val_withcheck(e,v,k):
        if not k in e: # if key does not in dict. raise warning or error
            log.warning(f'[InvalidConf] keys "{ keys }" does not exist in config.')
            # raise IOError(f'[InvalidConf] keys "{ keys }" does not exist in config.')
        else: # if key in dict, forbid user modify list
            if isinstance(e[k], list):
                raise KeyError(f'[UnableToUpdate] nested_set() forbids user update a list. The config {keys}:{value} is forbidden')
        e[k] = v
    if type(element) is not dict:
        raise AttributeError('nested_set() expects dict as first argument.')
    if len(keys) < 2:
        set_val_withcheck(element, value, keys[0])
        return

    _keys = keys[:-1]
    _element = element
    for key in _keys:
        _element = _element[key]
        if isinstance(_element, list):
            raise KeyError(f'[UnableToUpdate] nested_set() forbids user update a list. The config {keys}:{value} is forbidden')
    set_val_withcheck(_element, value, keys[-1])
    #_element[keys[-1]] = value

def update_opts(argOPTs) -> dict:
    def _get_key_and_value(theSTR):
        if '=' not in theSTR: raise IOError(f'[InvalidArg] arg {theSTR} is invalid. there should be a "=" sign')
        key, value = theSTR.split('=')
        return key,value

    opts = {}
    if argOPTs:
        for argOPT in argOPTs:
            conf_key, conf_val = _get_key_and_value(argOPT)
            opts[conf_key] = conf_val
    return opts

def update_conf(origCONF, updateOPTs):
    # lowerpad/xLABEL=3317
    # lowerpad/xLABEL and opt 3317

    for key, opt in updateOPTs.items():
        nested_set(origCONF, opt, *key.split('/'))

