#!/usr/bin/env python3

import ROOT

def TakeRatio(outHISTname, hUPPER, hLOWER):
    hU = hUPPER
    hL = hLOWER
    ratio = ROOT.TGraphAsymmErrors()
    ratio.SetName(outHISTname)
    ratio.Divide(hU,hL, 'pois')
    return ratio
def interested_hists_in_a_folder(inFILE, dirNAME):
    def h(DICT, newNAME, inHIST):
        inHIST.SetName(newNAME)
        DICT[newNAME] = inHIST
    inFOLDER = inFILE.Get(dirNAME)
    all_hists = {}
    h(all_hists,'ljet', inFOLDER.Get('ljet') )
    h(all_hists,'cjet', inFOLDER.Get('cjet') )
    h(all_hists,'bjet', inFOLDER.Get('bjet') )
    h(all_hists,'data', inFOLDER.Get('data_obs') )
    h(all_hists,'fit' , inFOLDER.Get('TotalProcs') )
    h(all_hists,'sign', inFOLDER.Get('TotalSig') )

    def calculate_norm_hist(theDICT, name):
        newobj = theDICT[name].Clone()
        newobj.SetName( 'norm'+newobj.GetName() )
        newobj.Scale( 1./newobj.Integral() )
        theDICT['n'+name] = newobj
    #calculate_norm_hist(all_hists, 'btag')
    #calculate_norm_hist(all_hists, 'CvsL')
    #calculate_norm_hist(all_hists, 'CvsB')
    all_hists['fit_ratio'] = TakeRatio('fit_ratio', all_hists['data'], all_hists['fit'])
    all_hists['fit_ratio'].GetYaxis().SetTitle('data/MC')
    return all_hists

def TakeRatio_(histNAME, histDICTup, histDICTlow):
    hU = histDICTup [histNAME]
    hL = histDICTlow[histNAME]
    ratio = ROOT.TGraphAsymmErrors()
    ratio.SetName(histNAME)
    ratio.Divide(hU,hL, 'pois')
    return ratio
def WriteHistsToDir(fOUT, dirNAME, histDICT):
    dirout = fOUT.mkdir(dirNAME) if dirNAME else fOUT
    dirout.cd()
    for n,h in histDICT.items():
        h.Write()


if __name__ == "__main__":
    f = ROOT.TFile.Open("postfit.root")
    fout = ROOT.TFile("secondary_plotable.root", "RECREATE")


    ## Get hists from Lall folder
    loadedDir = 'cvsl_postfit'
    histL = interested_hists_in_a_folder(f, loadedDir)
    WriteHistsToDir(fout, loadedDir, histL)


    ## write futher calculated objects
    #fout.cd()
    #ratio_C_L = {}
    #ratio_C_L['btag'] = TakeRatio_('nbtag', histC, histL)
    #ratio_C_L['CvsL'] = TakeRatio_('nCvsL', histC, histL)
    #ratio_C_L['CvsB'] = TakeRatio_('nCvsB', histC, histL)

    #for n,h in ratio_C_L.items():
    #    h.SetName('ratioCoverL__'+n)
    #    h.Write()


    fout.Close()
