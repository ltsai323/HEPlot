import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import math
import mplhep as hep
from uncertainties import ufloat, unumpy
import HistSet
from DrawObj_TGraphAsymmError import DrawObj_TGraphAsymmError



INFO_CMS_PRELIMIILARY_UL2016PREVFP  = {'label':'Prelimilary', 'data':True, 'lumi':19.52, 'year':'UL2016preVFP' , 'loc':2}
INFO_CMS_PRELIMIILARY_UL2016POSTVFP = {'label':'Prelimilary', 'data':True, 'lumi':16.81, 'year':'UL2016postVFP', 'loc':2}

### the parameters are used in yaml file.
def DrawPlotablesWithCMSFormat(plotobjs,
                    xLABEL:str=None,
                    yLABEL:str=None, ySCALE:str=None, yRANGE:tuple=None,
                    figNAME:str=None,
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
    if yRANGE: ax.set_ylim(*yRANGE)
    ax.legend()
    plt.suptitle('')
    plt.grid(True, which='major', axis='y')

    hep.cms.label(ax=ax, **INFO_CMS_PRELIMIILARY_UL2016POSTVFP)
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
    if plotable['type'] == DrawObj_TGraphAsymmError.name:
        return DrawObj_TGraphAsymmError(plotable)
    raise IOError(f'[InvalidType] "{ plotable["type"] }" is an invalid plotable type. Please check yaml file')

if __name__ == "__main__":
    import yaml
    import sys
    fIN = GetArgs_InputYAML(sys.argv)

    with open(fIN,'r') as f:
        conf = yaml.safe_load(f)
        # yamlCONF = YAMLConfigs(conf)

    pp = [ DrawObjFactory(plotable) for plotable in reversed(conf['plotables']) ]
    DrawPlotablesWithCMSFormat(pp,**conf)


