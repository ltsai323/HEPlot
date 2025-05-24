#!/usr/bin/env python3

import ROOT


#dataFILE = '/data4/ltsai/ProducedFiles/2022EE/ZJet/stage2_ZJetData.root'
#signFILE = '/data4/ltsai/ProducedFiles/2022EE/ZJet/stage2_ZJetMC_DYto2L2Jets.root'
dataFILE = '/home/ltsai/stage2_ZJetData.root'
signFILE = '/home/ltsai/stage2_ZJetMC_DYto2L2Jets_MLL50_0to2J.root'
#dataFILE = '/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_ZJet/stage2/stage2_ZJetData.root'
#signFILE = '/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_ZJet/stage2/stage2_ZJetMC_DYto2L2Jets_MLL50_0to2J.root'
outputFILE = 'output.root'

class histCollection:
    def __init__(self):
        pass
    def WriteAllHists(self, fOUT):
        fOUT.cd()
        for hname, hinst in vars(self).items():
            hinst.Write()


def normhist(hist):
    newhist = hist.Clone()
    newhist.SetName( hist.GetName() + '_norm' )
    newhist.Scale(1./hist.Integral())
    return newhist
def TakeRatio(outHISTname, hUPPER, hLOWER):
    hU = hUPPER
    hL = hLOWER
    for ibin in range(1,hL.GetNbinsX()+2):
        if hL.GetBinContent(ibin) == 0: hL.SetBinContent(ibin, 1e-8)
    ratio = ROOT.TGraphAsymmErrors()
    ratio.SetName(outHISTname)
    ratio.Divide(hU,hL, 'pois')
    return ratio

def TakeNormedRatio(outHISTname, hUPPER, hLOWER):
    hU = hUPPER.Clone()
    hL = hLOWER.Clone()
    hU.SetName( hU.GetName() + '_norm' )
    hL.SetName( hL.GetName() + '_norm' )
    hU.Scale( 1./hU.Integral() )
    hL.Scale( 1./hL.Integral() )
    return TakeRatio(outHISTname, hU, hL)

def take_ratio_in_obj(obj, insU:str, insD:str, ratioNAME):
    hU = getattr(obj,insU)
    hD = getattr(obj,insD)
    print(type(hU))
    print(type(hD))
    ratio = TakeRatio(ratioNAME, hU.GetValue(), hD.GetValue())
    setattr(obj,ratioNAME, ratio)



