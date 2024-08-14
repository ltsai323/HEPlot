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

def trigger_turn_on(hNUMERATOR:HistSet.HistSet, hDENOMINATOR:HistSet.HistSet,
                    xLABEL, yLABEL, ySCALE, figNAME:str=''
                    ):
    hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    hep.style.use("CMS") # string aliases work too
    fig, ax = plt.subplots(figsize=(8,8))

    ratio_value, ratio_error = take_ratio(hNUMERATOR,hDENOMINATOR)
    bin_center = HistSet.GetBinCenter(hNUMERATOR)
    bin_width  = HistSet.GetBinWidth(hNUMERATOR)

    ax.errorbar( bin_center, ratio_value, xerr=bin_width, yerr=ratio_error, label=hNUMERATOR.desc, **HistSet.PLOTSTYLE_STAR1 )
    ax.set_xlabel(xLABEL)
    ax.set_ylabel(yLABEL)
    ax.set_ylim(0.,1.4)
    ax.legend()
    plt.suptitle('')
    plt.grid(True, which='major', axis='y')

    hep.cms.label(ax=ax, **INFO_CMS_PRELIMIILARY_UL2016POSTVFP)
    if figNAME:
        ple.savefig(figNAME)
        print(f'[SavedOutput] {figNAME}')
    else:
        plt.show()
        current_figsize = fig.get_size_inches()
        print(f"[AdjustedFigureSize] {current_figsize[0]} inches x {current_figsize[1]} inches")
def draw_raw_distribution(hNUMERATOR:HistSet.HistSet, hDENOMINATOR:HistSet.HistSet,
                    xLABEL, yLABEL, ySCALE, figNAME:str=''
                    ):
    hep.style.use(hep.style.ROOT) # For now ROOT defaults to CMS
    hep.style.use("CMS") # string aliases work too
    fig, ax = plt.subplots(figsize=(8,8))

    bin_center = HistSet.GetBinCenter(hNUMERATOR)
    bin_width  = HistSet.GetBinWidth(hNUMERATOR)

    valU = HistSet.GetBinData(hNUMERATOR)
    bincontent_U = unumpy.nominal_values(valU)
    binerror_U = unumpy.std_devs(valU)
    valD = HistSet.GetBinData(hDENOMINATOR)
    bincontent_D = unumpy.nominal_values(valD)
    binerror_D = unumpy.std_devs(valD)
    #bincontent_U, binerror_U = HistSet.GetBinData(hNUMERATOR)
    #bincontent_D, binerror_D = HistSet.GetBinData(hDENOMINATOR)

    new_bincontent_U = [ vv+10 for vv in bincontent_U ]
    ax.errorbar( bin_center, bincontent_U, xerr=bin_width, yerr=binerror_U, label=hNUMERATOR.desc  , **HistSet.PLOTSTYLE_STAR1 )
    ax.errorbar( bin_center, bincontent_D, xerr=bin_width, yerr=binerror_D, label=hDENOMINATOR.desc, **HistSet.PLOTSTYLE_DIAMOND1)
    ax.errorbar( bin_center, new_bincontent_U, xerr=bin_width, yerr=binerror_U, label=hNUMERATOR.desc  , **HistSet.PLOTSTYLE_DATA)
    ax.set_xlabel(xLABEL)
    ax.set_ylabel(yLABEL)
    #ax.set_ylim(0.,1.4)
    ax.legend()
    plt.suptitle('')
    plt.grid(True, which='major', axis='y')

    hep.cms.label(ax=ax, **INFO_CMS_PRELIMIILARY_UL2016POSTVFP)
    if figNAME:
        ple.savefig(figNAME)
        print(f'[SavedOutput] {figNAME}')
    else:
        plt.show()
        current_figsize = fig.get_size_inches()
        print(f"[AdjustedFigureSize] {current_figsize[0]} inches x {current_figsize[1]} inches")

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
        h_numerator   = getHistSet(file, var_info['num'], desc='JetHLT $\cap$ Photon175')
        h_denominator = getHistSet(file, var_info['den'], desc='JetHLT')
        draw_raw_distribution(h_numerator, h_denominator,
            xLABEL='$p_{T}^{\gamma}$', yLABEL='entries', ySCALE='linear'
        )


