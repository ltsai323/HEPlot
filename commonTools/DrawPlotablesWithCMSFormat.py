#!/usr/bin/env python3

### DrawPlotableWithCMSFormat.py inCONF.yaml dataORmc=mc commonINPUTfile=hi.root xLABEL=asdf
import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import logging
import sys
from pprint import pformat

log = logging.getLogger(__name__)


import math
import mplhep as hep
from uncertainties import ufloat, unumpy
from MyROOTPlotSetup.DrawObj_TGraphAsymmError import DrawObj_TGraphAsymmError
from MyROOTPlotSetup.DrawObj_TH1F             import DrawObj_TH1F
from MyROOTPlotSetup.DrawObj_TextLabelTH1F    import DrawObj_TextLabelTH1F
import DrawTools



INFO_CMS_PRELIMIILARY_2022EE        = {'label':'Prelimilary', 'data':True , 'lumi':27.01, 'year':'2022EE'       , 'loc':2, 'com': 13.6}
INFO_CMS_PRELIMIILARY_Simulations   = {'label':''           , 'data':False, 'lumi':None , 'year':'Psuedodata'   , 'loc':2, 'com':13.6}

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
### the parameters are used in yaml file.
def DrawPlotablesWithCMSFormat(plotobjs,
                    xLABEL:str=None,
                    yLABEL:str=None, ySCALE:str=None, yRANGE:tuple=None,
                    figNAME:str=None,
                    legNcolumn:int=1, legFONTsize:str='small', legTITLE:str='',
                    dataORmc:str='mc',
                    **otherargs_notused
                    ):
    if len(plotobjs) == 0: raise IOError(f'[NothingPlotted] DrawPlotablesWithCMSFormat() got 0 plotobjs')
    hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    hep.style.use("CMS") # string aliases work too
    fig, ax = plt.subplots(figsize=(10,8))

    ax.yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    overwrite_xaxis_label = None
    for plotidx, plotobj in enumerate(plotobjs):
        plotobj.Draw(ax, plotidx, len(plotobjs))
        if overwrite_xaxis_label is None: ## only valid in DrawObj_TextLabelTH1F
            overwrite_xaxis_label = getattr(plotobj, 'x_axislabels', None)

    if overwrite_xaxis_label:
        labels = overwrite_xaxis_label() # callback function
        x = np.arange(len(labels))  # The label locations

        ax.set_xticks(x)
        ax.set_xticklabels(labels)

    if xLABEL: ax.set_xlabel(xLABEL)
    if yLABEL:
        if hasattr(plotobjs[0], 'binwidth'):
            yLABEL = f'{yLABEL} [1/{ str(float(plotobjs[0].binwidth))}]'
        ax.set_ylabel(yLABEL)
    #if yRANGE: ax.set_ylim(*[ float(v) for v in yRANGE ])
    #if ySCALE: ax.set_yscale(ySCALE)
    yAxisConfigs(ax,yRANGE, ySCALE)
    ax.legend(ncol=legNcolumn, fontsize=legFONTsize, title=legTITLE, title_fontsize=legFONTsize)
    plt.suptitle('')
    plt.grid(True, which='major', axis='y')

    if dataORmc == 'data':
        hep.cms.label(ax=ax, **INFO_CMS_PRELIMIILARY_2022EE)
    if dataORmc == 'mc':
        hep.cms.label(ax=ax, **INFO_CMS_PRELIMIILARY_Simulations)
    if figNAME:
        plt.savefig(figNAME)
        log.info(f'[SavedOutput] {figNAME}')
    else:
        plt.show()
        current_figsize = fig.get_size_inches()
        log.info(f"[AdjustedFigureSize] {current_figsize[0]} inches x {current_figsize[1]} inches")


#class YAMLConfigs:
#    def __init__(self, yamlCONFIGs):
#        config = yamlCONFIGs
#        self.figNAME = config['figNAME'] if 'figNAME' in config else None
#        self.yLABEL = config['yLABEL'] if 'yLABEL' in config else None
#        self.yRANGE = config['yRANGE'] if 'yRANGE' in config else None
#        self.xLABEL = config['xLABEL'] if 'xLABEL' in config else None
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



if __name__ == "__main__":
    import os
    loglevel = os.environ.get('LOG_LEVEL', 'INFO') # DEBUG, INFO, WARNING
    DEBUG_MODE = True if loglevel == 'DEBUG' else False
    logLEVEL = getattr(logging, loglevel)
    logging.basicConfig(stream=sys.stdout,level=logLEVEL,
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

    pp = [ DrawObjFactory(plotable,conf.get('commonINPUTfile',None)) for plotable in reversed(conf['plotables']) ]
    DrawPlotablesWithCMSFormat(pp,**conf)
