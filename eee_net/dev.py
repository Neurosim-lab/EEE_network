import batch_utils
import batch_analysis
import matplotlib.pyplot as plt

batchLabel = "bill_batch_05"

params, data = batch_utils.load_batch(batchLabel, "data")

#vtraces = batch_analysis.get_vtraces(params, data)

#fig = batch_analysis.plot_relation(**vtraces)

fig2 = batch_analysis.plot_vtraces(batchLabel)

plt.show()

