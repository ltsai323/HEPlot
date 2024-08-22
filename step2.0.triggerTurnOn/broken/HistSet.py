import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import math
import mplhep as hep
from uncertainties import ufloat, unumpy




'''
def GetOrder(maxNUMBER:float) -> float:
    index_to_10 = int(math.log10(maxNUMBER))
    return 10**index_to_10
'''


# Create a ratio plot function
class HistSet:
    def __init__(self, hist, **xargs):
        self.hist = hist
        for name, val in xargs.items():
            setattr(self, name, val)


def GetBinCenter(h:HistSet) -> list:
    return h.hist.axes.centers[0]
def GetBinWidth(h:HistSet) -> list:
    return h.hist.axes.widths[0]
def GetBinData(h:HistSet) -> list:
    ''' return a list of ufloat(). Get bin content with bin error '''
    #return unumpy.uarray( h.hist.values(), h.hist.errors() )
    return unumpy.uarray( h.orig_obj.values(), h.orig_obj.errors() )
def GetBinContent(h:HistSet) -> list:
    return unumpy.nominal_values(getBinData(h))
def GetBinError(h:HistSet) -> list:
    return unumpy.std_devs(getBinData(h))

def Scale(h:HistSet, scaleFACTOR:float):
    h.orig_obj._values *= scaleFACTOR
    h.orig_obj._variances *= scaleFACTOR*scaleFACTOR
    h.hist = h.orig_obj.to_hist() # update hist.Hist object
    h.desc += f' (SF={scaleFACTOR:.1f})'


def getHistMinForVisualization(h:HistSet, outTYPE:str) -> float:
    if outTYPE == 'linear':
        return 0
    if outTYPE == 'log':
        return min( [ v for v in getBinContent(h) if v != 0. ] ) * 0.1
    if outTYPE == 'original':
        return min(getBinContent(h))
    raise IOError(f'[InvalidArgument] getHistMinForVisualization() got outTYPE == "{ outTYPE }".')

def getHistMaxForVisualization(h:HistSet, outTYPE:str) -> float:
    if outTYPE == 'linear':
        return max(getBinContent(h)) * 2.0
    if outTYPE == 'log':
        return max(getBinContent(h)) * 1000.
    if outTYPE == 'original':
        return max(getBinContent(h))
    raise IOError(f'[InvalidArgument] getHistMaxForVisualization() got outTYPE == "{ outTYPE }".')

def GetVisualizationRange(h:HistSet, outTYPE:str='linear') -> tuple:
    return ( getHistMinForVisualization(h,outTYPE), getHistMaxForVisualization(h,outTYPE) )
    




MYCOLORS = [ '#8C736F', '#D4B8B4', '#ADAAA5', '#B7B7BD', '#AAB8AB', '#A08887', '#53565C']
MORANDI_DARK = ['#2D241F', '#614E52', '#7A6747', '#A06A50', '#605D54', '#511F1E', '#7D6647', '#69647B']
MORANDI_LIGHT= ['#D0C1C6', '#D6D6D6', '#BCA9A2', '#92ACD1', '#9B908A']
#MORANDI_SERIES = ['#903B1C', '#955839', '#A68E76', '#5F524A', '#A0765D']
MORANDI_SERIES = ['#D0C1C6', '#D6D6D6', '#BCA9A2', '#92ACD1', '#9B908A']
MY_MORANDI_LIGHT = ['#92ACD1', '#B17A7D', '#D0C1C6']
MY_MORANDI_LIGHT = ['#D5A1A3',  '#DFD8AB', '#B4C6DC'] # 0 2

def light_colors(idx):
    return MY_MORANDI_LIGHT[idx]

PLOTSTYLE_DATA   = { 'linestyle': 'None', 'color': 'black', 'marker': 'o', 'barsabove':True }
# 0 3 7 dark
PLOTSTYLE_STAR1 = { 'linestyle': 'None', 'color': light_colors(1), 'marker': '*', 'barsabove':True }
PLOTSTYLE_DIAMOND1 = { 'linestyle': 'None', 'color': light_colors(2), 'marker': 'D', 'barsabove':True }
PLOTSTYLE_HIST = { 'histtype': 'fill', 'edgecolor': '1', 'linewidth': 0.5 } # need to set color afterhand

INFO_CMS_PRELIMIILARY_UL2016PREVFP  = {'label':'Prelimilary', 'data':True, 'lumi':19.52, 'year':'UL2016preVFP' , 'loc':2}
INFO_CMS_PRELIMIILARY_UL2016POSTVFP = {'label':'Prelimilary', 'data':True, 'lumi':16.81, 'year':'UL2016postVFP', 'loc':2}

