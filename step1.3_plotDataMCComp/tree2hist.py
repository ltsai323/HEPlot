#!/usr/bin/env python3

import ROOT


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

class NameSet:
    def __init__(self, varNAME):
        self.data = f'data_{varNAME}'
        self.sign = f'sign_{varNAME}'
        self.fake = f'fake_{varNAME}'
        self.diff = f'ratio_{varNAME}'

        self.stak = f'stak_{varNAME}' # name from simulations stack
        print(f'[NameSet] Generating histograms: {self.data} {self.sign} {self.fake} {self.stak} {self.diff}')
def take_ratio_in_obj(obj, histNAMEset:NameSet):
    h_data = getattr(obj, histNAMEset.data).GetValue() # use GetValue() converting Histo1D to TH1F
    h_sign = getattr(obj, histNAMEset.sign).GetValue()
    h_fake = getattr(obj, histNAMEset.fake).GetValue()
    h_stak = h_sign.Clone()
    h_stak.Add(h_fake)
    h_stak.SetName(histNAMEset.stak)

    diff = TakeRatio(histNAMEset.diff, h_data, h_stak)
    setattr(obj,histNAMEset.diff, diff)
    setattr(obj,histNAMEset.stak, h_stak)

def general_cut(additionalCUT): return f'{additionalCUT}'
#def general_cut(additionalCUT): return f'jet_pt>200 && {additionalCUT}'
#def general_cut(additionalCUT): return f'selected_jet_idx == 0 && {additionalCUT}' ## only select LEADING jet
def all_gjet  (): return general_cut('1')
def WPc_loose (): return general_cut('ParTCvsL > 0.039 && ParTCvsB > 0.067')
def WPc_medium(): return general_cut('ParTCvsL > 0.117 && ParTCvsB > 0.128')
def WPc_tight (): return general_cut('ParTCvsL > 0.358 && ParTCvsB > 0.095')
def WPb_loose (): return general_cut('ParTB > 0.0897')
def WPb_medium(): return general_cut('ParTB > 0.4510')
def WPb_tight (): return general_cut('ParTB > 0.8604')


