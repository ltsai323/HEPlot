import uproot
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt

# Open the ROOT file
file = uproot.open("dataMCcomp_endcapPhoton.root")

# Access the 'expdata' directory
expdata = file['expdata']
sign0 = file['sign0']
fake0 = file['fake0']

# Read histograms
hDATA = expdata['phoEta'].to_hist()
hSIGN = sign0['phoEta'].to_hist()
hFAKE = fake0['phoEta'].to_hist()
#phoPt = expdata['phoPt'].to_hist()
#phoEta = expdata['phoEta'].to_hist()
#phoPhi = expdata['phoPhi'].to_hist()

# Create a ratio plot function
def ratio_plot(hist1, hist2, xlabel, ylabel, title):
    fig, (ax, ax_ratio) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

    # Main plot
    hep.histplot(hist1, ax=ax, label='Hist 1')
    hep.histplot(hist2, ax=ax, label='Hist 2')

    ax.set_ylabel(ylabel)
    ax.legend()

    # Ratio plot
    ratio = hist1.values() / hist2.values()
    #ratio_err = ratio * np.sqrt((hist1.errors() / hist1.values())**2 + (hist2.errors() / hist2.values())**2)
    bin_centers = hist1.axes[0].centers

    #ax_ratio.errorbar(bin_centers, ratio, yerr=ratio_err, fmt='o', color='k')
    ax_ratio.errorbar(bin_centers, ratio, fmt='o', color='k')
    ax_ratio.set_ylabel('Ratio')
    ax_ratio.set_xlabel(xlabel)
    ax_ratio.set_ylim(0, 2)

    plt.suptitle(title)
    #plt.show()
    plt.savefig('a.png')

# Assuming histograms are already normalized
# Plot phoPt ratio
ratio_plot(hDATA, hSIGN, xlabel='\eta^{\gamma}', ylabel='Events', title='Ratio')

# You can add more ratio plots similarly for other histograms if needed
# ratio_plot(phoPt, phoPhi, xlabel='pT', ylabel='Events', title='phoPt / phoPhi Ratio')
