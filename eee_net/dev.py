import batch_utils
import batch_analysis
import matplotlib.pyplot as plt
from netpyne import sim
from itertools import product
import os
plt.ion()

batchdatadir = "data"


def analyze_batch(batchLabel, batchdatadir=batchdatadir):

    params, data = batch_utils.load_batch(batchLabel, batchdatadir=batchdatadir)
    batch = (batchLabel, params, data)

    batch_analysis.plot_batch_raster(batch, timeRange=[100, 1000], markerSize=0.5, orderInverse=False)
    batch_analysis.plot_vtraces(batch, timerange=[100, 1000])
    #batch_analysis.plot_batch_conn(batch)

#analyze_batch('v01_batch03')
#analyze_batch('v01_batch04')
#analyze_batch('v01_batch05')
#analyze_batch('v01_batch06')




# Individual plots

def plot_batch_ind_conn(batchLabel, batchdatadir='data', includePre = ['all'], includePost = ['all'], feature = 'strength', orderBy = 'gid', figSize = (10,10), groupBy = 'pop', groupByIntervalPre = None, groupByIntervalPost = None, graphType = 'matrix', synOrConn = 'syn', synMech = None, connsFile = None, tagsFile = None, clim = None, fontSize = 12, saveData = None, showFig = False, save=True, outputdir='batch_figs'):
    """Plots individual connectivity plots for each parameter combination."""

    from netpyne import specs

    if type(batchLabel) == str:
        params, data = batch_utils.load_batch(batchLabel, batchdatadir=batchdatadir)
    elif type(batchLabel) == tuple:
        batchLabel, params, data = batchLabel
    else:
        raise Exception()

    simLabels = data.keys()

    for simLabel in simLabels:

        print('Plotting sim: ' + simLabel)

        datum = data[simLabel]

        cfg = specs.SimConfig(datum['simConfig'])
        cfg.createNEURONObj = False

        sim.initialize()  # create network object and set cfg and net params
        sim.loadAll('', data=datum, instantiate=False)
        sim.setSimCfg(cfg)
        try:
            print('Cells created: ' + str(len(sim.net.allCells)))
        except:
            print('Alternate sim loading...')
            sim.net.createPops()     
            sim.net.createCells()
            sim.setupRecording()
            sim.gatherData() 

        sim.allSimData = datum['simData']

        features = ['weight', 'delay', 'numConns', 'probability', 'strength', 'convergence', 'divergence']

        for feature in features:

            if save:
                saveFig = batchdatadir + '/' + batchLabel + '/' + 'connFig_' + feature + simLabel + '.png'
            else:
                saveFig = None

            sim.analysis.plotConn(includePre=includePre, includePost=includePost, feature=feature, orderBy=orderBy, figSize=figSize, groupBy=groupBy, groupByIntervalPre=groupByIntervalPre, groupByIntervalPost=groupByIntervalPost, graphType=graphType, synOrConn=synOrConn, synMech=synMech, connsFile=connsFile, tagsFile=tagsFile, clim=clim, fontSize=fontSize, saveData=saveData, saveFig=saveFig, showFig=showFig)



def plot_batch_ind_raster(batchLabel, batchdatadir='data', include=['allCells'], timeRange=None, maxSpikes=1e8, orderBy='gid', orderInverse=False, labels='legend', popRates=False, spikeHist=None, spikeHistBin=5, syncLines=False, figSize=(10,8), saveData=None, showFig=False, save=True, outputdir='batch_figs'):
    """Plots individual raster plots for each parameter combination."""

    from netpyne import specs

    if type(batchLabel) == str:
        params, data = batch_utils.load_batch(batchLabel, batchdatadir=batchdatadir)
    elif type(batchLabel) == tuple:
        batchLabel, params, data = batchLabel
    else:
        raise Exception()

    simLabels = data.keys()

    for simLabel in simLabels:

        print('Plotting sim: ' + simLabel)

        datum = data[simLabel]

        cfg = specs.SimConfig(datum['simConfig'])
        cfg.createNEURONObj = False

        sim.initialize()  # create network object and set cfg and net params
        sim.loadAll('', data=datum, instantiate=False)
        sim.setSimCfg(cfg)
        try:
            print('Cells created: ' + str(len(sim.net.allCells)))
        except:
            print('Alternate sim loading...')
            sim.net.createPops()     
            sim.net.createCells()
            sim.setupRecording()
            sim.gatherData() 

        sim.allSimData = datum['simData']

        if save:
            saveFig = batchdatadir + '/' + batchLabel + '/' + 'rasterFig' + simLabel + '.png'
        else:
            saveFig = None

        sim.analysis.plotRaster(include=include, timeRange=timeRange, maxSpikes=maxSpikes, orderBy=orderBy, orderInverse=orderInverse, labels=labels, popRates=popRates, spikeHist=spikeHist, spikeHistBin=spikeHistBin, syncLines=syncLines, figSize=figSize, saveData=saveData, saveFig=saveFig, showFig=showFig)




