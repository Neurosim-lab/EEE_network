from netpyne import specs, sim
import os

cfg = specs.SimConfig()
cfg.simLabel = 'poirazi_36'
cfg.saveFolder = os.path.join('output', cfg.simLabel)

saveFigs = True
showFigs = False

cfg.duration = 2000
cfg.dt = 0.025
cfg.verbose = True
cfg.hParams.celsius = 34.0
cfg.recordStep = 0.1


## Number of cells (80% pyr, 20% inh)
cfg.numCells = 20


## Saving data
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']


## Plotting
cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc':0.5, 'var':'v'},
					'V_dend': {'sec':'dend_0', 'loc':0.5, 'var':'v'}}
cfg.recordCells = [('pyrs', [0,1]), ('pyrs_plat', [0,1]), ('inhs', [0,1])]
cfg.analysis['plotRaster'] = {'saveFig': saveFigs, 'showFig': showFigs, 'orderInverse': True, 'popRates': True}
cfg.analysis['plotTraces'] = {'saveFig': saveFigs, 'showFig': showFigs, 'overlay': True}
#cfg.analysis['plot2Dnet']  = {'saveFig': saveFigs, 'showFig': showFigs}
cfg.analysis['plotConn']   = {'saveFig': saveFigs, 'showFig': showFigs, 'includePre': ['pyrs_plat', 'pyrs', 'inhs'], 'includePost': ['pyrs_plat', 'pyrs', 'inhs'], 'feature': 'strength'}  # strength, numConns

cfg.analysis['plotSpikeStats'] = {'saveFig': saveFigs, 'showFig': showFigs, 'include': ['eachPop'], 'graphType': 'boxplot', 'stats': ['rate', 'isicv', 'sync', 'pairsync'], 'timeRange': [1250, 1500]} 


# Stimulation parameters
cfg.glutStim       = True
cfg.stimNumber     = 25
cfg.stimAMPAweight = 0.00024
cfg.stimNMDAweight = 0.22
cfg.stimScale      = 50.0
cfg.stimTime       = 1200


## Connectivity 

# pyramidal -> pyramidal
cfg.numSynsPyrPyr = 5
cfg.PyrPyrAMPAweight = 0.00019
cfg.PyrPyrNMDAweight = 0.585

# pyramidal -> inhibitory
cfg.numSynsPyrInh = 2
cfg.PyrInhAMPAweight = 7.5e-4
cfg.PyrInhNMDAweight = 3.2e-4

# inhibitory -> pyramidal
cfg.numSynsInhPyr = 4
cfg.PyrInhGABAaWeight = 6.9e-4 
cfg.PyrInhGABAbWeight = 1.05e-4

# inhibitory -> inhibitory
cfg.numSynsInhInh = 12
cfg.InhInhGABAaWeight = 5.1e-4


## Resting membrane potential
cfg.pyrEpas = -66.0
cfg.inhEpas = -70.0


## Noise
cfg.noise = True
cfg.noiseScale = 0.1
cfg.pyrExcNoiseE = cfg.pyrEpas + 65.0     # Default E_e : 0.0
cfg.pyrInhNoiseE = cfg.pyrEpas - 10.0     # Default E_i : -75.0
cfg.inhExcNoiseE = cfg.inhEpas + 65.0     # Default E_e : 0.0
cfg.inhInhNoiseE = cfg.inhEpas - 10.0     # Default E_i : -75.0


## Current injection

cfg.pyrInject = True
cfg.pyrInjectDel = 200
cfg.pyrInjectDur = 250
cfg.pyrInjectAmp = 0.34
cfg.pyrInjectSec = 'soma'
cfg.pyrInjectLoc = 0.5



