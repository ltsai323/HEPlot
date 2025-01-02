#!/usr/bin/env python3
import uproot
import matplotlib.pyplot as plt

def normalized_histogram(origHIST):
    bin_contents = origHIST.values()
    bin_errors = origHIST.errors()
    integration = sum(bin_contents)
    return  (bin_contents/integration, bin_errors/integration)
def get_x_axis_info(origHIST):
    x_centers = origHIST.axis().centers()
    x_error = origHIST.axis().widths() / 2.
    return (x_centers,x_error),

    

if __name__ == "__main__":
    inFILE = uproot.open('secondary_plotable.root')
    hists = {
            'L': 'Lall/DeepFlavour_bScore',
            'C': 'Call/DeepFlavour_bScore',
            'ratio': 'ratioC_L__bS',
    }

    xAxis = get_x_axis_info(histL['bScore'])
    normalized_L = normalized_histogram(histL['bScore'])
    normalized_C = normalized_histogram(histC['bScore'])

    fig, ax = plt.subplot()
    plt.hist(normalized_L[0], bins=normalized_L[0]

    