def plot_batch_ind_stats(batchLabel, batchdatadir='data', include=['allCells', 'eachPop'], statDataIn={}, timeRange=None, graphType='boxplot', stats=['rate', 'isicv'], bins=50, popColors=[], histlogy=False, histlogx=False, histmin=0.0, density=False, includeRate0=False, legendLabels=None, normfit=False, histShading=True, xlim=None, dpi=100, figSize=(6,8), fontSize=12, saveData=None, showFig=True, save=True, outputdir='batch_figs'):
    """Plots individual connectivity plots for each parameter combination."""

    from netpyne import specs

    if type(batchLabel) == str:
        params, data = batch_utils.load_batch(batchLabel, batchdatadir=batchdatadir)
    elif type(batchLabel) == tuple:
        batchLabel, params, data = batchLabel
    else:
        raise Exception()

    simLabels = data.keys()

    for simLabel in simLabels:

        print('Plotting sim: ' + simLabel)

        datum = data[simLabel]

        cfg = specs.SimConfig(datum['simConfig'])
        cfg.createNEURONObj = False

        sim.initialize()  # create network object and set cfg and net params
        sim.loadAll('', data=datum, instantiate=False)
        sim.setSimCfg(cfg)
        try:
            print('Cells created: ' + str(len(sim.net.allCells)))
        except:
            print('Alternate sim loading...')
            sim.net.createPops()     
            sim.net.createCells()
            sim.setupRecording()
            sim.gatherData() 

        sim.allSimData = datum['simData']

        if save:
            saveFig = batchdatadir + '/' + batchLabel + '/' + 'statFig_' + simLabel
        else:
            saveFig = None

        sim.analysis.plotSpikeStats(include=include, statDataIn=statDataIn, timeRange=timeRange, graphType=graphType, stats=stats, bins=bins, popColors=popColors, histlogy=histlogy, histlogx=histlogx, histmin=histmin, density=density, includeRate0=includeRate0, legendLabels=legendLabels, normfit=normfit, histShading=histShading, xlim=xlim, dpi=dpi, figSize=figSize, fontSize=fontSize, saveData=saveData, saveFig=saveFig, showFig=showFig)



simLabel = 'eee_net_25'

simPath = os.path.join('data', simLabel, simLabel + '.json')
sim.load(simPath, createNEURONObj=False)

#sim.analysis.plotTraces()

rasterFig, rasterData = sim.analysis.plotRaster(include=['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5' ], orderInverse=False)

syncFigPre, syncDataPre = sim.analysis.plotSpikeStats(include=['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5'], timeRange = [200, 400], graphType='boxplot', stats = ['sync'], figSize = (6,8), saveData = None, saveFig = None, showFig = True)

syncFigPlat, syncDataPlat = sim.analysis.plotSpikeStats(include=['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5'], timeRange = [800, 1000], graphType='boxplot', stats = ['sync'], figSize = (6,8), saveData = None, saveFig = None, showFig = True)

syncFigInput, syncDataInput = sim.analysis.plotSpikeStats(include=['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5'], timeRange = [1400, 1600], graphType='boxplot', stats = ['sync'], figSize = (6,8), saveData = None, saveFig = None, showFig = True)

syncFigPlatInput, syncDataPlatInput = sim.analysis.plotSpikeStats(include=['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5'], timeRange = [2000, 2200], graphType='boxplot', stats = ['sync'], figSize = (6,8), saveData = None, saveFig = None, showFig = True)


# Bar plot of synchrony

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


labels = ['Nothing', 'Plats', 'Inputs', 'Plats+Inputs']

PT51_sync = []
PT51_sync.append(syncDataPre['statData'][0][0])
PT51_sync.append(syncDataPlat['statData'][0][0])
PT51_sync.append(syncDataInput['statData'][0][0])
PT51_sync.append(syncDataPlatInput['statData'][0][0])

PT52_sync = []
PT52_sync.append(syncDataPre['statData'][1][0])
PT52_sync.append(syncDataPlat['statData'][1][0])
PT52_sync.append(syncDataInput['statData'][1][0])
PT52_sync.append(syncDataPlatInput['statData'][1][0])

PT53_sync = []
PT53_sync.append(syncDataPre['statData'][2][0])
PT53_sync.append(syncDataPlat['statData'][2][0])
PT53_sync.append(syncDataInput['statData'][2][0])
PT53_sync.append(syncDataPlatInput['statData'][2][0])

PT54_sync = []
PT54_sync.append(syncDataPre['statData'][3][0])
PT54_sync.append(syncDataPlat['statData'][3][0])
PT54_sync.append(syncDataInput['statData'][3][0])
PT54_sync.append(syncDataPlatInput['statData'][3][0])


x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width*(3/2), PT51_sync, width, label='PT5_1')
rects2 = ax.bar(x - width/(2), PT52_sync, width, label='PT5_2')
rects3 = ax.bar(x + width/(2), PT53_sync, width, label='PT5_3')
rects4 = ax.bar(x + width*(3/2), PT54_sync, width, label='PT5_4')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Synchrony')
ax.set_title('Synchrony by population and condition')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()




#batchLabel = 'v01_batch20'
#params, data = batch_utils.load_batch(batchLabel, batchdatadir=batchdatadir)
#batchData = (batchLabel, params, data)

#include = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5']
#plot_batch_ind_conn(batchData, includePre=include, includePost=include)

#plot_batch_ind_raster(batchData)

#stats = ['rate', 'isicv', 'sync', 'pairsync']
#plot_batch_ind_stats(batchData, stats=stats)

#stats = ['sync']
#timeRange = [200, 400]
#plot_batch_ind_stats(batchData, stats=stats, timeRange=timeRange)
#batch_analysis.plot_batch_raster(batchData)





## To load a single sim from file:
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

# plt.show()




