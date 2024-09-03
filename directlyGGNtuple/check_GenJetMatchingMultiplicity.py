#!/usr/bin/env python3
'''
  // -1 : failed offical gen-jet matching
  //  n : n gen jet matched with gen photon
  //  9 : number of gen photon in this sample
'''
import ROOT

def GetArgs_IOFiles(argv):
    return 'result_rr.root'
    return argv[1]


def InterpretHistogram(hist):
    bin_failed = hist.GetBinContent(0+1)
    # bin2: 0, bin9: 7
    binN = { iBin-2: hist.GetBinContent(iBin) for iBin in range(2,9+1) }
    bin_total_entries = hist.GetBinContent(10+1)

    print(f''' ------- Result -------
            Mutiplicity of gen jet in each event.
           -1 : {bin_failed:5.2e} ({bin_failed/bin_total_entries:5.2f})  -- Failed to get offical jet matching
            0 : {binN[0]   :5.2e} ({binN[0]   /bin_total_entries:5.2f})  -- 0 jet matched to gen photon
            1 : {binN[1]   :5.2e} ({binN[1]   /bin_total_entries:5.2f})  -- 1 jet matched to gen photon
            2 : {binN[2]   :5.2e} ({binN[2]   /bin_total_entries:5.2f})  -- 2 jet matched to gen photon
            3 : {binN[3]   :5.2e} ({binN[3]   /bin_total_entries:5.2f})  -- 3 jet matched to gen photon
            4 : {binN[4]   :5.2e} ({binN[4]   /bin_total_entries:5.2f})  -- 4 jet matched to gen photon
            5 : {binN[5]   :5.2e} ({binN[5]   /bin_total_entries:5.2f})  -- 5 jet matched to gen photon
            6 : {binN[6]   :5.2e} ({binN[6]   /bin_total_entries:5.2f})  -- 6 jet matched to gen photon
            7 : {binN[7]   :5.2e} ({binN[7]   /bin_total_entries:5.2f})  -- 7 jet matched to gen photon
            9 : {bin_total_entries:5.2e}   -- Total number of gen photon
            ''')

if __name__ == "__main__":
    import sys
    inFILE = GetArgs_IOFiles(sys.argv)
    tfile = ROOT.TFile.Open(inFILE)
    the_hist = tfile.Get('checkerplot')
    InterpretHistogram(the_hist)

