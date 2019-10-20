import batch_utils
import batch_analysis
import matplotlib.pyplot as plt
from netpyne import sim
from itertools import product
import numpy as np
import os
plt.ion()

batchdatadir = "batch_data"


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

def plot_batch_ind_conn(batchLabel, batchdatadir=batchdatadir, includePre = ['all'], includePost = ['all'], feature = 'strength', orderBy = 'gid', figSize = (10,10), groupBy = 'pop', groupByIntervalPre = None, groupByIntervalPost = None, graphType = 'matrix', synOrConn = 'syn', synMech = None, connsFile = None, tagsFile = None, clim = None, fontSize = 12, saveData = None, showFig = False, save=True, outputdir='batch_figs'):
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



def plot_batch_ind_raster(batchLabel, batchdatadir=batchdatadir, include=['allCells'], timeRange=None, maxSpikes=1e8, orderBy='gid', orderInverse=False, labels='legend', popRates=False, spikeHist=None, spikeHistBin=5, syncLines=False, figSize=(10,8), saveData=None, showFig=False, save=True, outputdir='batch_figs'):
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




def plot_batch_ind_stats(batchLabel, batchdatadir=batchdatadir, include=['allCells', 'eachPop'], statDataIn={}, timeRange=None, graphType='boxplot', stats=['rate', 'isicv'], bins=50, popColors=[], histlogy=False, histlogx=False, histmin=0.0, density=False, includeRate0=False, legendLabels=None, normfit=False, histShading=True, xlim=None, dpi=100, figSize=(6,8), fontSize=12, saveData=None, showFig=True, save=True, outputdir='batch_figs'):
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



def plotSimSync(simPath='data', simLabel='eee_net_25', showFigs=False, batchLabel=None):

    if not batchLabel:
        simPath = os.path.join(simPath, simLabel, simLabel + '.json')
        sim.load(simPath, createNEURONObj=False)
    else:
        simPath = os.path.join(simPath, batchLabel, simLabel + '.json')
        sim.load(simPath, createNEURONObj=False)

    #sim.analysis.plotTraces()

    rasterFig, rasterData = sim.analysis.plotRaster(include=['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5' ], orderInverse=False)

    syncFigPre, syncDataPre = sim.analysis.plotSpikeStats(include=['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5'], timeRange = [200, 400], graphType='boxplot', stats = ['sync'], figSize = (6,8), saveData = None, saveFig = None, showFig = showFigs)

    syncFigPlat, syncDataPlat = sim.analysis.plotSpikeStats(include=['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5'], timeRange = [800, 1000], graphType='boxplot', stats = ['sync'], figSize = (6,8), saveData = None, saveFig = None, showFig = showFigs)

    syncFigInput, syncDataInput = sim.analysis.plotSpikeStats(include=['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5'], timeRange = [1400, 1600], graphType='boxplot', stats = ['sync'], figSize = (6,8), saveData = None, saveFig = None, showFig = showFigs)

    syncFigPlatInput, syncDataPlatInput = sim.analysis.plotSpikeStats(include=['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5'], timeRange = [2000, 2200], graphType='boxplot', stats = ['sync'], figSize = (6,8), saveData = None, saveFig = None, showFig = showFigs)


    # Bar plot of synchrony
    labels = ['Control', 'Plats', 'Inputs', 'Plats+Inputs']

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
    rects1 = ax.bar(x - width*(3/2), PT51_sync, width, label='PT5_1 (+P+I)')
    rects2 = ax.bar(x - width/(2), PT52_sync, width, label='PT5_2 (+P-I)')
    rects3 = ax.bar(x + width/(2), PT53_sync, width, label='PT5_3 (-P+I)')
    rects4 = ax.bar(x + width*(3/2), PT54_sync, width, label='PT5_4 (-P-I)')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Synchrony')
    ax.set_title('Synchrony by population and condition')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()

    outputData = [PT51_sync, PT52_sync, PT53_sync, PT54_sync]
    return outputData

#plotSimSync(simLabel='eee_net_23')


