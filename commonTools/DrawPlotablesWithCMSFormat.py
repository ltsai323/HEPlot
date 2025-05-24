#!/usr/bin/env python3
import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import math
import mplhep as hep
from uncertainties import ufloat, unumpy
from MyROOTPlotSetup.DrawObj_TGraphAsymmError import DrawObj_TGraphAsymmError
from MyROOTPlotSetup.DrawObj_TH1F             import DrawObj_TH1F



INFO_CMS_PRELIMIILARY_2022EE        = {'label':'Prelimilary', 'data':True, 'lumi':26.81, 'year':'2022EE'       , 'loc':2, 'com': 13.6}

### the parameters are used in yaml file.
def DrawPlotablesWithCMSFormat(plotobjs,
                    xLABEL:str=None,
                    yLABEL:str=None, ySCALE:str=None, yRANGE:tuple=None,
                    figNAME:str=None,
                    legNcolumn:int=1, legFONTsize:str='small',
                    **otherargs_notused
                    ):
    hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    hep.style.use("CMS") # string aliases work too
    fig, ax = plt.subplots(figsize=(10,8))

    ax.yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    for plotobj in plotobjs:
        plotobj.Draw(ax)

    if xLABEL: ax.set_xlabel(xLABEL)
    if yLABEL: ax.set_ylabel(yLABEL)
    if yRANGE: ax.set_ylim(*[ float(v) for v in yRANGE ])
    if ySCALE: ax.set_yscale(ySCALE)
    ax.legend(ncol=legNcolumn, fontsize=legFONTsize)
    plt.suptitle('')
    plt.grid(True, which='major', axis='y')

    #hep.cms.label(ax=ax, **INFO_CMS_PRELIMIILARY_UL2016POSTVFP)
    hep.cms.label(ax=ax, **INFO_CMS_PRELIMIILARY_2022EE)
    if figNAME:
        plt.savefig(figNAME)
        print(f'[SavedOutput] {figNAME}')
    else:
        plt.show()
        current_figsize = fig.get_size_inches()
        print(f"[AdjustedFigureSize] {current_figsize[0]} inches x {current_figsize[1]} inches")

def GetArgs_InputYAML(argv):
    #return 'newinput.yaml'
    return argv[1]

#class YAMLConfigs:
#    def __init__(self, yamlCONFIGs):
#        config = yamlCONFIGs
#        self.figNAME = config['figNAME'] if 'figNAME' in config else None
#        self.yLABEL = config['yLABEL'] if 'yLABEL' in config else None
#        self.yRANGE = config['yRANGE'] if 'yRANGE' in config else None
#        self.xLABEL = config['xLABEL'] if 'xLABEL' in config else None
def DrawObjFactory(plotable):
    Type = plotable['type']
    if Type == DrawObj_TGraphAsymmError.name:
        return DrawObj_TGraphAsymmError(plotable)
    if Type == DrawObj_TH1F            .name:
        return DrawObj_TH1F            (plotable)
    raise IOError(f'[InvalidType] "{ plotable["type"] }" is an invalid plotable type. Please check yaml file')

if __name__ == "__main__":
    import yaml
    import sys
    fIN = GetArgs_InputYAML(sys.argv)

    with open(fIN,'r') as f:
        conf = yaml.safe_load(f)
        # yamlCONF = YAMLConfigs(conf)
        print(conf)

    pp = [ DrawObjFactory(plotable) for plotable in reversed(conf['plotables']) ]
    DrawPlotablesWithCMSFormat(pp,**conf)
