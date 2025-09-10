#!/usr/bin/env python3
### DrawRatioPlotableWithCMSFormat.py inCONF.yaml dataORmc=mc commonINPUTfile=hi.root lowerpad/xLABEL=asdf
import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import textwrap
import logging
from pprint import pformat
import sys

log = logging.getLogger(__name__)

import math
import mplhep as hep
from uncertainties import ufloat, unumpy
from MyROOTPlotSetup.DrawObj_TGraphAsymmError          import DrawObj_TGraphAsymmError
from MyROOTPlotSetup.DrawObj_TH1F                      import DrawObj_TH1F
from MyROOTPlotSetup.DrawObj_TextLabelTGraphAsymmError import DrawObj_TextLabelTGraphAsymmError
from MyROOTPlotSetup.DrawObj_TextLabelTH1F             import DrawObj_TextLabelTH1F
import DrawTools



INFO_CMS_PRELIMIILARY_UL2016PREVFP  = {'label':'Prelimilary', 'data':True , 'lumi':19.52, 'year':'UL2016preVFP' , 'loc':2}
INFO_CMS_PRELIMIILARY_UL2016POSTVFP = {'label':'Prelimilary', 'data':True , 'lumi':16.81, 'year':'UL2016postVFP', 'loc':2}
INFO_CMS_PRELIMIILARY_2022EE        = {'label':'Prelimilary', 'data':True , 'lumi':27.01, 'year':'2022EE'       , 'loc':2, 'com':13.6}
INFO_CMS_PRELIMIILARY_Simulations   = {'label':''           , 'data':False, 'lumi':None , 'year':'Psuedodata'   , 'loc':2, 'com':13.6}

OVERWRITE_XAXIS_LABEL = None ## this value is set from upperpad plotables but affect the x-axis at lowerplot
def DrawContentAtPad(ax, plotobjs,
        xLABEL:str=None, yLABEL:str=None, ySCALE:str=None, yRANGE:tuple=None, **otherargs_notused ):

    global OVERWRITE_XAXIS_LABEL
    for plotidx, plotobj in enumerate(plotobjs):
        plotobj.Draw(ax, plotidx, len(plotobjs))
        if OVERWRITE_XAXIS_LABEL is None: ## only valid in DrawObj_TextLabelTH1F
            OVERWRITE_XAXIS_LABEL = getattr(plotobj, 'x_axislabels', None)

    if xLABEL:
        if OVERWRITE_XAXIS_LABEL:
            labels = OVERWRITE_XAXIS_LABEL() # callback function
            x = np.arange(len(labels))  # The label locations

            ax.set_xticks(x)
            ax.set_xticklabels(labels)
        else:
            ax.set_xlabel(xLABEL)

    if yLABEL:
        yLABEL = yLABEL.replace('\\n','\n')
        if hasattr(plotobjs[0], 'binwidth'):
            yLABEL = f'{yLABEL} [1/{float(plotobjs[0].binwidth):.2f}]'
        ax.set_ylabel(yLABEL)
    yAxisConfigs(ax,yRANGE, ySCALE)
    ax.grid(True, which='major', axis='y')

def yAxisConfigs(ax, yRANGE:tuple=None, ySCALE:str=None):

    user_y_range = [ float(v) for v in yRANGE ] if yRANGE else None
    origylim = ax.get_ylim()
    log.debug(f'[CHECK] yRANGE="{ yRANGE }" and ySCALE="{ ySCALE }"')



    if ySCALE == 'log':
        ax.set_yscale('log')
        if yRANGE:
            if user_y_range[0] < 0: raise ValueError(f'[InvalidYaxisRange] yAxisConfigs() received invalid range "{ user_y_range }" with log scale')
            ax.set_ylim(*user_y_range)
            log.debug(f'[ySCALE] Log using user y_range')
        else:
            ax.set_ylim(origylim[0], origylim[1] * 1e3)
            log.debug(f'[ySCALE] Log using original y_range with additional multiplier * 1e3 at upper')



    if ySCALE == 'linear' or ySCALE is None:
        ax.set_yscale('linear')
        if yRANGE:
            ax.set_ylim(*user_y_range)
            log.debug(f'[ySCALE] Linear using user y_range "{ user_y_range }"')
        else:
            interval = origylim[1]-origylim[0]
            ax.set_ylim( origylim[0], origylim[1] * 1.5 )
            log.debug(f'[ySCALE] Linear using original y_range with additional multiplier * 1.5 at upper')
        ax.yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))




