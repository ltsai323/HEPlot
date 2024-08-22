#!/usr/bin/env python3
import uproot

import matplotlib.pyplot as plt



if __name__ == "__main__":
    f = uproot.open('HLT_AbsTurnOnEff_JetHT_UL2016PostVFP.root')
    h = f['HLTbit7/endcap_ratio']
    print(type(h))

    values0, values1 = h.values()
    low0, low1 = h.errors('low')
    high0, high1 = h.errors('high')
    mean0, mean1 = h.errors('mean')
    diff0, diff1 = h.errors('diff')


    y_err = [low1,high1]
    x_err = [low0,high0]
    plt.errorbar(values0,values1, xerr=x_err, yerr=y_err, fmt='o', capsize=5, label='hiiii')

    plt.legend()
    plt.show()

    
