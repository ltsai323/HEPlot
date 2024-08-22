import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import math
import mplhep as hep
from uncertainties import ufloat, unumpy
import VisualizationPresets


'''
YAML content
  plotables:
    - objname: HLTbit7/barrel_ratio
      file: HLT_AbsTurnOnEff_JetHT_UL2016PostVFP.root
      label: HLT_PFJetxx
      plotstyle: test
'''


def GetAsymErrXY(graphOBJ:uproot.models.TGraph.Model_TGraphAsymmErrors_v3):
    errLx, errLy = graphOBJ.errors('low')
    errHx, errHy = graphOBJ.errors('high')
    errX = [errLx,errHx]
    errY = [errLy,errHy]
    return [errX,errY]
def GetAsymXY(graphOBJ:uproot.models.TGraph.Model_TGraphAsymmErrors_v3):
    pointX, pointY = graphOBJ.values()
    return [pointX, pointY]

def DrawEP(ax, graphOBJ, label:str, plotSTYLE:str):
    bin_center, bin_content = GetAsymXY(graphOBJ)
    x_err, y_err = GetAsymErrXY(graphOBJ)
    ax.errorbar( bin_center, bin_content, xerr=x_err, yerr=y_err, label=label, **VisualizationPresets.PlotStyle(plotSTYLE))
# Create a ratio plot function

class DrawObj_TGraphAsymmError:
    name = 'TGraphAsymmError'
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
            graph_obj = f[self.objname]
        except IOError as e:
            mesg = f'parameter: opened file "{ self.file }" and "{ self.objname }"'
            print('\n\n')
            print('-' * len(mesg))
            print(mesg)
            print('-' * len(mesg))
            print('\n\n')
            raise IOError(e)
        DrawEP(ax, graph_obj, self.label, self.plotstyle)

if __name__ == "__main__":
    import yaml
    f = open('newinput.yaml','r')
    configs = yaml.safe_load(f)
    fig,ax = plt.subplots()
    drawobj = DrawObj_TGraphAsymmError(configs['plotables'][0])
    drawobj.Draw(ax)

    if 'yRANGE' in configs:
        ax.set_ylim(*configs['yRANGE'])
    if 'yLABEL' in configs:
        ax.set_ylabel(configs['yLABEL'])
    if 'xLABEL' in configs:
        ax.set_xlabel(configs['xLABEL'])

    ax.legend()
    plt.show()