if __name__ == "__main__":
    the_data = ROOT.RDataFrame('Events', dataFILE)
    the_sign = ROOT.RDataFrame('Events', signFILE)
    df__sign = the_sign.Define("event_weight_no_PUw", "integrated_luminosity * genWeight * cross_section / integrated_gen_weight")

    #out_file = ROOT.TFile(outputFILE, 'RECREATE')
    hists = histCollection()
    canv = ROOT.TCanvas("c","",500,500)


    binz = lambda hNAME: (hNAME, 'Z mass', 40, 90-30,90+30)
    hists.data_zmass = the_data.Histo1D( binz('data_zmass'), 'recoZ_mass')
    hists.sign_zmass = df__sign.Histo1D( binz('sign_zmass'), 'recoZ_mass', 'event_weight')
    #hists.data_zmassF= the_data.Histo1D( autobin('data_zmassF'), 'recoZ_mass')
    #hists.sign_zmassF= df__sign.Histo1D( autobin('sign_zmassF'), 'recoZ_mass', 'event_weight')
    take_ratio_in_obj(hists, 'data_zmass', 'sign_zmass', 'ratio_zmass')
    #take_ratio_in_obj(hists, 'data_zmassF', 'sign_zmassF', 'ratio_zmassF')

    binpt = lambda hNAME: (hNAME, 'pt', 200, 0., 1500.)
    hists.data_zpt   = the_data.Histo1D( binpt('data_zpt'), 'recoZ_pt')
    hists.sign_zpt   = df__sign.Histo1D( binpt('sign_zpt'), 'recoZ_pt', 'event_weight')
    take_ratio_in_obj(hists, 'data_zpt', 'sign_zpt', 'ratio_zpt')

    hists.data_mu0pt = the_data.Histo1D( binpt('data_mu0pt'), 'recoMuon0_pt')
    hists.sign_mu0pt = df__sign.Histo1D( binpt('sign_mu0pt'), 'recoMuon0_pt', 'event_weight')
    take_ratio_in_obj(hists, 'data_mu0pt', 'sign_mu0pt', 'ratio_mu0pt')
    hists.data_mu1pt = the_data.Histo1D( binpt('data_mu1pt'), 'recoMuon1_pt')
    hists.sign_mu1pt = df__sign.Histo1D( binpt('sign_mu1pt'), 'recoMuon1_pt', 'event_weight')
    take_ratio_in_obj(hists, 'data_mu1pt', 'sign_mu1pt', 'ratio_mu1pt')
    hists.data_jetpt     = the_data.Histo1D( binpt('data_jetpt')    , 'recoJet_pt')
    hists.data_jetpt_raw = the_data.Histo1D( binpt('data_jetpt_raw'), 'recoJet_rawpt')
    hists.sign_jetpt     = df__sign.Histo1D( binpt('sign_jetpt')    , 'recoJet_pt'   , 'event_weight')
    hists.sign_jetpt_raw = df__sign.Histo1D( binpt('sign_jetpt_raw'), 'recoJet_rawpt', 'event_weight')
    take_ratio_in_obj(hists, 'data_jetpt', 'sign_jetpt'    , 'ratio_jetpt')
    take_ratio_in_obj(hists, 'data_jetpt', 'data_jetpt_raw', 'ratio_jetpt_datacorr')
    take_ratio_in_obj(hists, 'sign_jetpt', 'sign_jetpt_raw', 'ratio_jetpt_signcorr')


    bineta = lambda hNAME: (hNAME, 'eta', 40, -4, 4)
    hists.data_zeta   = the_data.Histo1D( bineta('data_zeta'), 'recoZ_eta')
    hists.sign_zeta   = df__sign.Histo1D( bineta('sign_zeta'), 'recoZ_eta', 'event_weight')
    take_ratio_in_obj(hists, 'data_zeta', 'sign_zeta', 'ratio_zeta')
    hists.data_mu0eta = the_data.Histo1D( bineta('data_mu0eta'), 'recoMuon0_eta')
    hists.sign_mu0eta = df__sign.Histo1D( bineta('sign_mu0eta'), 'recoMuon0_eta', 'event_weight')
    take_ratio_in_obj(hists, 'data_mu0eta', 'sign_mu0eta', 'ratio_mu0eta')
    hists.data_mu1eta = the_data.Histo1D( bineta('data_mu1eta'), 'recoMuon1_eta')
    hists.sign_mu1eta = df__sign.Histo1D( bineta('sign_mu1eta'), 'recoMuon1_eta', 'event_weight')
    take_ratio_in_obj(hists, 'data_mu1eta', 'sign_mu1eta', 'ratio_mu1eta')
    hists.data_jeteta = the_data.Histo1D( bineta('data_jeteta'), 'recoJet_eta')
    hists.sign_jeteta = df__sign.Histo1D( bineta('sign_jeteta'), 'recoJet_eta', 'event_weight')
    take_ratio_in_obj(hists, 'data_jeteta', 'sign_jeteta', 'ratio_jeteta')



    binphi = lambda hNAME: (hNAME, 'phi', 40, -4, 4)
    hists.data_zphi   = the_data.Histo1D( binphi('data_zphi'), 'recoZ_phi')
    hists.sign_zphi   = df__sign.Histo1D( binphi('sign_zphi'), 'recoZ_phi', 'event_weight')
    take_ratio_in_obj(hists, 'data_zphi', 'sign_zphi', 'ratio_zphi')
    hists.data_mu0phi = the_data.Histo1D( binphi('data_mu0phi'), 'recoMuon0_phi')
    hists.sign_mu0phi = df__sign.Histo1D( binphi('sign_mu0phi'), 'recoMuon0_phi', 'event_weight')
    take_ratio_in_obj(hists, 'data_mu0phi', 'sign_mu0phi', 'ratio_mu0phi')
    hists.data_mu1phi = the_data.Histo1D( binphi('data_mu1phi'), 'recoMuon1_phi')
    hists.sign_mu1phi = df__sign.Histo1D( binphi('sign_mu1phi'), 'recoMuon1_phi', 'event_weight')
    take_ratio_in_obj(hists, 'data_mu1phi', 'sign_mu1phi', 'ratio_mu1phi')
    hists.data_jetphi = the_data.Histo1D( binphi('data_jetphi'), 'recoJet_phi')
    hists.sign_jetphi = df__sign.Histo1D( binphi('sign_jetphi'), 'recoJet_phi', 'event_weight')
    take_ratio_in_obj(hists, 'data_jetphi', 'sign_jetphi', 'ratio_jetphi')


    binnPVs = lambda hNAME: (hNAME, 'nPVs', 120,0.,120)
    hists.data_nPVs          = the_data.Histo1D( binnPVs('data_nPVs') , 'PV_npvs')
    hists.sign_nPVs          = df__sign.Histo1D( binnPVs('sign_nPVsORIG'), 'PV_npvs', 'event_weight_no_PUw')
    hists.sign_nPVsWEIG      = df__sign.Histo1D( binnPVs('sign_nPVsWEIG'), 'PV_npvs', 'event_weight') # add pileup weight
    hists.ratio_nPVs_data_mcORIG = TakeNormedRatio('normratio_nPVs_ORIG',hists.data_nPVs, hists.sign_nPVs)
    hists.ratio_nPVs_data_mcWEIG = TakeNormedRatio('normratio_nPVs_WEIG',hists.data_nPVs, hists.sign_nPVsWEIG)

    binnPVsGood = lambda hNAME: (hNAME, 'nPVsGood', 100,0.,100)
    hists.data_nPVsGood          = the_data.Histo1D( binnPVsGood('data_nPVsGood') , 'PV_npvs')
    hists.sign_nPVsGood          = df__sign.Histo1D( binnPVsGood('sign_nPVsGoodORIG'), 'PV_npvs', 'event_weight_no_PUw')
    hists.sign_nPVsGoodWEIG      = df__sign.Histo1D( binnPVsGood('sign_nPVsGoodWEIG'), 'PV_npvs', 'event_weight') # add pileup weight
    hists.ratio_nPVsGood_data_mcORIG = TakeNormedRatio('normratio_nPVsGood_ORIG',hists.data_nPVsGood, hists.sign_nPVsGood)
    hists.ratio_nPVsGood_data_mcWEIG = TakeNormedRatio('normratio_nPVsGood_WEIG',hists.data_nPVsGood, hists.sign_nPVsGoodWEIG)

    binnConstituents = lambda hNAME: (hNAME, 'nConstituents in jet', 120, 0,120)
    hists.data_jetnconst = the_data.Histo1D( binnConstituents('data_jetnconst'), 'recoJet_nConstituents')
    hists.sign_jetnconst = df__sign.Histo1D( binnConstituents('sign_jetnconst'), 'recoJet_nConstituents', 'event_weight')
    take_ratio_in_obj(hists, 'data_jetnconst', 'sign_jetnconst', 'ratio_jetnconst')

    binjetmass = lambda hNAME: (hNAME, 'jet mass', 100, 0., 250.)
    hists.data_jetmass     = the_data.Histo1D( binjetmass('data_jetmass'    ), 'recoJet_mass')
    hists.data_jetmass_raw = the_data.Histo1D( binjetmass('data_jetmass_raw'), 'recoJet_rawmass')
    hists.sign_jetmass     = df__sign.Histo1D( binjetmass('sign_jetmass'    ), 'recoJet_mass',    'event_weight')
    hists.sign_jetmass_raw = df__sign.Histo1D( binjetmass('sign_jetmass_raw'), 'recoJet_rawmass', 'event_weight')
    take_ratio_in_obj(hists, 'data_jetmass', 'sign_jetmass', 'ratio_jetmass')
    take_ratio_in_obj(hists, 'data_jetmass', 'data_jetmass_raw', 'ratio_jetmass_datacorr')
    take_ratio_in_obj(hists, 'sign_jetmass', 'sign_jetmass_raw', 'ratio_jetmass_signcorr')

    f_out = ROOT.TFile(outputFILE, 'recreate')
    hists.WriteAllHists(f_out)
    f_out.Close()
