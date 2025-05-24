hist_lists = [
"bin11L_all_" ,
"bin11L_WPcM_",
"bin11L_WPcT_",
"bin11L_WPbM_",
"bin11L_WPbT_",
'',

"bin11C_all_" ,
"bin11C_WPbL_",
"bin11C_WPbM_",
"bin11C_WPbT_",
'',

"bin11B_all_" ,
"bin11B_WPcL_",
"bin11B_WPcM_",
"bin11B_WPcT_",
]

import ROOT
f = ROOT.TFile.Open("WPeff_2022GJetMadgraph.root")

def check_hist(tfile,hNAME):
    if hNAME == '':
        print('\n')
        return
    h = tfile.Get(hNAME)
    nbins = h.GetNbinsX()
    print(f'[AccessHist] {h.GetName()}')
    for ibin in range(nbins):
        binIdx = ibin+1
        binval = h.GetBinContent(binIdx)
        if binval < 100:
            edgeL = h.GetBinLowEdge(binIdx)
            edgeR = h.GetBinLowEdge(binIdx+1)

            print(f'[LowStatistics] binning({edgeL:4.0f},{edgeR:4.0f}) got BinContent({binval})')
    print(f'[AccessHistENDED] {h.GetName()}')

for histname in hist_lists:
    check_hist(f, histname)

