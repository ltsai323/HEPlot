#!/usr/bin/env python3

import ROOT

def create_normalized_hists(inFILE, dirNAME):
    inFOLDER = inFILE.Get(dirNAME)
    all_hists = {}
    all_hists['bS'] = inFOLDER.Get('DeepFlavour_bScore')
    all_hists['CL'] = inFOLDER.Get('DeepFlavour_CvsL')
    all_hists['CB'] = inFOLDER.Get('DeepFlavour_CvsB')

    def _norm_hists(theDICT, name):
        newobj = theDICT[name].Clone()
        newobj.SetName( 'norm'+newobj.GetName() )
        newobj.Scale( 1./newobj.Integral() )
        theDICT['n'+name] = newobj
    _norm_hists(all_hists, 'bS')
    _norm_hists(all_hists, 'CL')
    _norm_hists(all_hists, 'CB')
    return all_hists

def TakeRatio(histNAME, histDICTup, histDICTlow):
    hU = histDICTup[histNAME]
    hL = histDICTlow[histNAME]
    ratio = ROOT.TGraphAsymmErrors()
    ratio.SetName(histNAME)
    ratio.Divide(hU,hL, 'pois')
    return ratio
def WriteHistsToDir(fOUT, dirNAME, histDICT):
    dirout = fOUT.mkdir(dirNAME)
    dirout.cd()
    for n,h in histDICT.items():
        h.Write()


if __name__ == "__main__":
    f = ROOT.TFile.Open("sigMC.cjet_sideban.root")

    fout = ROOT.TFile("secondary_plotable.root", "RECREATE")
    loadedDir = 'Lall'
    histL = create_normalized_hists(f, loadedDir)
    WriteHistsToDir(fout, loadedDir, histL)

    loadedDir = 'Call'
    histC = create_normalized_hists(f, loadedDir)
    WriteHistsToDir(fout, loadedDir, histC)
    
    loadedDir = 'Ball'
    histB = create_normalized_hists(f, loadedDir)
    WriteHistsToDir(fout, loadedDir, histB)
    
    ## write futher calculated objects
    fout.cd()
    ratio_C_L = {}
    ratio_C_L['bS'] = TakeRatio('nbS', histC, histL)
    ratio_C_L['CL'] = TakeRatio('nCL', histC, histL)
    ratio_C_L['CB'] = TakeRatio('nCB', histC, histL)

    for n,h in ratio_C_L.items():
        h.SetName('ratioC_L__'+n)
        h.Write()

    
    fout.Close()
