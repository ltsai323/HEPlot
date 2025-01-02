import matplotlib.pyplot as plt

# Sample data
data1 = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
data2 = [2, 3, 3, 4, 4, 5, 5, 5, 6]
edges = [ i for i in range(10) ]

fig, ax = plt.subplots()

# Plot histograms separately
ax.hist(data1, bins=edges, alpha=0.5, label='Data 1', histtype='stepfilled', edgecolor='black')
ax.hist(data2, bins=edges, alpha=0.5, label='Data 2', histtype='stepfilled', edgecolor='black')

# Add legend
ax.legend()

# Show plot
plt.show()
