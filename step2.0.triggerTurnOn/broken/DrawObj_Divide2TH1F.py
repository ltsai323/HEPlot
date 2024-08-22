import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import math
import mplhep as hep
from uncertainties import ufloat, unumpy





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



class DrawObj_Divide2TH1F:
    name = 'Divide2TH1F'
    def __init__(self, yamlCONFIGs):
        try:
            config = yamlCONFIGs
            self.file = config['file']
            self.objname = config['objname']
            self.label = config['label']
            self.plotstyle = config['plotstyle']
        except KeyError as e:
            mesg = f'Invalid key found in yaml configuration. please check'
            print('\n\n')
            print('-' * len(mesg))
            print(mesg)
            print('-' * len(mesg))
            print('\n\n')
            raise KeyError(e)
    def Draw(self,ax):
        try:
            f = uproot.open(self.file)
            hist1 = f[self.objname]
            hist2 = f[self.objname]
        except IOError as e:
            mesg = f'parameter: opened file "{ self.file }" and "{ self.objname }"'
            print('\n\n')
            print('-' * len(mesg))
            print(mesg)
            print('-' * len(mesg))
            print('\n\n')
            raise IOError(e)
        DrawEP(ax, graph_obj, self.label, self.plotstyle)
    
