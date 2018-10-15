import matplotlib.pyplot as plt
import numpy as np

plt.ion()

distance = range(10, 200, 10)
numspines = [0.982, 4.677, 10.91, 14.72, 18.24, 18.76, 19.05, 17.15, 17.38, 16.17, 15.36, 15.07, 15.24, 13.97, 12.53, 12.64, 11.84, 9.988, 11.43]

# Data from: 
# Ballesteros-Yanez, Benavides-Piccione, Elston, Yuste, DeFelipe. Density and
# morphology of dendritic spines in mouse neocortex. Neuroscience. 2006; 138:403-9.

def getspineLocs(numspines, spinedist=[1]):
    numspines += 2
    numsecs = len(spinedist)
    spinespersec = []
    total_weight = sum(spinedist)
    for weight in spinedist:
        weight = float(weight)
        if weight > 0:
            share = weight / total_weight
        else:
            share = 0.0
        distributed = round(share * numspines)
        spinespersec.append(distributed)
        total_weight -= weight
        numspines -= distributed
    spineLocs = []
    for index, spines in enumerate(spinespersec):
        start = index * (1./numsecs)
        stop = (index + 1) * (1./numsecs)
        spineLocs.extend(np.linspace(start, stop, num=spines, endpoint=False).tolist())
    spineLocs = spineLocs[1:-1]
    return spineLocs

# Physiological distribution
spinedist = 200 * np.array(getspineLocs(1000, numspines))
hist, bin_edges = np.histogram(spinedist, bins=20, range=(0,200), density=True)

# Actual number of spines in model
spineLocs = 200 * np.array(getspineLocs(255, spinedist=numspines))
hist2, bin_edges2 = np.histogram(spineLocs, bins=20, range=(0,200))

centers = (bin_edges2[:-1] + bin_edges2[1:]) / 2

fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.bar(bin_edges[0:-1], hist*1000, width=10, label="Physiological Distribution")
ax1.set_xlabel("Distance from Soma (um)")
ax1.set_ylabel("Spine Distribution (percent)")
ax1.set_ylim(0, 8)

ax2 = ax1.twinx()
ax2.plot(centers, hist2, "-go", label="Modeled Physiological")
ax2.plot(centers, np.zeros(np.shape(centers)) + 12.0, "-rd", label="Modeled Uniform")
ax2.set_ylabel("Number of Spines in Model")
ax2.set_ylim(0, 20)

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0, fontsize="small")
ax2.set_title("Spine Distribution and Number of Spines Modeled")

fig.savefig("spinedists.png", dpi=600, bbox_inches='tight')




