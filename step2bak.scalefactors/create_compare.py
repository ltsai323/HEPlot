#!usr/bin/env python3

import ROOT
from array import array

def take_ratio_tgraphasymmerrors(gerrCOMP, gerrORIG):
    if gerrCOMP.GetN() != gerrORIG.GetN():
        raise IOError(f'[InvalidBinning] total number of bins of {gerrCOMP.GetName()}={gerrCOMP.GetN()} and {gerrORIG.GetName()}={gerrORIG.GetN()} are different.')
    nbins = gerrCOMP.GetN()

    xarr = [ gerrORIG.GetPointX(ibin) for ibin in range(nbins) ]
    yarr_orig = ( gerrORIG.GetPointY(ibin) for ibin in range(nbins) )
    yarr_comp = ( gerrCOMP.GetPointY(ibin) for ibin in range(nbins) )

    yarr_ratio = [ vcomp / vorig for vcomp,vorig in zip(yarr_comp,yarr_orig) ]

    emptyval = [0] * nbins
    o = ROOT.TGraphAsymmErrors( nbins, array('f',xarr), array('f',yarr_ratio) )
    return o
    



def CreateHist_across_file(hNAME, inFILEcomp, inFILEorig):
    ifileO = ROOT.TFile.Open(inFILEorig)
    horig = ifileO.Get(hNAME)
    horig.SetName('horig')

    ifileC = ROOT.TFile.Open(inFILEcomp)
    hcomp = ifileC.Get(hNAME)
    hcomp.SetName('hcomp')
    print(hcomp.GetName())

    thediff = take_ratio_tgraphasymmerrors(hcomp, horig)
    thediff.SetName('hdiff')


    ofile = ROOT.TFile('create_compare.root', 'recreate')
    ofile.cd()
    horig.Write()
    hcomp.Write()
    thediff.Write()
    print(f'[ROOT genearted] {ofile.GetName()} exported')
    ofile.Close()
def CreateHist(inFILE, hNAMEcomp, hNAMEorig):
    ifile = ROOT.TFile.Open(inFILE)
    horig = ifile.Get(hNAMEorig)
    horig.SetName('horig')

    hcomp = ifile.Get(hNAMEcomp)
    hcomp.SetName('hcomp')
    print(hcomp.GetName())

    thediff = take_ratio_tgraphasymmerrors(hcomp, horig)
    thediff.SetName('hdiff')


    ofile = ROOT.TFile('create_compare.root', 'recreate')
    ofile.cd()
    horig.Write()
    hcomp.Write()
    thediff.Write()
    print(f'[ROOT genearted] {ofile.GetName()} exported')
    ofile.Close()



if __name__ == "__main__":
    import sys
    #inFILE, hNAMEcomp, hNAMEorig = sys.argv[1:]
    #print(inFILE, hNAMEcomp, hNAMEorig)
    #CreateHist(inFILE, hNAMEcomp, hNAMEorig)

    hNAME, fORIG, fCOMP = sys.argv[1:]
    CreateHist_across_file(hNAME, fCOMP, fORIG)
    
