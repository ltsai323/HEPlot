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


INFO_CMS_PRELIMIILARY_UL2016PREVFP  = {'label':'Prelimilary', 'data':True, 'lumi':19.52, 'year':'UL2016preVFP' , 'loc':2}
INFO_CMS_PRELIMIILARY_UL2016POSTVFP = {'label':'Prelimilary', 'data':True, 'lumi':16.81, 'year':'UL2016postVFP', 'loc':2}

def DrawContentAtPad(ax, plotobjs,
        xLABEL:str=None, yLABEL:str=None, ySCALE:str=None, yRANGE:tuple=None, **otherargs_notused ):
    for plotobj in plotobjs:
        plotobj.Draw(ax)

    if xLABEL: ax.set_xlabel(xLABEL)
    if yLABEL: ax.set_ylabel(yLABEL)
    yAxisConfigs(ax,yRANGE, ySCALE)
    ax.grid(True, which='major', axis='y')

def yAxisConfigs(ax, yRANGE:tuple=None, ySCALE:str=None):
    if yRANGE: ax.set_ylim(*[ float(v) for v in yRANGE ])

    if ySCALE == None: return

    ax.set_yscale(ySCALE)
    if ySCALE == 'log': return # if the log scale, no need further configurations
    ax.yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
### the parameters are used in yaml file.
def DrawUpperPad(ax, plotobjs,
        xLABEL:str=None, yLABEL:str=None, ySCALE:str=None, yRANGE:tuple=None, **otherargs_notused ):
    #hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    #hep.style.use("CMS") # string aliases work too
    #fig, ax = plt.subplots(figsize=(10,8))

    #ax.yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    #ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    for plotobj in plotobjs:
        plotobj.Draw(ax)

    if xLABEL: ax.set_xlabel(xLABEL)
    if yLABEL: ax.set_ylabel(yLABEL)
    if yRANGE: ax.set_ylim(*[ float(v) for v in yRANGE ])
    if ySCALE: ax.set_yscale(ySCALE)
    ax.legend()
    ax.grid(True, which='major', axis='y')
    ax.yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    #hep.cms.label(ax=ax, **INFO_CMS_PRELIMIILARY_UL2016POSTVFP)
def DrawLowerPad(ax, plotobjs,
        xLABEL:str=None, yLABEL:str=None, ySCALE:str=None, yRANGE:tuple=None, **otherargs_notused ):
    #hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    #hep.style.use("CMS") # string aliases work too
    #fig, ax = plt.subplots(figsize=(10,8))

    #ax.yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    #ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    for plotobj in plotobjs:
        plotobj.Draw(ax)

    if xLABEL: ax.set_xlabel(xLABEL)
    if yLABEL: ax.set_ylabel(yLABEL)
    if yRANGE: ax.set_ylim(*[ float(v) for v in yRANGE ])
    if ySCALE: ax.set_yscale(ySCALE)
    ax.grid(True, which='major', axis='y')

def DrawRatioPlotablesWithCMSFormat(
        upperPLOTOBJs:list=[], upperYlabel:str=None, upperYscale:str=None, upperYrange:tuple=None,
        lowerPLOTOBJs:list=[], lowerYlabel:str=None, lowerYscale:str=None, lowerYrange:tuple=None,
                    xLABEL:str=None,
                    figNAME:str=None,
                    **otherargs_notused
                    ):
    hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    hep.style.use("CMS") # string aliases work too
    #fig, ax = plt.subplots(figsize=(10,8))
    fig, (ax_upper, ax_lower) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, sharex=True, figsize=(10,8))

    #ax.yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    #ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    if xLABEL: ax_lower.set_xlabel(xLABEL)

    ######### upper pad ############
    for plotobj in upperPLOTOBJs:
        plotobj.Draw(ax_upper)
    ax_upper.set_xlabel('')
    if upperYlabel: ax_upper.set_ylabel(upperYlabel)
    if upperYrange: ax_upper.set_ylim(*[ float(v) for v in upperYrange ])
    if upperYscale: ax_upper.set_yscale(upperYscale)
    ax_upper.legend()

    ######### lower pad ############
    for plotobj in lowerPLOTOBJs:
        plotobj.Draw(ax_lower)
    ax_lower.set_xlabel('')
    if lowerYlabel: ax_lower.set_ylabel(lowerYlabel)
    if lowerYrange: ax_lower.set_ylim(*[ float(v) for v in lowerYrange ])
    if lowerYscale: ax_lower.set_yscale(lowerYscale)
    #ax_lower.legend()

    plt.suptitle('')
    plt.grid(True, which='major', axis='y')

    hep.cms.label(ax=ax_upper, **INFO_CMS_PRELIMIILARY_UL2016POSTVFP)
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

    upper_plotables = [ DrawObjFactory(plotable) for plotable in reversed(conf['upperpad']['plotables']) ]
    lower_plotables = [ DrawObjFactory(plotable) for plotable in reversed(conf['lowerpad']['plotables']) ]
    #DrawRatioPlotablesWithCMSFormat(pp,**conf)
    hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    hep.style.use("CMS") # string aliases work too
    fig, (ax_upper, ax_lower) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, sharex=True, figsize=(10,8))
    #DrawUpperPad(ax_upper, upper_plotables, **conf['upperpad'])
    #DrawLowerPad(ax_lower, lower_plotables, **conf['lowerpad'])
    DrawContentAtPad(ax_upper, upper_plotables, **conf['upperpad'])
    ax_upper.legend()

    DrawContentAtPad(ax_lower, lower_plotables, **conf['lowerpad'])
    ax_lower.axhline(y=1.0, color='gray', linestyle='-', linewidth=0.5)

    hep.cms.label(ax=ax_upper, **INFO_CMS_PRELIMIILARY_UL2016POSTVFP)

    figname = conf['figNAME']
    if figname == '':
        plt.show()
        current_figsize = fig.get_size_inches()
        print(f"[AdjustedFigureSize] {current_figsize[0]} inches x {current_figsize[1]} inches")
    else:
        plt.savefig(figname)
        print(f'[SavedOutput] {figname}')


