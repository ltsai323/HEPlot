#!/usr/bin/env python3
import logging
import ROOT
import sys

log = logging.getLogger(__name__)

def GetShape(f,hNAME, hTITLE, emptyALLOWED=False):
    log.debug(f'[LoadHist] Load hist {hNAME}')
    try:
        h = f.Get(hNAME)
        h.SetTitle(hTITLE)
        h.Scale(1./h.Integral())
        return h
    except AttributeError as e:
        if emptyALLOWED:
            return None
        raise AttributeError(f"\n\n[NoSuchHist] hist {hNAME} doen not exist in root file {f.GetName()}") from e

def TakeRatio(hU, hD, errNAME):
    ge = ROOT.TGraphAsymmErrors()
    ge.SetName(errNAME)
    ge.Divide(hU,hD,'pois')
    return ge

def CalculateChi2(hTEST,hREF) -> float:
    '''
    Calculate chi2 from sum_bin ( (binTEST-binREF)/bin_errTEST )^2
    Such as, ignore uncertainties from hREF and calculate chi2
    '''
    nbin = hTEST.GetNbinsX()
    nbin_= hREF .GetNbinsX()
    if nbin != nbin_: raise IOError(f'[UnmatchedNbins] bin number of hist {hTEST.GetName()}({nbin}) differs from hist {hREF.GetName()}({nbin_})')

    sum_chi2 = float(0)
    while nbin > 0:
        vtest = hTEST.GetBinContent(nbin)
        etest = hTEST.GetBinError  (nbin)
        vref  = hREF .GetBinContent(nbin)
        if etest > 1e-8:
            sum_chi2 += (vtest-vref )**2 / etest**2
        nbin-=1
    return sum_chi2

def TestData():
    return '/Users/noises/Downloads/psuedofit_datacard_cvsl.root', 'test.root', 'gjet_cvsl'
def ArgData():
    iFILE = sys.argv[1]
    oFILE = sys.argv[2]
    return iFILE, oFILE
class HistSource:
    def __init__(self, outTAG, hNAMEref,hNAMEnew,hNAMEold):
        self.otag = outTAG

        self.nref = hNAMEref
        self.nold = hNAMEold
        self.nnew = hNAMEnew

        self.tagref = 'psuedo data'
        self.tagold = 'original MC'
        self.tagnew = 'SF weighted'

        self.ratioold = f'ratio{outTAG}_old'
        self.rationew = f'ratio{outTAG}_new'
    def AccessTFile(self,iFILE) -> list:
        href = GetShape(ifile, hsource.nref, hsource.tagref)
        hold = GetShape(ifile, hsource.nold, hsource.tagold, True)
        hnew = GetShape(ifile, hsource.nnew, hsource.tagnew)

        tag_and_chi2 = lambda tag, chi2, ndof: f'{tag}: {chi2:.1f} / {ndof-1:d}'
        nbinsx = href.GetNbinsX()
        chi2_new = CalculateChi2(hnew,href)
        hnew.SetTitle(tag_and_chi2(hsource.tagnew,chi2_new,nbinsx))
        rationew = TakeRatio(hnew,href, hsource.rationew)

        if hold is None:
            hold = href.Clone(hsource.nold)
            for ibin in range(hold.GetNbinsX()):
                hold.SetBinContent(ibin+1,0)
                hold.SetBinError  (ibin+1,0)
            hold.SetTitle(f'No {hsource.tagold}')
        else:
            chi2_old = CalculateChi2(hold,href)
            hold.SetTitle(tag_and_chi2(hsource.tagold,chi2_old,nbinsx))
        ratioold = TakeRatio(hold,href, hsource.ratioold)

        return [href,hold,hnew, ratioold,rationew]

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout,level=logging.DEBUG,
                        format='[basicCONFIG] %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')

    iFILE, oFILE = ArgData()

    hist_names = [
            HistSource('btagL', 'truthL_gjet_btag','sigL_gjet_btag','sigL_gjet_origweight_btag'),
            HistSource('btagC', 'truthC_gjet_btag','sigC_gjet_btag','sigC_gjet_origweight_btag'),
            HistSource('btagB', 'truthB_gjet_btag','sigB_gjet_btag','sigB_gjet_origweight_btag'),
            HistSource('cvsbL', 'truthL_gjet_cvsb','sigL_gjet_cvsb','sigL_gjet_origweight_cvsb'),
            HistSource('cvsbC', 'truthC_gjet_cvsb','sigC_gjet_cvsb','sigC_gjet_origweight_cvsb'),
            HistSource('cvsbB', 'truthB_gjet_cvsb','sigB_gjet_cvsb','sigB_gjet_origweight_cvsb'),
            HistSource('cvslL', 'truthL_gjet_cvsl','sigL_gjet_cvsl','sigL_gjet_origweight_cvsl'),
            HistSource('cvslC', 'truthC_gjet_cvsl','sigC_gjet_cvsl','sigC_gjet_origweight_cvsl'),
            HistSource('cvslB', 'truthB_gjet_cvsl','sigB_gjet_cvsl','sigB_gjet_origweight_cvsl'),

            HistSource('phopt' , 'kine_data_phopt' , 'kine_gjet_phopt' , 'kine_gjet_origweight_phopt'),
            HistSource('phoeta', 'kine_data_phoeta', 'kine_gjet_phoeta', 'kine_gjet_origweight_phoeta'),
            HistSource('phophi', 'kine_data_phophi', 'kine_gjet_phophi', 'kine_gjet_origweight_phophi'),
            HistSource('jetpt' , 'kine_data_jetpt' , 'kine_gjet_jetpt' , 'kine_gjet_origweight_jetpt'),
            HistSource('jeteta', 'kine_data_jeteta', 'kine_gjet_jeteta', 'kine_gjet_origweight_jeteta'),
            HistSource('jetphi', 'kine_data_jetphi', 'kine_gjet_jetphi', 'kine_gjet_origweight_jetphi'),
            HistSource('njet'  , 'kine_data_njet'  , 'kine_gjet_njet'  , 'kine_gjet_origweight_njet'),
            ]
    loaded_hists = {}


    ifile = ROOT.TFile.Open(iFILE)

    ofile = ROOT.TFile(oFILE, 'recreate')
    ofile.cd()
    for hsource in hist_names:
        rootOBJs = hsource.AccessTFile(ifile)
        for rootOBJ in rootOBJs:
            if rootOBJ:
                log.info(f'[WriteObj] object "{ rootOBJ.GetName() }" written.')
                rootOBJ.Write()
    ofile.Close()
    log.info(f'[WriteFile] file {oFILE} written.')
