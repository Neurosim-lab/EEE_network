from netpyne import specs, sim
import os

cfg = specs.SimConfig()
cfg.simLabel = 'poirazi_02'
cfg.saveFolder = os.path.join('output', cfg.simLabel)

saveFigs = True
showFigs = False

cfg.duration = 1000
cfg.dt = 0.025
cfg.verbose = True
cfg.hParams.celsius = 34.0

cfg.recordStep = 0.1
cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc':0.5, 'var':'v'}}

cfg.analysis['plotRaster'] = {'saveFig': saveFigs, 'showFig': showFigs}
cfg.analysis['plotTraces'] = {'include': ['all'], 'saveFig': saveFigs, 'showFig': showFigs}
cfg.analysis['plot2Dnet']  = {'saveFig': saveFigs, 'showFig': showFigs}

# Stimulation parameters
cfg.stimNumber = 90
cfg.stimAMPAweight = 0.00024
cfg.stimNMDAweight = 0.22