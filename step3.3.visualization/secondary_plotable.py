#!/usr/bin/env python3

import ROOT
FILE_IDENTIFIER = 'secondary_plotable.py'
def info(mesg):
    print(f'i-{FILE_IDENTIFIER}@ {mesg}')


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

'''
def TakeRatio_(histNAME, histDICTup, histDICTlow):
    hU = histDICTup [histNAME]
    hL = histDICTlow[histNAME]
    ratio = ROOT.TGraphAsymmErrors()
    ratio.SetName(histNAME)
    ratio.Divide(hU,hL, 'pois')
    return ratio
'''
def WriteHistsToDir(fOUT, dirNAME, histDICT):
    dirout = fOUT.mkdir(dirNAME) if dirNAME else fOUT
    dirout.cd()
    for n,h in histDICT.items():
        h.Write()


if __name__ == "__main__":
    from collections import namedtuple
    inputARGs = namedtuple('InputArgs', 'postfit_file output_file')
    import sys
    io = inputARGs(*sys.argv[1:])
    f = ROOT.TFile.Open(io.postfit_file)
    fout = ROOT.TFile(io.output_file, "RECREATE")

    def record_hist(loadedDIR):
        if not f or f.IsZombie():
            info(f'[InvalidInputs] input root file is broken or not found')
            return
        if not f.GetListOfKeys().Contains(loadedDIR):
            info(f'[SkipFolder] directory "{ loadedDIR }" is skipped because missing folder in root file.')
            return
        hists = interested_hists_in_a_folder(f, loadedDIR)
        WriteHistsToDir(fout, loadedDIR, hists)
        info(f'[Recorded] directory "{ loadedDIR }" recorded')

    record_hist('cvsl_postfit')
    record_hist('btag_postfit')
    record_hist('cvsb_postfit')
    record_hist('gjet_postfit')

    record_hist('SBbtag_postfit')
    record_hist('SBcvsb_postfit')
    record_hist('SBcvsl_postfit')
    record_hist('gjet_inclusive_postfit')



    ### Get hists from Lall folder
    #loadedDir = 'cvsl_postfit'
    #hists = interested_hists_in_a_folder(f, loadedDir)
    #WriteHistsToDir(fout, loadedDir, hists)

    #loadedDir = 'btag_postfit'
    #hists = interested_hists_in_a_folder(f, loadedDir)
    #WriteHistsToDir(fout, loadedDir, hists)

    #loadedDir = 'cvsb_postfit'
    #hists = interested_hists_in_a_folder(f, loadedDir)
    #WriteHistsToDir(fout, loadedDir, hists)

    #loadedDir = 'gjet_postfit'
    #hists = interested_hists_in_a_folder(f, loadedDir)
    #WriteHistsToDir(fout, loadedDir, hists)

    fout.Close()
