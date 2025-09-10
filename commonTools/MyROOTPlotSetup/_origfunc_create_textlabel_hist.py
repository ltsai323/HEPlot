#!/usr/bin/env python3

import ROOT


BIN_LABEL = [ 'lVAL', 'cVAL', 'bVAL' ]
NBIN = len(BIN_LABEL)
fout = ROOT.TFile('newfile.root','recreate')
hist = ROOT.TH1F('h1', 'test hist', NBIN, 0, NBIN)

hist.SetBinContent(1,23)
hist.SetBinError  (1,3)
hist.SetBinContent(2,18)
hist.SetBinError  (2,1.3)
hist.SetBinContent(3,40)
hist.SetBinError  (3,4)


r = ROOT.TGraphAsymmErrors()
r.SetName('theratio')
r.Divide(hist,hist,'pois')

for idx, binLabel in enumerate(BIN_LABEL):
    binIdx = idx+1
    hist.GetXaxis().SetBinLabel(binIdx,binLabel)
    #r.GetXaxis().SetBinLabel(binIdx,binLabel)


hist.Write()
r.Write()
fout.Close()