def mainfunc(dataFILE, signFILE, fakeFILE, outputFILE, additionalCUT):
    the_data = ROOT.RDataFrame('tree', dataFILE).Filter(f'photon_pt>210 && {additionalCUT}')
    the_sign = ROOT.RDataFrame('tree', signFILE).Filter(f'photon_pt>210 && {additionalCUT}')
    the_fake = ROOT.RDataFrame('tree', fakeFILE).Filter(f'photon_pt>210 && {additionalCUT}')
    the_sign = the_sign \
            .Define("event_weight", "wgt * 26.81") # gen weight, xs norm, PU weight, photon SF, trigger SF
    the_fake = the_fake \
            .Define("event_weight", "wgt * 26.81") # gen weight, xs norm, PU weight, photon SF, trigger SF


    hists = histCollection()




    binpt = lambda hNAME: (hNAME, 'pt', 100, 210, 1500.)
    n_phopt = NameSet('phopt')
    hists.data_phopt = the_data.Histo1D( binpt(n_phopt.data), 'photon_pt')
    hists.sign_phopt = the_sign.Histo1D( binpt(n_phopt.sign), 'photon_pt', 'event_weight')
    hists.fake_phopt = the_fake.Histo1D( binpt(n_phopt.fake), 'photon_pt', 'event_weight')
    take_ratio_in_obj(hists, n_phopt)

    n_jetpt = NameSet('jetpt')
    binjetpt = lambda hNAME: (hNAME, 'pt', 100,  50, 1500.)
    hists.data_jetpt     = the_data.Histo1D( binjetpt(n_jetpt.data), 'jet_pt')
    hists.sign_jetpt     = the_sign.Histo1D( binjetpt(n_jetpt.sign), 'jet_pt'   , 'event_weight')
    hists.fake_jetpt     = the_fake.Histo1D( binjetpt(n_jetpt.fake), 'jet_pt'   , 'event_weight')
    take_ratio_in_obj(hists, n_jetpt)

    n_svpt = NameSet('svpt')
    binsvpt = lambda hNAME: (hNAME, 'pt', 100,  50, 1500.)
    hists.data_svpt     = the_data.Histo1D( binsvpt(n_svpt.data), 'jet_SVpt')
    hists.sign_svpt     = the_sign.Histo1D( binsvpt(n_svpt.sign), 'jet_SVpt'   , 'event_weight')
    hists.fake_svpt     = the_fake.Histo1D( binsvpt(n_svpt.fake), 'jet_SVpt'   , 'event_weight')
    take_ratio_in_obj(hists, n_svpt)

    n_svmass = NameSet('svmass')
    binsvmass = lambda hNAME: (hNAME, 'pt', 40, -1., 5.)
    hists.data_svmass     = the_data.Histo1D( binsvmass(n_svmass.data), 'jet_SVmass')
    hists.sign_svmass     = the_sign.Histo1D( binsvmass(n_svmass.sign), 'jet_SVmass'   , 'event_weight')
    hists.fake_svmass     = the_fake.Histo1D( binsvmass(n_svmass.fake), 'jet_SVmass'   , 'event_weight')
    take_ratio_in_obj(hists, n_svmass)




    bineta = lambda hNAME: (hNAME, 'eta', 40, -4, 4)
    n_phoeta = NameSet('phoeta')
    hists.data_phoeta = the_data.Histo1D( bineta(n_phoeta.data), 'photon_eta')
    hists.sign_phoeta = the_sign.Histo1D( bineta(n_phoeta.sign), 'photon_eta', 'event_weight')
    hists.fake_phoeta = the_fake.Histo1D( bineta(n_phoeta.fake), 'photon_eta', 'event_weight')
    take_ratio_in_obj(hists, n_phoeta)

    n_jeteta = NameSet('jeteta')
    hists.data_jeteta = the_data.Histo1D( bineta(n_jeteta.data), 'jet_eta')
    hists.sign_jeteta = the_sign.Histo1D( bineta(n_jeteta.sign), 'jet_eta', 'event_weight')
    hists.fake_jeteta = the_fake.Histo1D( bineta(n_jeteta.fake), 'jet_eta', 'event_weight')
    take_ratio_in_obj(hists, n_jeteta)

    binsieie = lambda hNAME: (hNAME, 'sieie', 40, 0., 0.04)
    n_sieie = NameSet('sieie')
    hists.data_sieie = the_data.Histo1D( binsieie(n_sieie.data), 'photon_sieie')
    hists.sign_sieie = the_sign.Histo1D( binsieie(n_sieie.sign), 'photon_sieie', 'event_weight')
    hists.fake_sieie = the_fake.Histo1D( binsieie(n_sieie.fake), 'photon_sieie', 'event_weight')
    take_ratio_in_obj(hists, n_sieie)

    binhoe = lambda hNAME: (hNAME, 'hoe', 40, 0., 0.05)
    n_hoe = NameSet('hoe')
    hists.data_hoe = the_data.Histo1D( binhoe(n_hoe.data), 'photon_hoe')
    hists.sign_hoe = the_sign.Histo1D( binhoe(n_hoe.sign), 'photon_hoe', 'event_weight')
    hists.fake_hoe = the_fake.Histo1D( binhoe(n_hoe.fake), 'photon_hoe', 'event_weight')
    take_ratio_in_obj(hists, n_hoe)



    binphi = lambda hNAME: (hNAME, 'phi', 40, -4, 4)
    n_phophi = NameSet('phophi')
    hists.data_phophi = the_data.Histo1D( binphi(n_phophi.data), 'photon_phi')
    hists.sign_phophi = the_sign.Histo1D( binphi(n_phophi.sign), 'photon_phi', 'event_weight')
    hists.fake_phophi = the_fake.Histo1D( binphi(n_phophi.fake), 'photon_phi', 'event_weight')
    take_ratio_in_obj(hists, n_phophi)

    n_jetphi = NameSet('jetphi')
    hists.data_jetphi = the_data.Histo1D( binphi(n_jetphi.data), 'jet_phi')
    hists.sign_jetphi = the_sign.Histo1D( binphi(n_jetphi.sign), 'jet_phi', 'event_weight')
    hists.fake_jetphi = the_fake.Histo1D( binphi(n_jetphi.fake), 'jet_phi', 'event_weight')
    take_ratio_in_obj(hists, n_jetphi)


    #binnPVs = lambda hNAME: (hNAME, 'nPVs', 120,0.,120)
    #hists.data_nPVs          = the_data.Histo1D( binnPVs('data_nPVs') , 'PV_npvs')
    #hists.sign_nPVs          = the_sign.Histo1D( binnPVs('sign_nPVsORIG'), 'PV_npvs', 'event_weight_no_PUw')
    #hists.sign_nPVsWEIG      = the_sign.Histo1D( binnPVs('sign_nPVsWEIG'), 'PV_npvs', 'event_weight') # add pileup weight
    #hists.ratio_nPVs_data_mcORIG = TakeNormedRatio('normratio_nPVs_ORIG',hists.data_nPVs, hists.sign_nPVs)
    #hists.ratio_nPVs_data_mcWEIG = TakeNormedRatio('normratio_nPVs_WEIG',hists.data_nPVs, hists.sign_nPVsWEIG)

    #binnPVsGood = lambda hNAME: (hNAME, 'nPVsGood', 100,0.,100)
    #hists.data_nPVsGood          = the_data.Histo1D( binnPVsGood('data_nPVsGood') , 'PV_npvs')
    #hists.sign_nPVsGood          = the_sign.Histo1D( binnPVsGood('sign_nPVsGoodORIG'), 'PV_npvs', 'event_weight_no_PUw')
    #hists.sign_nPVsGoodWEIG      = the_sign.Histo1D( binnPVsGood('sign_nPVsGoodWEIG'), 'PV_npvs', 'event_weight') # add pileup weight
    #hists.ratio_nPVsGood_data_mcORIG = TakeNormedRatio('normratio_nPVsGood_ORIG',hists.data_nPVsGood, hists.sign_nPVsGood)
    #hists.ratio_nPVsGood_data_mcWEIG = TakeNormedRatio('normratio_nPVsGood_WEIG',hists.data_nPVsGood, hists.sign_nPVsGoodWEIG)

    binjetMultiplicity = lambda hNAME: (hNAME, 'jet multiplicity', 40,0.,40.)
    n_jetmultp = NameSet('jetmultp') # jet multiplicity
    hists.data_jetmultp = the_data.Histo1D( binjetMultiplicity(n_jetmultp.data), 'jet_multiplicity')
    hists.sign_jetmultp = the_sign.Histo1D( binjetMultiplicity(n_jetmultp.sign), 'jet_multiplicity', 'event_weight')
    hists.fake_jetmultp = the_sign.Histo1D( binjetMultiplicity(n_jetmultp.fake), 'jet_multiplicity', 'event_weight')
    take_ratio_in_obj(hists, n_jetmultp)

    n_svmultp = NameSet('svmultp') # jet multiplicity
    hists.data_svmultp = the_data.Histo1D( binjetMultiplicity(n_svmultp.data), 'jet_nSV')
    hists.sign_svmultp = the_sign.Histo1D( binjetMultiplicity(n_svmultp.sign), 'jet_nSV', 'event_weight')
    hists.fake_svmultp = the_sign.Histo1D( binjetMultiplicity(n_svmultp.fake), 'jet_nSV', 'event_weight')
    take_ratio_in_obj(hists, n_svmultp)

    binjetmass = lambda hNAME: (hNAME, 'jet mass', 100, 0., 250.)
    #hists.data_jetmass     = the_data.Histo1D( binjetmass('data_jetmass'    ), 'recoJet_mass')
    #hists.data_jetmass_raw = the_data.Histo1D( binjetmass('data_jetmass_raw'), 'recoJet_rawmass')
    #hists.sign_jetmass     = the_sign.Histo1D( binjetmass('sign_jetmass'    ), 'recoJet_mass',    'event_weight')
    #hists.sign_jetmass_raw = the_sign.Histo1D( binjetmass('sign_jetmass_raw'), 'recoJet_rawmass', 'event_weight')
    #take_ratio_in_obj(hists, 'data_jetmass', 'sign_jetmass', 'ratio_jetmass')
    #take_ratio_in_obj(hists, 'data_jetmass', 'data_jetmass_raw', 'ratio_jetmass_datacorr')
    #take_ratio_in_obj(hists, 'sign_jetmass', 'sign_jetmass_raw', 'ratio_jetmass_signcorr')


    binchiso = lambda hNAME: (hNAME, 'chiso', 40, 0, 2)
    n_phochiso = NameSet('chiso')
    hists.data_chiso = the_data.Histo1D( binchiso(n_phochiso.data), 'photon_pfChargedIsoPFPV')
    hists.sign_chiso = the_sign.Histo1D( binchiso(n_phochiso.sign), 'photon_pfChargedIsoPFPV', 'event_weight')
    hists.fake_chiso = the_fake.Histo1D( binchiso(n_phochiso.fake), 'photon_pfChargedIsoPFPV', 'event_weight')
    take_ratio_in_obj(hists, n_phochiso)



    f_out = ROOT.TFile(outputFILE, 'recreate')
    hists.WriteAllHists(f_out)
    f_out.Close()

