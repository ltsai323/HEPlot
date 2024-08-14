import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import math
import mplhep as hep
from uncertainties import ufloat, unumpy
import HistSet





INFO_CMS_PRELIMIILARY_UL2016PREVFP  = {'label':'Prelimilary', 'data':True, 'lumi':19.52, 'year':'UL2016preVFP' , 'loc':2}
INFO_CMS_PRELIMIILARY_UL2016POSTVFP = {'label':'Prelimilary', 'data':True, 'lumi':16.81, 'year':'UL2016postVFP', 'loc':2}
def take_ratio(hNUMERATOR:HistSet.HistSet, hDENOMINATOR:HistSet.HistSet) -> tuple:
    ''' Take ratio of two histogram (HistSet). Get the binned value and error '''
    value_numerator = HistSet.GetBinData(hNUMERATOR)
    value_denominator = HistSet.GetBinData(hDENOMINATOR)
    ratio = [ u/d if d != 0 else ufloat(0,0) for u,d in zip(value_numerator,value_denominator) ]

    my_ratio = []
    my_ratio_err = []
    #for u,d in zip(value_numerator, value_denominator):
    #    vu = u.nominal_value
    #    eu = u.std_dev
    #    vd = d.nominal_value
    #    ed = d.std_dev
    #    my_ratio.append(vu/vd)
    #    #my_ratio_err.append( 
        
    return ( unumpy.nominal_values(ratio),unumpy.std_devs(ratio) )

def trigger_turn_on(hNUMERATOR:HistSet.HistSet, hDENOMINATOR:HistSet.HistSet,
                    xLABEL, yLABEL, ySCALE
                    ):
    hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    hep.style.use("CMS") # string aliases work too
    fig, ax = plt.subplots(figsize=(8,8))

    ratio_value, ratio_error = take_ratio(hNUMERATOR,hDENOMINATOR)
    bin_center = HistSet.GetBinCenter(hNUMERATOR)
    bin_width  = HistSet.GetBinWidth(hNUMERATOR)

    #ax.errorbar( bin_center, ratio_value, xerr=bin_width, yerr=ratio_error, label=hNUMERATOR.desc, **HistSet.PLOTSTYLE_STAR1 )
    ### trigger turn on plot do not contains statistic uncertainties
    ax.errorbar( bin_center, ratio_value, xerr=bin_width, label=hNUMERATOR.desc, **HistSet.PLOTSTYLE_DATA )
    ax.set_xlabel(xLABEL)
    ax.set_ylabel(yLABEL)
    ax.set_ylim(0.,1.4)
    ax.legend()
    plt.suptitle('')
    plt.grid(True, which='major', axis='y')

    hep.cms.label(ax=ax, **INFO_CMS_PRELIMIILARY_UL2016POSTVFP)

if __name__ == "__main__":

# Open the ROOT file
    file = uproot.open("result.root")

# Access the 'expdata' directory
    def getHistSet(tFILE, var, **xargs):
        h = tFILE[var]
        xargs['orig_obj'] = h
        return HistSet.HistSet(h.to_hist(), **xargs)

    absolute = [
            #{ 'num': 'Range0_passingBothJetHLT0','den': 'Range0_passingJetHLT', 'yTITLE':'Efficiency of jjjj', },
            #{ 'num': 'Range1_passingBothJetHLT1','den': 'Range1_passingJetHLT', 'yTITLE':'Efficiency of linear', },
            #{ 'num': 'Range2_passingBothJetHLT2','den': 'Range2_passingJetHLT', 'yTITLE':'Efficiency of linear', },
            #{ 'num': 'Range3_passingBothJetHLT3','den': 'Range3_passingJetHLT', 'yTITLE':'Efficiency of linear', },
            #{ 'num': 'Range4_passingBothJetHLT4','den': 'Range4_passingJetHLT', 'yTITLE':'Efficiency of linear', },
            #{ 'num': 'Range5_passingBothJetHLT5','den': 'Range5_passingJetHLT', 'yTITLE':'Efficiency of HLT_Photon125', },
            #{ 'num': 'Range6_passingBothJetHLT6','den': 'Range6_passingJetHLT', 'yTITLE':'Efficiency of HLT_Photon150', },
            { 'num': 'Range7_passingBothJetHLT7','den': 'Range7_passingJetHLT', 'yTITLE':'Efficiency of HLT_Photon175', },
            #{ 'num': 'Range8_passingBothJetHLT7','den': 'Range8_passingJetHLT', 'yTITLE':'Efficiency of HLT_Photon175', },
            ]
    var_looping_info = [
            #{ 'num': 'Range0_passingBothJetHLT0','den': 'Range0_passingJetHLT', 'yTITLE':'Efficiency of jjjj', },
            #{ 'num': 'Range1_passingBothJetHLT1','den': 'Range1_passingJetHLT', 'yTITLE':'Efficiency of linear', },
            #{ 'num': 'Range2_passingBothJetHLT2','den': 'Range2_passingJetHLT', 'yTITLE':'Efficiency of linear', },
            #{ 'num': 'Range3_passingBothJetHLT3','den': 'Range3_passingJetHLT', 'yTITLE':'Efficiency of linear', },
            #{ 'num': 'Range4_passingBothJetHLT4','den': 'Range4_passingJetHLT', 'yTITLE':'Efficiency of linear', },
            #{ 'num': 'Range5_passingBothJetHLT5','den': 'Range5_passingJetHLT', 'yTITLE':'Efficiency of HLT_Photon125', },
            #{ 'num': 'Range6_passingBothJetHLT6','den': 'Range6_passingJetHLT', 'yTITLE':'Efficiency of HLT_Photon150', },
            { 'num': 'Range7_passingBothJetHLT7','den': 'Range7_passingJetHLT', 'yTITLE':'Efficiency of HLT_Photon175', },
            #{ 'num': 'Range8_passingBothJetHLT7','den': 'Range8_passingJetHLT', 'yTITLE':'Efficiency of HLT_Photon175', },
            ]

    for var_info in var_looping_info:
        h_numerator   = getHistSet(file, var_info['num'], desc='Jet HT')
        h_denominator = getHistSet(file, var_info['den'])
        trigger_turn_on(h_numerator, h_denominator,
            xLABEL='$p_{T}^{\gamma}$', yLABEL=var_info['yTITLE'], ySCALE='linear'
        )
        figNAME = var_info.get('figNAME','')
        if figNAME:
            ple.savefig(figNAME)
            print(f'[SavedOutput] {figNAME}')
        else:
            plt.show()
            current_figsize = fig.get_size_inches()
            print(f"[AdjustedFigureSize] {current_figsize[0]} inches x {current_figsize[1]} inches")
