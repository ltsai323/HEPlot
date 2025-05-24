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
> plotables:
>   - type: TH1F
>     objname: HLTbit7/barrel_ratio
>     file: HLT_AbsTurnOnEff_JetHT_UL2016PostVFP.root
>     label: HLT_PFJetxx
>     plotstyle: test
'''



def DrawHIST(ax, uprootTH1Fobj, label:str, plotSTYLE:str):
    values = uprootTH1Fobj.values()
    bin_edges = uprootTH1Fobj.axis().edges()
    ax.hist(bin_edges[:-1], bins=bin_edges, weights=values, label=label, **VisualizationPresets.PlotStyle(plotSTYLE))
def DrawEP(ax, uprootTH1Fobj, label:str, plotSTYLE:str):
    values = uprootTH1Fobj.values()
    errors = uprootTH1Fobj.errors()
    bin_centers = uprootTH1Fobj.axis().centers()
    bin_errors = uprootTH1Fobj.axis().widths() / 2.
    ax.errorbar( bin_centers, values, xerr=bin_errors, yerr=errors, label=label, **VisualizationPresets.PlotStyle(plotSTYLE))

def highlight_mesg(mesg):
    print('\n\n')
    print('-' * len(mesg))
    print(mesg)
    print('-' * len(mesg))
    print('\n\n')

class DrawObj_TH1F:
    name = 'TH1F'
    def __init__(self, yamlCONFIGs):
        try:
            config = yamlCONFIGs
            self.file = config['file']
            self.objname = config['objname']
            self.label = config['label']
            self.plotstyle = config['plotstyle']
        except KeyError as e:
            mesg = f'Invalid key found in yaml configuration. please check'
            highlight_mesg(mesg)
            raise KeyError(e)
    def __str__(self):
        return f'DrawObj_TH1F({self.objname}, label={self.label})'
    def Draw(self,ax):
        try:
            f = uproot.open(self.file)
            graph_obj = f[self.objname]
        except IOError as e:
            mesg = f'parameter: opened file "{ self.file }" and "{ self.objname }"'
            highlight_mesg(mesg)
            raise IOError(e)
        if 'hist' in self.plotstyle or 'line' in self.plotstyle:
            DrawHIST(ax, graph_obj, self.label, self.plotstyle)
        else:
            DrawEP(ax, graph_obj, self.label, self.plotstyle)

if __name__ == "__main__":
    import yaml
    f = open('test.TH1F.yaml','r')
    configs = yaml.safe_load(f)
    fig,ax = plt.subplots()
    drawobj = DrawObj_TH1F(configs['plotables'][0]) # draw first plotables for test
    drawobj.Draw(ax)

    if 'yRANGE' in configs:
        ax.set_ylim(*configs['yRANGE'])
    if 'yLABEL' in configs:
        ax.set_ylabel(configs['yLABEL'])
    if 'xLABEL' in configs:
        ax.set_xlabel(configs['xLABEL'])

    ax.legend()
    plt.show()
