import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import math
import mplhep as hep
from uncertainties import ufloat, unumpy
import HistSet

def GetArgs_InputAndOutput(argv):
    if len(argv) == 2:
        return argv[1]
    return 'test.yaml'





INFO_CMS_PRELIMIILARY_UL2016PREVFP  = {'label':'Prelimilary', 'data':True, 'lumi':19.52, 'year':'UL2016preVFP' , 'loc':2}
INFO_CMS_PRELIMIILARY_UL2016POSTVFP = {'label':'Prelimilary', 'data':True, 'lumi':16.81, 'year':'UL2016postVFP', 'loc':2}
def take_ratio(hNUMERATOR:HistSet.HistSet, hDENOMINATOR:HistSet.HistSet) -> tuple:
    ''' Take ratio of two histogram (HistSet). Get the binned value and error '''
    value_numerator = HistSet.GetBinData(hNUMERATOR)
    value_denominator = HistSet.GetBinData(hDENOMINATOR)
    ratio = [ u/d if d != 0 else ufloat(0,0) for u,d in zip(value_numerator,value_denominator) ]

    return ( unumpy.nominal_values(ratio),unumpy.std_devs(ratio) )


def draw_ratio_plot(ax,
                    hNUMERATOR:HistSet.HistSet, hDENOMINATOR:HistSet.HistSet,
                    label:str, drawYerr=False):
    ratio_value, ratio_error = take_ratio(hNUMERATOR,hDENOMINATOR)
    bin_center = HistSet.GetBinCenter(hNUMERATOR)
    bin_width  = HistSet.GetBinWidth(hNUMERATOR)
    
    xVAL = bin_center
    xERR = bin_width

    yVAL = ratio_value
    yERR = ratio_error if drawYerr else None
    ax.errorbar( xVAL, yVAL, xerr=xERR, yerr=yERR, label=label )
    
def trigger_turn_on(listOFdrawableFUNC:list,
                      xLABEL, yLABEL, ySCALE, yRANGE:tuple=(),
                    ):
    '''
        Args:
            listOFdrawableFUNC is a list containing a tuple, first is callback function, the second one is the xargs
            listOFdrawableFUNC = [
                ( func1, xargs1 ),
                ( func2, xargs2 ),
            ]
    '''

    #plt.clf()
    hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    hep.style.use("CMS") # string aliases work too
    fig, ax = plt.subplots(figsize=(8,8))

    for drawbleFUNC, funcPARAMETERdict in listOFdrawableFUNC:
        drawbleFUNC(ax, **funcPARAMETERdict)

    ax.set_xlabel(xLABEL)
    ax.set_ylabel(yLABEL)
    if len(yRANGE):
        ax.set_ylim( yRANGE[0], yRANGE[1] )
    ax.legend()
    plt.suptitle('')
    plt.grid(True, which='major', axis='y')

    hep.cms.label(ax=ax, **INFO_CMS_PRELIMIILARY_UL2016POSTVFP)

    return fig, ax

class DrawableEntry:
    def __init__(self, entry:dict):
        try:
            self.num = entry['num']
            self.den = entry['den']
            self.root = entry['root']
            self.label = entry['label']
        except KeyError as e:
            mesg = f'[DrawableEntry] "num", "den", "root", "label" are required in yaml file'
            print('\n\n' + '*' * len(mesg) )
            print(mesg)
            print('*' * len(mesg) + '\n\n')
            raise KeyError(e)
class YAMLEntry:
    def __init__(self, entry:dict):
        try:
            self.fig_name = entry['figNAME']
            self.y_title = entry['yTITLE']
            self.ratio_plots = [ DrawableEntry(e) for e in entry['ratioPLOTs'] ]
        except KeyError as e:
            mesg = f'[YAMLEntry] "figNAME", "yTITLE", "ratioPLOTs" are required in yaml file'
            print('\n\n' + '*' * len(mesg) )
            print(mesg)
            print('*' * len(mesg) + '\n\n')
            raise KeyError(e)

    def __str__(self):
        return f'Configs for entry "{self.y_title}"'
    def __repr__(self):
        return self.__str__()
def GetYAMLConfigs(yamlFILE):
    '''
    output yaml format with 
    out = [
        { 'figNAME': 'hi.jpg', 'yTITLE': 'test', 
            'ratioPLOTs': [
                { 'num': 'Range7_passingBothJetHLT7', 'den': 'Range7_passingJetHLT', 'label': 'jjj', 'root': 'a.root', },
                { 'num': 'Range7_passingBothJetHLT7', 'den': 'Range7_passingJetHLT', 'label': 'kkk', 'root': 'b.root', },
                ]
        },
        { 'figNAME': 'hi.jpg', 'yTITLE': 'test', 
            'ratioPLOTs': [
                { 'num': 'Range7_passingBothJetHLT7', 'den': 'Range7_passingJetHLT', 'label': 'jjj', 'root': 'a.root', },
                { 'num': 'Range7_passingBothJetHLT7', 'den': 'Range7_passingJetHLT', 'label': 'kkk', 'root': 'b.root', },
                ]
        },
    ]
    '''
    import yaml
    with open(yamlFILE, 'r') as fIN:
        return [ YAMLEntry(entry) for entry in yaml.safe_load(fIN) ]

if __name__ == "__main__":
    import sys
    inFILE = GetArgs_InputAndOutput(sys.argv)
    entries = GetYAMLConfigs( inFILE )
    



# Access the 'expdata' directory
    def getHistSet(tFILE, var, **xargs):
        h = tFILE[var]
        xargs['orig_obj'] = h
        return HistSet.HistSet(h.to_hist(), **xargs)


    fig_configurations = {
            'xLABEL': '$E^{\gamma}_{T}$ (GeV)',
            'yLABEL': 'modification required',
            'ySCALE': 'linear',
            'yRANGE': (0.,1.4),
    }
    for entry in entries:
        drawing_contents = []
        for drawable_entry in entry.ratio_plots:
            rootFILE = uproot.open(drawable_entry.root)
            h_numerator   = getHistSet(rootFILE, drawable_entry.num, desc='aaaaa') # desc need to be removed
            h_denominator = getHistSet(rootFILE, drawable_entry.den, desc='aaaaa')
            drawable_parameters = {
                'hNUMERATOR': h_numerator, 'hDENOMINATOR': h_denominator, 
                'label': drawable_entry.label,
                'drawYerr': False
            }
            drawing_contents.append( (draw_ratio_plot, drawable_parameters) )
            rootFILE.close()

        fig_configurations['yLABEL'] = entry.y_title
        fig, ax = trigger_turn_on( drawing_contents, **fig_configurations)
        figNAME = entry.fig_name
        if figNAME:
            plt.savefig(figNAME)
            print(f'[SavedOutput] {figNAME}')
        else:
            plt.show()
            current_figsize = fig.get_size_inches()
            print(f"[AdjustedFigureSize] {current_figsize[0]} inches x {current_figsize[1]} inches")
        #plt.cla()

