import batch_utils
import batch_analysis
import matplotlib.pyplot as plt
from netpyne import sim
from itertools import product
plt.ion()

batchdatadir = "data"


def analyze_batch(batchLabel, batchdatadir=batchdatadir):

	params, data = batch_utils.load_batch(batchLabel, batchdatadir=batchdatadir)
	batch = (batchLabel, params, data)


	#batch_analysis.plot_batch_raster(batch, timeRange=[100, 1000], markerSize=0.5, orderInverse=False)
	
	#batch_analysis.plot_vtraces(batch, timerange=[100, 1000])

	batch_analysis.plot_batch_conn(batch)


#analyze_batch('v01_batch03')
#analyze_batch('v01_batch04')
#analyze_batch('v01_batch05')
#analyze_batch('v01_batch06')


# Individual plots

def plot_batch_ind_conn(batchname, batchdatadir='data', includePre = ['all'], includePost = ['all'], feature = 'strength', orderBy = 'gid', figSize = (10,10), groupBy = 'pop', groupByIntervalPre = None, groupByIntervalPost = None, graphType = 'matrix', synOrConn = 'syn', synMech = None, connsFile = None, tagsFile = None, clim = None, fontSize = 12, saveData = None, saveFig = None, showFig = True, save=True, outputdir="batch_figs", filename=None, **kwargs):
    """Plots individual raster plots for each parameter combination."""

    if type(batchname) == str:
        params, data = batch_utils.load_batch(batchname, batchdatadir=batchdatadir)
    elif type(batchname) == tuple:
        batchname, params, data = batchname
    else:
        raise Exception()

    groupedParams = False
    ungroupedParams = False

    for p in params:
        if 'group' not in p: 
            p['group'] = False
            ungroupedParams = True
        elif p['group'] == True: 
            groupedParams = True

    if ungroupedParams:
        labelList, valuesList = zip(*[(p['label'], p['values']) for p in params if p['group'] == False])
        valueCombinations = list(product(*(valuesList)))
        indexCombinations = list(product(*[range(len(x)) for x in valuesList]))
    else:
        valueCombinations = [(0,)] # this is a hack -- improve!
        indexCombinations = [(0,)]
        labelList = ()
        valuesList = ()

    if groupedParams:
        labelListGroup, valuesListGroup = zip(*[(p['label'], p['values']) for p in params if p['group'] == True])
        valueCombGroups = zip(*(valuesListGroup))
        indexCombGroups = zip(*[range(len(x)) for x in valuesListGroup])
        labelList = labelListGroup+labelList
    else:
        valueCombGroups = [(0,)] # this is a hack -- improve!
        indexCombGroups = [(0,)]

    for iCombG, pCombG in zip(indexCombGroups, valueCombGroups):
        for iCombNG, pCombNG in zip(indexCombinations, valueCombinations):
            if groupedParams and ungroupedParams: # temporary hack - improve
                iComb = iCombG+iCombNG
                pComb = pCombG+pCombNG
            elif ungroupedParams:
                iComb = iCombNG
                pComb = pCombNG
            elif groupedParams:
                iComb = iCombG
                pComb = pCombG
            else:
                iComb = []
                pComb = []
                
            print(iComb, pComb)

            for i, paramVal in enumerate(pComb):
                paramLabel = labelList[i]
                print(str(paramLabel)+' = '+str(paramVal))

            simLabel = batchLabel+''.join([''.join('_'+str(i)) for i in iComb])
            print(simLabel)

            simFile = simLabel + ".json"

            sim.load(batchdatadir + '/' + batchLabel + '/' + simFile, instantiate=False)

            sim.analysis.plotConn(includePre=includePre, includePost=includePost, feature=feature, orderBy=orderBy, figSize=figSize, groupBy=groupBy, groupByIntervalPre=groupByIntervalPre, groupByIntervalPost=groupByIntervalPost, graphType=graphType, synOrConn=synOrConn, synMech=synMech, connsFile=connsFile, tagsFile=tagsFile, clim=clim, fontSize=fontSize, saveData=saveData, saveFig=saveFig, showFig=showFig)




batchLabel = "v01_batch03"
params, data = batch_utils.load_batch(batchLabel, batchdatadir=batchdatadir)
batch = (batchLabel, params, data)
include = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5']
figFile = batchdatadir + '/' + batchLabel + '/' + 'connFig_' + batchLabel + '.png'
plot_batch_ind_conn(batch, includePre=include, includePost=include, saveFig=figFile)


    














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