def DrawObjFactory(plotable, commonINPUTfile:str = None):
    Type = plotable['type']
    if commonINPUTfile: ## once common input file put, ignore the original recorded input file
        plotable['file'] = commonINPUTfile
    if Type == DrawObj_TGraphAsymmError.name:
        return DrawObj_TGraphAsymmError(plotable)
    if Type == DrawObj_TH1F            .name:
        return DrawObj_TH1F            (plotable)
    if Type == DrawObj_TextLabelTGraphAsymmError.name:
        return DrawObj_TextLabelTGraphAsymmError(plotable)
    if Type == DrawObj_TextLabelTH1F   .name:
        return DrawObj_TextLabelTH1F   (plotable)
    raise IOError(f'[InvalidType] "{ plotable["type"] }" is an invalid plotable type. Please check yaml file')

def DrawRatioPlotWithCMSFormat(
        upperPLOTABLEs, lowerPLOTABLEs,
        upperCONFIGs, lowerCONFIGs,
        figNAME:str=None,
        dataORmc='mc',
        **otherCONFs
        ):
    upper_plotables = upperPLOTABLEs
    lower_plotables = lowerPLOTABLEs

    hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    hep.style.use("CMS") # string aliases work too
    fig, (ax_upper, ax_lower) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, sharex=True, figsize=(10,8))
    DrawContentAtPad(ax_upper, upper_plotables, **upperCONFIGs)

    reordered_legend_items = sum([ 0 if 'legorder' in plotable else 1 for plotable in reversed(upperCONFIGs['plotables']) ])
    legNcolumn = upperCONFIGs['legNcolumn'] if 'legNcolumn' in upperCONFIGs else 1
    legFONTsize = upperCONFIGs['legFONTsize'] if 'legFONTsize' in upperCONFIGs else 'small'
    legTITLE = upperCONFIGs['legTITLE'] if 'legTITLE' in upperCONFIGs else ''
    legTITLEfontsize = upperCONFIGs['legTITLEfontsize'] if 'legTITLEfontsize' in upperCONFIGs else 'x-small'

    if reordered_legend_items == 0:
        log.info(f'[ReorderedLegend] Use the option "legorder" to arrange items')
        handles, labels = ax_upper.get_legend_handles_labels()
        # Custom order for legend
        ### sort legend order in ascend ordered.
        my_order = { plotable['legorder']: plotable['label'] for plotable in reversed(upperCONFIGs['plotables']) }

        ordered_labels = [ my_order[o] for o in sorted(my_order.keys()) ]
        ordered_handles = [ handles[labels.index(label)] for label in ordered_labels ]

        ax_upper.legend(ordered_handles, ordered_labels, ncol=legNcolumn, fontsize=legFONTsize, title=legTITLE, title_fontsize=legTITLEfontsize)
    else:
        log.info(f'[DefaultLegend] Use default item order.')
        ax_upper.legend(ncol=legNcolumn, fontsize=legFONTsize, title=legTITLE, title_fontsize=legTITLEfontsize)
        #ax_upper.legend()
        #ax.legend(ncol=legNcolumn, fontsize=legFONTsize, title=legTITLE, title_fontsize=legFONTsize)

    DrawContentAtPad(ax_lower, lower_plotables, **lowerCONFIGs)
    ax_lower.axhline(y=1.0, color='gray', linestyle='-', linewidth=0.5)

    if dataORmc == 'data':
        hep.cms.label(ax=ax_upper, **INFO_CMS_PRELIMIILARY_2022EE)
    if dataORmc == 'mc':
        hep.cms.label(ax=ax_upper, **INFO_CMS_PRELIMIILARY_Simulations)

    figname = figNAME
    if figname == '':
        plt.show()
        current_figsize = fig.get_size_inches()
        log.info(f"[AdjustedFigureSize] {current_figsize[0]} inches x {current_figsize[1]} inches")
    else:
        plt.savefig(figname)
        log.info(f'[SavedOutput] {figname}')




if __name__ == "__main__":
    import os
    loglevel = os.environ.get('LOG_LEVEL', 'INFO') # DEBUG, INFO, WARNING
    DEBUG_MODE = True if loglevel == 'DEBUG' else False
    logLEVEL = getattr(logging, loglevel)
   #logging.basicConfig(level=logging.INFO,
    logging.basicConfig( stream=sys.stdout, level=logLEVEL,
            format='[basicCONFIG] %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')
    import yaml
    import sys
    yamlCONFIG = sys.argv[1]
    updated_confs = DrawTools.update_opts(sys.argv[2:] if len(sys.argv)>2 else None)

    with open(yamlCONFIG,'r') as f:
        conf = yaml.safe_load(f)
    DrawTools.update_conf(conf, updated_confs)


    log.info(pformat(conf))


    upper_plotables = [ DrawObjFactory(plotable,conf.get('commonINPUTfile',None)) for plotable in reversed(conf['upperpad']['plotables']) ]
    lower_plotables = [ DrawObjFactory(plotable,conf.get('commonINPUTfile',None)) for plotable in reversed(conf['lowerpad']['plotables']) ]

    DrawRatioPlotWithCMSFormat(
            upper_plotables, lower_plotables,
            conf['upperpad'], conf['lowerpad'],
            **conf)


