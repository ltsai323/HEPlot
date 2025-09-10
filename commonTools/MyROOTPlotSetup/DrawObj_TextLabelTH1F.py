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



def DrawHIST(ax, uprootTH1Fobj, label:str, plotSTYLE:str, plotIDX:int=0, lenPLOTABLEs:int=0):
    values = uprootTH1Fobj.values()
    bin_edges = uprootTH1Fobj.axis().edges()
    ax.hist(bin_edges[:-1], bins=bin_edges, weights=values, label=label, **VisualizationPresets.PlotStyle(plotSTYLE))
def DrawEP(ax, uprootTH1Fobj, label:str, plotSTYLE:str, plotIDX:int=0, lenPLOTABLEs:int=0):
    values = uprootTH1Fobj.values()
    errors = uprootTH1Fobj.errors()
    bin_centers = uprootTH1Fobj.axis().centers()
    bin_errors = uprootTH1Fobj.axis().widths() / 2.
    ax.errorbar( bin_centers, values, xerr=bin_errors, yerr=errors, label=label, **VisualizationPresets.PlotStyle(plotSTYLE))
#def DrawNOSTACKb(ax, uprootTH1Fobj, label:str, plotSTYLE:str, plotIDX:int=0, lenPLOTABLEs:int=0):
#    values = uprootTH1Fobj.values()
#    bin_edges = uprootTH1Fobj.axis().edges()
#    bin_widths = np.diff(bin_edges) / float(2+lenPLOTABLEs)
#    shifted_idx = float( 1+plotIDX )
#
#    bin_centers = bin_edges[:-1] + 0.5 * bin_widths
#    shifted_bin_centers = bin_centers + shifted_idx * bin_widths
#
#    ### ax.bar treats bin_edge as center.
#    #ax.hist(bin_edges[:-1], bins=bin_edges, weights=values, label=label, **VisualizationPresets.PlotStyle(plotSTYLE))
#    ax.bar(shifted_bin_centers, values, bin_widths, label=label, yerr=[0], **VisualizationPresets.PlotStyle(plotSTYLE))
def DrawNOSTACKb(ax, uprootTH1Fobj, label:str, plotSTYLE:str, plotIDX:int=0, lenPLOTABLEs:int=0):
    values = uprootTH1Fobj.values()
    errors = uprootTH1Fobj.errors()
    bin_edges = uprootTH1Fobj.axis().edges()
    bin_widths = np.diff(bin_edges) / float(2+lenPLOTABLEs)
    shifted_idx = float( 1+plotIDX-float( (2+lenPLOTABLEs)/2.) )

    bin_centers = bin_edges[:-1] + 0.5 * bin_widths
    shifted_bin_centers = bin_centers + shifted_idx * bin_widths

    ### ax.bar treats bin_edge as center.
    #ax.hist(bin_edges[:-1], bins=bin_edges, weights=values, label=label, **VisualizationPresets.PlotStyle(plotSTYLE))
    ax.bar(shifted_bin_centers, values, bin_widths, label=label, yerr=errors, **VisualizationPresets.PlotStyle(plotSTYLE))
    #ax.errorbar(shifted_bin_centers, values, yerr=errors, label=label, **VisualizationPresets.PlotStyle(plotSTYLE))

def highlight_mesg(mesg):
    print('\n\n')
    print('-' * len(mesg))
    print(mesg)
    print('-' * len(mesg))
    print('\n\n')

class DrawObj_TextLabelTH1F:
    name = 'TextLabelTH1F'
    def __init__(self, yamlCONFIGs):
        try:
            config = yamlCONFIGs
            self.file = config['file']
            self.objname = config['objname']
            self.label = config['label']
            self.plotstyle = config['plotstyle']
            self.x_axislabels = None
        except KeyError as e:
            mesg = f'Invalid key found in yaml configuration. please check'
            highlight_mesg(mesg)
            raise KeyError(e)
    def __str__(self):
        return f'DrawObj_TH1F({self.objname}, label={self.label})'
    def Draw(self,ax, plotIDX=0, lenPLOTABLEs=0):
        try:
            f = uproot.open(self.file)
            graph_obj = f[self.objname]
            #self.x_axislabels = [ graph_obj.GetXaxis().GetBinLabel(idx+1) for idx in graph_obj.GetNbinsX() ] ## only valid for pyROOT, instead of uproot
            self.x_axislabels = getattr(graph_obj.axes[0], "labels", None)
        except IOError as e:
            mesg = f'parameter: opened file "{ self.file }" and "{ self.objname }"'
            highlight_mesg(mesg)
            raise IOError(e)

        def allowed_plotstyle(plotSTYLE, *predefinedSTYLEs):
            for predefined_style in predefinedSTYLEs:
                if predefined_style in plotSTYLE: return True
            return False

        if allowed_plotstyle(self.plotstyle, 'nostackb'):
            return DrawNOSTACKb(ax, graph_obj, self.label, self.plotstyle, plotIDX, lenPLOTABLEs)
        if allowed_plotstyle(self.plotstyle, 'hist', 'line'):
            return DrawHIST(ax, graph_obj, self.label, self.plotstyle, plotIDX, lenPLOTABLEs)
        if allowed_plotstyle(self.plotstyle, 'data', 'square', 'diamond', 'cross', 'star', 'test'):
            return DrawEP(ax, graph_obj, self.label, self.plotstyle, plotIDX, lenPLOTABLEs)
        raise IOError(f'[InvalidPlotStyle] DrawObj_TH1F does not support plot style "{ self.plotstyle }"')

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
