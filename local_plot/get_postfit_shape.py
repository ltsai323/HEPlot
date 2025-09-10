#!/usr/bin/env python3
import logging
import ROOT
import sys

log = logging.getLogger(__name__)

def GetShape(h):
    h.Scale(1./h.Integral())

def TakeRatio(hU, hD, errNAME):
    ge = ROOT.TGraphAsymmErrors()
    ge.SetName(errNAME)
    ge.Divide(hU,hD,'pois')
    return ge


def TestData():
    return '/Users/noises/Downloads/psuedofit_datacard_cvsl.root', 'test.root', 'gjet_cvsl'
def ArgData():
    iFILE = sys.argv[1]
    oFILE = sys.argv[2]
    folder = sys.argv[3] if len(sys.argv) > 3 else 'gjet_cvsl'
    return iFILE, oFILE, folder

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout,level=logging.DEBUG,
                        format='[basicCONFIG] %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')

    iFILE, oFILE, folder = ArgData()
    #iFILE, oFILE, folder = TestData()

    hist_names = [
        f'{folder}/data_obs',
        f'{folder}/fake',
        f'{folder}/Ljet',
        f'{folder}/Cjet',
        f'{folder}/Bjet',
        f'{folder}/truthL',
        f'{folder}/truthC',
        f'{folder}/truthB',
    ]
    loaded_hists = {}


    ifile = ROOT.TFile.Open(iFILE)

    ofile = ROOT.TFile(oFILE, 'recreate')
    ofile.cd()
    for hname in hist_names:
        log.debug(f'[LoadHist] Load hist {hname}')
        h = ifile.Get(hname)
        h.Scale(1./h.Integral())
        h.Write()
        log.debug(f'[WriteHist] hist {h.GetName()} written in file\n')

        loaded_hists[h.GetName()] = h

    ratioL = TakeRatio(loaded_hists['Ljet'],loaded_hists['truthL'], 'ratioL')
    ratioC = TakeRatio(loaded_hists['Cjet'],loaded_hists['truthC'], 'ratioC')
    ratioB = TakeRatio(loaded_hists['Bjet'],loaded_hists['truthB'], 'ratioB')
    ratioL.Write()
    ratioC.Write()
    ratioB.Write()
    
    ofile.Close()
    log.info(f'[WriteFile] file {oFILE} written.')