if __name__ == "__main__":

#data_file = '/data4/ltsai/ProducedFiles/2022EE/ZJet/stage2_ZJetData.root'
#sign_file = '/data4/ltsai/ProducedFiles/2022EE/ZJet/stage2_ZJetMC_DYto2L2Jets.root'
#data_file = '/home/ltsai/stage2_ZJetData.root'
#sign_file = '/home/ltsai/stage2_ZJetMC_DYto2L2Jets_MLL50_0to2J.root'
#data_file = '/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_ZJet/stage2/stage2_ZJetData.root'
#sign_file = '/eos/home-l/ltsai/eos_storage/condor_summary/2022EE_ZJet/stage2/stage2_ZJetMC_DYto2L2Jets_MLL50_0to2J.root'

#data_file = '/home/ltsai/ProducedFiles/2022EE/GJet/stage2_GJetDataDataSideband.root'
    #data_file = '/home/ltsai/ProducedFiles/2022EE/GJet/stage2_GJetDataSignalRegion.root'
    #sign_file = '/home/ltsai/ProducedFiles/2022EE/GJet/stage2_GJetMCGJetMadgraph.root'
    #fake_file = '/home/ltsai/ProducedFiles/2022EE/GJet/stage2_QCDMadgraph.root'
    #data_file = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root'
    data_file = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root'
    #sign_file = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.all.root'
    sign_file = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root'
    #fake_file = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.all.root'
    fake_file = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root'
#sign_file = '/home/ltsai/ProducedFiles/2022EE/GJet/stage2_GJetPythiaFlat.root'



    output_file = lambda tag: f'output_{tag.strip()}.root' # stript() ignore redundant " "


    mainfunc(data_file, sign_file, fake_file, output_file('all_gjet  '), WPc_loose () )
    mainfunc(data_file, sign_file, fake_file, output_file('WPc_loose '), WPc_loose () )
    mainfunc(data_file, sign_file, fake_file, output_file('WPc_loose '), WPc_loose () )
    mainfunc(data_file, sign_file, fake_file, output_file('WPc_medium'), WPc_medium() )
    mainfunc(data_file, sign_file, fake_file, output_file('WPc_tight '), WPc_tight () )
    mainfunc(data_file, sign_file, fake_file, output_file('WPb_loose '), WPb_loose () )
    mainfunc(data_file, sign_file, fake_file, output_file('WPb_medium'), WPb_medium() )
    mainfunc(data_file, sign_file, fake_file, output_file('WPb_tight '), WPb_tight () )
