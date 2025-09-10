import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import math
import mplhep as hep
from uncertainties import ufloat, unumpy
import MyROOTPlotSetup.VisualizationPresets as VisualizationPresets


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

def DrawEP(ax, graphOBJ, label:str, plotSTYLE:str, plotIDX:int=0, lenPLOTABLEs:int=0):
    bin_center, bin_content = GetAsymXY(graphOBJ)
    x_err, y_err = GetAsymErrXY(graphOBJ)

    print(x_err)
    x_err0 = x_err[0] * float(lenPLOTABLEs) / float(lenPLOTABLEs+1)

    print(f'bin center {bin_center}')
    print(f'x_err {x_err}')
    print(f'y_err {y_err}')
    new_bin_center = bin_center - x_err[0]
    ax.errorbar( new_bin_center, bin_content, xerr=x_err0, yerr=y_err, label=label, **VisualizationPresets.PlotStyle(plotSTYLE))
# Create a ratio plot function

class DrawObj_TextLabelTGraphAsymmError:
    name = 'TextLabelTGraphAsymmError'
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
    def __str__(self):
        return f'DrawObj_TextLabelTGraphAsymmError({self.objname}, label={self.label})'
    def Draw(self,ax, plotIDX=0, lenPLOTABLEs=0):
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
        ### not sure it raising bug or not
        DrawEP(ax, graph_obj, self.label, self.plotstyle, plotIDX, lenPLOTABLEs)

        #### newer code.
        # def allowed_plotstyle(plotSTYLE, *predefinedSTYLEs):
        #     for predefined_style in predefinedSTYLEs:
        #         if predefined_style in plotSTYLE: return True
        #     return False

        # if allowed_plotstyle(self.plotstyle, 'nostackb'):
        #     return DrawNOSTACKb(ax, graph_obj, self.label, self.plotstyle, plotIDX, lenPLOTABLEs)
        # if allowed_plotstyle(self.plotstyle, 'hist', 'line'):
        #     return DrawHIST(ax, graph_obj, self.label, self.plotstyle, plotIDX, lenPLOTABLEs)
        # if allowed_plotstyle(self.plotstyle, 'data', 'square', 'diamond', 'cross', 'star', 'test'):
        #     return DrawEP(ax, graph_obj, self.label, self.plotstyle, plotIDX, lenPLOTABLEs)
        # raise IOError(f'[InvalidPlotStyle] DrawObj_TH1F does not support plot style "{ self.plotstyle }"')

if __name__ == "__main__":
    import yaml
    f = open('data/EG90.yaml','r')
    configs = yaml.safe_load(f)
    fig,ax = plt.subplots()
    drawobj = DrawObj_TextLabelTGraphAsymmError(configs['plotables'][0]) # draw first plotables for test
    drawobj.Draw(ax)

    if 'yRANGE' in configs:
        ax.set_ylim(*configs['yRANGE'])
    if 'yLABEL' in configs:
        ax.set_ylabel(configs['yLABEL'])
    if 'xLABEL' in configs:
        ax.set_xlabel(configs['xLABEL'])

    ax.legend()
    plt.show()
