#!/usr/bin/env python3
import ROOT


def GetRatio(name, cHIST, bHIST):
    ratio = ROOT.TGraphAsymmErrors()
    ratio.Divide(cHIST, bHIST, 'pois')
    ratio.SetName(name)
    return ratio

def GetRatio_Bayes(name, cHIST, allHIST):
    ratio = ROOT.TGraphAsymmErrors()
    ratio.BayesDivid(cHIST, allHIST)
    ratio.SetName(name)
    return ratio

if __name__ == "__main__":
    inFILE = 'result.root'
    tfile = ROOT.TFile.Open(inFILE)
    h_c_yield = tfile.Get('genCyield')
    h_b_yield = tfile.Get('genByield')
    h_l_yield = tfile.Get('genLyield')

    ## create all
    h_l_yield.Add(h_c_yield)
    h_l_yield.Add(h_b_yield)

    ratio = GetRatio_Bayes('c_composition', h_c_yield, h_l_yield)

    canv = ROOT.TCanvas("c1", "", 1000,1000)
    canv.Divide(1,2)
    canv.cd(1).SetLogy()
    h_c_yield.Draw("HIST")
    canv.cd(2)
    ratio.Draw()
    canv.SaveAs("hi.png")