def plotBatchSync(batchPath='batch_data', batchLabel='v01_batch25'):

    batchPathFiles = os.listdir(os.path.join(batchPath, batchLabel))

    simFiles = [file for file in batchPathFiles if file.endswith('.json')]
    simFiles = [file for file in simFiles if not file.endswith('cfg.json')]
    simFiles = [file for file in simFiles if not file.endswith('batch.json')]
    simFiles.sort()

    syncData = []

    for simFile in simFiles:

        simFile = simFile.split('.')[0]
        output = plotSimSync(simPath=batchPath, simLabel=simFile, showFigs=False, batchLabel=batchLabel)
        # output = [PT51_sync, PT52_sync, PT53_sync, PT54_sync]

        syncData.append(output)

    syncData = np.array(syncData)

    labels = ['Control', 'Plats', 'Inputs', 'Plats+Inputs']
    
    sdmean = np.mean(syncData, axis=0)
    sdstdv = np.std(syncData, axis=0)

    PT51_sync = sdmean[0,:]
    PT52_sync = sdmean[1,:]
    PT53_sync = sdmean[2,:]
    PT54_sync = sdmean[3,:]

    PT51_stdv = sdstdv[0,:]
    PT52_stdv = sdstdv[1,:]
    PT53_stdv = sdstdv[2,:]
    PT54_stdv = sdstdv[3,:]

    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width*(3/2), PT51_sync, yerr=PT51_stdv, width=width, label='PT5_1 (+P+I)')
    rects2 = ax.bar(x - width/(2), PT52_sync, yerr=PT52_stdv, width=width, label='PT5_2 (+P–I)')
    rects3 = ax.bar(x + width/(2), PT53_sync, yerr=PT53_stdv, width=width, label='PT5_3 (–P+I)')
    rects4 = ax.bar(x + width*(3/2), PT54_sync, yerr=PT54_stdv, width=width, label='PT5_4 (–P–I)')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Synchrony')
    ax.set_title('Synchrony by population and condition')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()

    return syncData


#syncData = plotBatchSync(batchLabel='v01_batch26')

#batch_analysis.plot_vtraces('v01_batch26')



### Detecting plateaus

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n



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




def plotBatchConn(batchPath='batch_data', batchLabel='v01_batch48', feature='all'):

    batchPath = os.path.join(batchPath, batchLabel)
    batchPathFiles = os.listdir(batchPath)

    simFiles = [file for file in batchPathFiles if file.endswith('.json')]
    simFiles = [file for file in simFiles if not file.endswith('cfg.json')]
    simFiles = [file for file in simFiles if not file.endswith('batch.json')]
    simFiles.sort()

    includePre  = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4','PV5']
    includePost = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4','PV5']
    features    = ['numConns', 'divergence', 'convergence', 'weight', 'probability', 'strength'] 
    groupBy     = 'pop'
    orderBy     = 'gid'

    EEmean = {}
    EImean = {}
    IEmean = {}
    IImean = {}
    EEstd = {}
    EIstd = {}
    IEstd = {}
    IIstd = {}

    if feature == 'all':

        for feature in features:

            EEmean[feature] = []
            EImean[feature] = []
            IEmean[feature] = []
            IImean[feature] = []
            EEstd[feature] = []
            EIstd[feature] = []
            IEstd[feature] = []
            IIstd[feature] = []

    for simFile in simFiles:

        simPath = os.path.join('batch_data', batchLabel, simFile)
        sim.load(simPath, createNEURONObj=False)

        for feature in features:   

            (fig, output) = sim.analysis.plotConn(includePre=includePre, includePost=includePost, feature=feature, groupBy=groupBy, orderBy=orderBy, showFig=False)
    
            connMatrix = output['connMatrix']

            EEmean[feature].append(np.mean(connMatrix[0:4, 0:4]))
            EImean[feature].append(np.mean(connMatrix[0:4, 4:5]))
            IEmean[feature].append(np.mean(connMatrix[4:5, 0:4]))
            IImean[feature].append(np.mean(connMatrix[4:5, 4:5]))

            EEstd[feature].append(np.std(connMatrix[0:4, 0:4]))
            EIstd[feature].append(np.std(connMatrix[0:4, 4:5]))
            IEstd[feature].append(np.std(connMatrix[4:5, 0:4]))
            IIstd[feature].append(np.std(connMatrix[4:5, 4:5]))

    for feature in features:

        labels = ['10', '100', '500', '1000', '5000']  

        x = np.arange(len(labels))  # the label locations
        width = 0.2  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width*(3/2), EEmean[feature], yerr=EEstd[feature], width=width, label='E->E')
        rects2 = ax.bar(x - width/(2), EImean[feature], yerr=EIstd[feature], width=width, label='E->I')
        rects3 = ax.bar(x + width/(2), IEmean[feature], yerr=IEstd[feature], width=width, label='I->E')
        rects4 = ax.bar(x + width*(3/2), IImean[feature], yerr=IIstd[feature], width=width, label='I->I')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Connectivity ' + feature)
        ax.set_title('Connectivity ' + feature)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_xlabel('Number of Cells')
        ax.legend()

        fig.tight_layout()

    return

#output = plotBatchConn()

