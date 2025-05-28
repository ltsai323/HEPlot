#!/usr/bin/env python3
import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import textwrap

import math
import mplhep as hep
from uncertainties import ufloat, unumpy
from MyROOTPlotSetup.DrawObj_TGraphAsymmError import DrawObj_TGraphAsymmError
from MyROOTPlotSetup.DrawObj_TH1F             import DrawObj_TH1F

def info(mesg):
    print(f'i@ {mesg}')

DEBUG_MODE = True
def BUG(mesg):
    if DEBUG_MODE:
        print(f'b@ {mesg}')


INFO_CMS_PRELIMIILARY_UL2016PREVFP  = {'label':'Prelimilary', 'data':True, 'lumi':19.52, 'year':'UL2016preVFP' , 'loc':2}
INFO_CMS_PRELIMIILARY_UL2016POSTVFP = {'label':'Prelimilary', 'data':True, 'lumi':16.81, 'year':'UL2016postVFP', 'loc':2}
INFO_CMS_PRELIMIILARY_2022EE        = {'label':'Prelimilary', 'data':True, 'lumi':26.81, 'year':'2022EE'       , 'loc':2, 'com':13.6}

def DrawContentAtPad(ax, plotobjs,
        xLABEL:str=None, yLABEL:str=None, ySCALE:str=None, yRANGE:tuple=None, **otherargs_notused ):
    for plotobj in plotobjs:
        info(f'[DrawObject] {plotobj}')
        plotobj.Draw(ax)

    if xLABEL: ax.set_xlabel(xLABEL)
    if yLABEL:
        ax.set_ylabel(yLABEL.replace('\\n','\n'))
    yAxisConfigs(ax,yRANGE, ySCALE)
    ax.grid(True, which='major', axis='y')

def yAxisConfigs(ax, yRANGE:tuple=None, ySCALE:str=None):
    if yRANGE: ax.set_ylim(*[ float(v) for v in yRANGE ])

    if ySCALE == None: return

    ax.set_yscale(ySCALE)
    if ySCALE == 'log': return # if the log scale, no need further configurations
    ax.yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))


def GetArgs_InputYAML(argv):
    #return 'newinput.yaml'
    return argv[1]


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

    hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    hep.style.use("CMS") # string aliases work too
    fig, (ax_upper, ax_lower) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, sharex=True, figsize=(10,8))
    DrawContentAtPad(ax_upper, upper_plotables, **conf['upperpad'])
    
    reordered_legend_items = sum([ 0 if 'legorder' in plotable else 1 for plotable in reversed(conf['upperpad']['plotables']) ])
    legNcolumn = conf['upperpad']['legNcolumn'] if 'legNcolumn' in conf['upperpad'] else 1
    legFONTsize = conf['upperpad']['legFONTsize'] if 'legFONTsize' in conf['upperpad'] else 'small'

    if reordered_legend_items == 0:
        info(f'[ReorderedLegend] Use the option "legorder" to arrange items')
        handles, labels = ax_upper.get_legend_handles_labels()
        # Custom order for legend
        ### sort legend order in ascend ordered.
        my_order = { plotable['legorder']: plotable['label'] for plotable in reversed(conf['upperpad']['plotables']) }

        ordered_labels = [ my_order[o] for o in sorted(my_order.keys()) ]
        ordered_handles = [ handles[labels.index(label)] for label in ordered_labels ]

        ax_upper.legend(ordered_handles, ordered_labels, ncol=legNcolumn, fontsize=legFONTsize)
    else:
        info(f'[DefaultLegend] Use default item order.')
        ax.legend(ncol=legNcolumn, fontsize=legFONTsize)
        ax_upper.legend()

    DrawContentAtPad(ax_lower, lower_plotables, **conf['lowerpad'])
    ax_lower.axhline(y=1.0, color='gray', linestyle='-', linewidth=0.5)

    hep.cms.label(ax=ax_upper, **INFO_CMS_PRELIMIILARY_2022EE)

    figname = conf['figNAME']
    if figname == '':
        plt.show()
        current_figsize = fig.get_size_inches()
        info(f"[AdjustedFigureSize] {current_figsize[0]} inches x {current_figsize[1]} inches")
    else:
        plt.savefig(figname)
        info(f'[SavedOutput] {figname}')


