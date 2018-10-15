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
cfg.duration = 1000 #1200
cfg.dt = 0.05
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 32}  
cfg.verbose = 0
cfg.cvode_active = False
cfg.printRunTime = 0.1
cfg.printPopAvgRates = True


###############################################################################
# Recording 
###############################################################################
cfg.recordTraces = {'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'}}
cfg.recordTraces['V_Bdend1'] = {'sec': 'Bdend1', 'loc': 0.5, 'var': 'v'}
#cfg.recordTraces['V_Bdend2'] = {'sec': 'Bdend2', 'loc': 0.5, 'var': 'v'}
#cfg.recordTraces['V_spine'] = {'sec': 'head_55', 'loc': 0.5, 'var': 'v'}

#cfg.recordTraces['g_NMDA'] = {'sec': 'head_55', 'loc': 0.99999, 'synMech': 'NMDA', 'var': 'g'}
#cfg.recordTraces['i_NMDA'] = {'sec': 'head_55', 'loc': 0.99999, 'synMech': 'NMDA', 'var': 'iNMDA'}
#cfg.recordTraces['i_Ca'] = {'sec': 'head_55', 'loc': 0.99999, 'synMech': 'NMDA', 'var': 'ica'}


#cfg.recordCells = ['eee7us', 'eee7ps']
cfg.recordCells = ['eee7']
cfg.recordStims = False  
cfg.recordStep = 0.1 


###############################################################################
# Saving
###############################################################################
cfg.simLabel = 'batch_20180207'
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

# Sodium and potassium conductance scaling
cfg.dendNaScale = 1.0 # Scales dendritic Na conductance
cfg.dendKScale  = 1.0 # Scales dendritic K  conductance
cfg.allNaScale  = 1.0 # Scales all Na conductances (overrides dendNaScale if not commented)
cfg.allKScale   = 1.0 # Scales all K  conductances (overrides dendKScale  if not commented)

# DMS NMDA params
cfg.NMDAAlphaScale = 1.0 # Scales original value of 4.0
cfg.NMDABetaScale  = 3.0 # Scales original value of 0.0015
cfg.CdurNMDAScale  = 1.0 # Scales original value of 1.0
cfg.CmaxNMDAScale  = 1.0 # Scales original value of 1.0
cfg.NMDAgmax       = 0.05
cfg.ratioAMPANMDA  = 2.0
cfg.NMDARev        = 0.0 # Reversal potential (originally 0)

# glutamate stim parameters
cfg.glutAmp    = 1.3   #0.8   # weight supplied to NMDAr and AMPAr 
cfg.glutLoc    = 0.28  # fraction of branch, not microns (0.28 head number 55)
cfg.glutSpread = 0.7   # microns, diameter of glutamate puff (0.7 only one head)
cfg.glutDelay  = 0.0   # ms/um delay in glutamate activation
cfg.glutDecay  = 0.0   # %/um decrease in glutamate amplitude 
 
# spillover params
cfg.spillDelay    = 10.0 # (ms) time to reach dendritic shaft
cfg.spillFraction = 0.0  # (%)  percent of glutamate weight that reaches shaft

# other params
cfg.RmScale       = 1.0  # Scales membrane resistance in all secs
cfg.ampIClamp1    = 3.0  # amplitude of current clamp
cfg.durIClamp1    = 1.0
cfg.e_pas         = -80.0 # resting membrane potential
cfg.ihScale       = 0.0   # Scales ih conductance
cfg.gpasSomaScale = 1.0 # Scales soma g_pas
cfg.Rneck         = 90.0
cfg.dendRaScale   = 1.0
cfg.dendRmScale   = 1.0
cfg.mgSlope       = 0.062 # Mg block slope from NMDAeee.mod

###############################################################################
# NetStim inputs 
###############################################################################
cfg.addNetStim = True

# cfg.NetStim1 = {'pop': ['eee7ps'], 'loc': 0.99999, 'sec': 'spineheads', 'synMech': ['NMDA','AMPA'], 'start': 100, 'interval': 1000, 'noise': 0.0, 'number': 1, 'weight': [cfg.glutAmp, cfg.glutAmp], 'delay': cfg.glutDelay}

cfg.NetStim2 = {'pop': ['eee7'], 'loc': cfg.glutLoc, 'sec': 'Bdend1', 'synMech': ['NMDA','AMPA'], 'start': 100, 'interval': 1000, 'noise': 0.0, 'number': 1, 'weight': [cfg.glutAmp, cfg.glutAmp], 'delay': cfg.glutDelay}


###############################################################################
# Current inputs 
###############################################################################
cfg.addIClamp = False
