import matplotlib.pyplot as plt
import numpy as np

# Data
labels = ['bVAL', 'cVAL']
fit_means = np.array([45, 23])
truth_means = np.array([42, 5])
fit_errors = np.array([3, 10])
truth_errors = np.array([1, 10])

# Ratios and error
ratios = fit_means / truth_means
ratio_errors = ratios * np.sqrt((fit_errors / fit_means) ** 2 + (truth_errors / truth_means) ** 2)

# Bin edges (assume equal spacing), length = len(labels) + 1
bin_edges = np.arange(len(labels) + 1)  # [0, 1, 2]
bin_centers = bin_edges[:-1] + 0.5      # [0.5, 1.5] — labels will go here

# Figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10), sharex=True)

# Plot bars centered within each bin
width = 0.35
x = bin_centers  # [0.5, 1.5]
ax1.bar(x - width/2, fit_means, width, label='Fit', yerr=fit_errors, capsize=5)
ax1.bar(x + width/2, truth_means, width, label='Truth', yerr=truth_errors, capsize=5)
ax1.set_ylabel('Values')
ax1.set_title('Grouped Error Bar Chart')
ax1.legend()

# Ratio plot
ax2.errorbar(x, ratios, yerr=ratio_errors, fmt='o', color='green', capsize=5, label='Fit / Truth Ratio')
ax2.axhline(1, color='red', linestyle='--')
ax2.set_ylabel('Ratio (Fit / Truth)')
ax2.set_ylim(0, np.max(ratios + ratio_errors) * 1.2)
ax2.legend()

# Set xticks at bin centers, labels between the edges
ax2.set_xticks(bin_centers)
ax2.set_xticklabels(labels)

# Optional: draw vertical lines at bin edges to visually clarify spacing
for edge in bin_edges:
    ax2.axvline(edge, color='gray', linestyle=':', linewidth=0.5)

plt.tight_layout()
plt.show()
