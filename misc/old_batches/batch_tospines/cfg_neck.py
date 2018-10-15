"""
cfg.py 

Simulation configuration 

Contributors: salvadordura@gmail.com
"""

from netpyne import specs
import numpy as np

cfg = specs.SimConfig()  

###############################################################################
#
# SIMULATION CONFIGURATION
#
###############################################################################

cfg.checkErrors = True

###############################################################################
# Run parameters
###############################################################################
cfg.duration = 1200 
cfg.dt = 0.05
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 34, 'v_init': -80}  
cfg.verbose = 0
cfg.cvode_active = False
cfg.printRunTime = 0.1
cfg.printPopAvgRates = True


###############################################################################
# Recording 
###############################################################################
cfg.recordTraces = {'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'}}
cfg.recordTraces['V_Bdend1'] = {'sec': 'Bdend1', 'loc': 0.5, 'var': 'v'}
cfg.recordTraces['V_Bdend2'] = {'sec': 'Bdend2', 'loc': 0.5, 'var': 'v'}
cfg.recordCells = ['eee7us', 'eee7ps']
cfg.recordStims = False  
cfg.recordStep = 0.1 


###############################################################################
# Saving
###############################################################################
cfg.simLabel = 'tospines'
cfg.saveFolder = 'batch_data'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']


###############################################################################
# Analysis and plotting 
###############################################################################
cfg.analysis['plotTraces'] = {'include': ['all'], 'oneFigPer': 'cell', 'saveFig': True, 
                              'showFig': False, 'figSize': (10,8), 'timeRange': [0,cfg.duration]}


###############################################################################
# Parameters
###############################################################################
cfg.dendNa = 0.00345 

cfg.tau1NMDA = 15
cfg.tau2NMDA = 600

cfg.BdendRa = 114.510490019

cfg.ratioAMPANMDA = 0.2
cfg.weightNMDA = 0.012 

cfg.dendK = 1.0

cfg.numsyns = 1
cfg.synsecs = 'neck_1'
cfg.synlocs = 0.00001
#cfg.synsecs = 'head_1'
#cfg.synlocs = 0.99999

###############################################################################
# Current inputs 
###############################################################################
cfg.addIClamp = 1

#cfg.IClamp1 = {'pop': 'PT5B', 'sec': 'soma', 'loc': 0.5, 'start': 200, 'dur': 1000, 'amp': 0.0}
cfg.IClamp1 = {'pop': ['SPI6', 'eee6', 'eee7', 'eee7us', 'eee7ps'], 'sec': 'soma', 'loc': 0.5, 'start': 200, 'dur': 1000, 'amp': 0.0}


###############################################################################
# NetStim inputs 
###############################################################################
cfg.addNetStim = 1

cfg.NetStim1 = {'pop': ['eee7us', 'eee7ps'], 'sec': cfg.synsecs, 'synsPerConn': cfg.numsyns, 'loc': cfg.synlocs, 'synMech': ['NMDA','AMPA'], 'start': 200, 'interval': 1000, 'noise': 0.0, 'number': 1, 'weight': [cfg.weightNMDA/cfg.numsyns, cfg.weightNMDA*cfg.ratioAMPANMDA/cfg.numsyns], 'delay': 1}

