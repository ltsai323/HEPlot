#!/usr/bin/env python3

import uproot
import pandas as pd



if __name__ == "__main__":
    inFILE = '/Users/noises/Downloads/ggtree_mc_107.root'
    tfile = uproot.open(inFILE)
    ttree = tfile['ggNtuplizer/EventTree']
    df = ttree.arrays(['phoEt', 'nJet'], 'phoEt>30 & nJet>0')
    print(df)
    #print(df['jetSecVtxPt'][:, 0])

    