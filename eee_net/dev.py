import batch_utils
import batch_analysis
import matplotlib.pyplot as plt
from netpyne import sim
plt.ion()

batchdatadir = "data"
batchLabel = "bill_batch_05"

curSim = "_0_0"

params, data = batch_utils.load_batch(batchLabel, batchdatadir=batchdatadir)
batch = (batchLabel, params, data)

batch_analysis.plot_batch_raster(batch)








# sim.load(batchdatadir + '/' + batchLabel + '/' + batchLabel + curSim + '.json', instantiate=False)

# fig1 = sim.analysis.plotTraces()
# fig2 = sim.analysis.plotRaster(orderInverse=True)
# fig3 = sim.analysis.plotSpikeHist()
# fig4 = sim.analysis.plotSpikeStats()
# fig5 = sim.analysis.plotConn()
# fig6 = sim.analysis.plotRatePSD()
# fig7 = sim.analysis.plot2Dnet()


# Code to get three rasters and plot them as subplots

# bigfig = plt.figure()

# bfax0 = plt.subplot(1,3,1)
# bfax1 = plt.subplot(1,3,2)
# bfax2 = plt.subplot(1,3,3)

# curSim = "_0_0"
# sim.load(batchdatadir + '/' + batchLabel + '/' + batchLabel + curSim + '.json', instantiate=False)
# sim.analysis.plotRaster(orderInverse=True, altAx=bfax0)

# curSim = "_0_1"
# sim.load(batchdatadir + '/' + batchLabel + '/' + batchLabel + curSim + '.json', instantiate=False)
# sim.analysis.plotRaster(orderInverse=True, altAx=bfax1, labels=None)

# curSim = "_0_2"
# sim.load(batchdatadir + '/' + batchLabel + '/' + batchLabel + curSim + '.json', instantiate=False)
# sim.analysis.plotRaster(orderInverse=True, altAx=bfax2, labels=None)




# vtraces = batch_analysis.get_vtraces(params, data)
# fig = batch_analysis.plot_relation(**vtraces)

# batch = (batchLabel, params, data)
# batch_analysis.plot_vtraces(batch, timerange=[100, 1000])

# batch_analysis.plot_num_spikes(batchLabel)

plt.show()

