#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint


def visualize(binCENTERs, binCONTENTs, binWIDTHs, **plotXargs):
    pprint(binCENTERs)
    pprint(binCONTENTs)
    pprint(binWIDTHs)
    plt.bar(binCENTERs, binCONTENTs, width=binWIDTHs, align='center', **plotXargs)



def GetXS_fromTTree(inFILE):
    import ROOT
    f = ROOT.TFile.Open(inFILE)
    t = f.Get("t2")
    info = t.GetUserInfo().At(0)
    print(info)
    return info[1]

def GetXS_fromRes(inFILE):
    with open(inFILE,'r') as fIN:
        content = fIN.read().strip()
        #print(content)
        c = content.split(' ')
        nEvt = float(c[0])
        xs = float(c[1])
        #print( nEvt, xs)
        return xs

def GetHistFromFile(sampleTEMPLATE, ptDEF):
    histCONTENT = []
    bin_centers = []
    bin_widths = []

    pt_range = ptDEF
    for idx in range(1,len(pt_range)):
        ptL = pt_range[idx-1]
        ptH = pt_range[idx]
        bin_center = (ptL+ptH) / 2.
        bin_width = ptH-ptL
        bin_content = GetXS_fromRes( sampleTEMPLATE.format(idx=idx) )

        bin_centers.append(bin_center)
        bin_widths.append(bin_width)
        histCONTENT.append(bin_content)
    return bin_centers, histCONTENT, bin_widths


def pt_def():
    return [ 190., 200., 220., 250., 300., 350., 400., 500., 750., 1000., 1500., ]

if __name__ == "__main__":
    sampleNorm = 'withoutPDFerr{idx}/2024_10_26__LOgeneration_13600GeV_NNPDF31_nlo_as_0118_0_NNPDF31_nlo_as_0118_0_iso2GeVinR04_IS1p0_RENORM1p0_FS1p0/ggd2024_10_26__LOgeneration_13600GeV_NNPDF31_nlo_as_0118_0_NNPDF31_nlo_as_0118_0_iso2GeVinR04_IS1p0_RENORM1p0_FS1p0.res'
    sample151 = 'withoutPDFerr{idx}/2024_10_20__LOgeneration_13600GeV_1Mevts_NNPDF31_nlo_as_0118_0_NNPDF31_nlo_as_0118_0_iso2GeVinR04_IS1p0_RENORM0p5_FS1p0/ggd2024_10_20__LOgeneration_13600GeV_1Mevts_NNPDF31_nlo_as_0118_0_NNPDF31_nlo_as_0118_0_iso2GeVinR04_IS1p0_RENORM0p5_FS1p0.res'
    pt_range = pt_def()
    bin_centers, contentNorm, bin_widths = GetHistFromFile(sampleNorm, pt_range)
    bin_centers, content151, bin_widths = GetHistFromFile(sample151, pt_range)




    #visualize( bin_centers, histCONTENT, bin_widths)
    visualize( bin_centers, contentNorm, bin_widths, edgecolor='blue', fill=False, label='IS=1 RENORM=1 FS=1' )
    visualize( bin_centers, content151, bin_widths, edgecolor='red' , fill=False, label='IS=1 RENORM=0.5 FS=1' )
    plt.legend()

    plt.xlabel('$p^{\gamma}_{T}$ (GeV)')
    plt.ylabel('generated differential $\sigma$')
    plt.show()


