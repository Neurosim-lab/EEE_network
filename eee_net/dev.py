import batch_utils
import batch_analysis
import matplotlib.pyplot as plt
from netpyne import sim
plt.ion()

batchdatadir = "data"


def analyze_batch(batchLabel, batchdatadir=batchdatadir):

	params, data = batch_utils.load_batch(batchLabel, batchdatadir=batchdatadir)
	batch = (batchLabel, params, data)


	batch_analysis.plot_batch_raster(batch, timeRange=[100, 1000], markerSize=0.5)
	batch_analysis.plot_vtraces(batch, timerange=[100, 1000])


#analyze_batch('v01_batch03')
#analyze_batch('v01_batch04')
#analyze_batch('v01_batch05')
analyze_batch('v01_batch06')

















# sim.load(batchdatadir + '/' + batchLabel + '/' + batchLabel + curSim + '.json', instantiate=False)

# fig1 = sim.analysis.plotTraces()
# fig2 = sim.analysis.plotRaster(orderInverse=True)
# fig3 = sim.analysis.plotSpikeHist()
# fig4 = sim.analysis.plotSpikeStats()
# fig5 = sim.analysis.plotConn()
# fig6 = sim.analysis.plotRatePSD()
# fig7 = sim.analysis.plot2Dnet()







# vtraces = batch_analysis.get_vtraces(params, data)
# fig = batch_analysis.plot_relation(**vtraces)

# batch = (batchLabel, params, data)
# batch_analysis.plot_vtraces(batch, timerange=[100, 1000])

# batch_analysis.plot_num_spikes(batchLabel)

plt.show()

