from netpyne import specs, sim
import os

cfg = specs.SimConfig()
cfg.simLabel = 'poirazi_17'
cfg.saveFolder = os.path.join('output', cfg.simLabel)

saveFigs = True
showFigs = False

cfg.duration = 2000 #6000
cfg.dt = 0.025
cfg.verbose = True
cfg.hParams.celsius = 34.0
cfg.recordStep = 0.1


## Plotting

cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc':0.5, 'var':'v'}}
cfg.printPopAvgRates = True

cfg.analysis['plotRaster'] = {'saveFig': saveFigs, 'showFig': showFigs}
cfg.analysis['plotTraces'] = {'include': ['all'], 'saveFig': saveFigs, 'showFig': showFigs}
cfg.analysis['plot2Dnet']  = {'saveFig': saveFigs, 'showFig': showFigs}
cfg.analysis['plotConn']   = {'saveFig': saveFigs, 'showFig': showFigs, 'feature': 'strength'}


# Stimulation parameters

cfg.stimNumber = 90
cfg.stimAMPAweight = 0.00024
cfg.stimNMDAweight = 0.22


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
cfg.PyrInhGABAaWeight = 7.5e-4
cfg.PyrInhGABAbWeight = 3.2e-4

# inhibitory -> inhibitory
cfg.numSynsInhInh = 12
cfg.InhInhGABAaWeight = 5.1e-4


## Resting membrane potential
cfg.pyrEpas = -66.0
cfg.inhEpas = -70.0


## Noise
cfg.pyrExcNoiseE = cfg.pyrEpas + 65.0     # Default E_e : 0.0
cfg.pyrInhNoiseE = cfg.pyrEpas - 10.0     # Default E_i : -75.0
cfg.inhExcNoiseE = cfg.inhEpas + 65.0     # Default E_e : 0.0
cfg.inhInhNoiseE = cfg.inhEpas - 10.0     # Default E_i : -75.0


## Current injection

cfg.pyrInject = True
cfg.pyrInjectDel = 1000
cfg.pyrInjectDur = 500
cfg.pyrInjectAmp = 1.5
cfg.pyrInjectSec = 'soma'
cfg.pyrInjectLoc = 0.5



