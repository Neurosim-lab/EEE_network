"""
cfg.py
"""

from netpyne import specs
cfg = specs.SimConfig()
import numpy as np
import os

#------------------------------------------------------------------------------
#
# SIMULATION CONFIGURATION
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------

cfg.duration = 2000 #ms
cfg.dt = 0.05 #don't do less than 0.05
cfg.hParams = {'celsius': 32}

cfg.verbose = 0
cfg.createNEURONObj = True
cfg.createPyStruct = True
cfg.cvode_active = False
cfg.cvode_atol = 1e-6
cfg.cache_efficient = True
cfg.checkErrors = True
cfg.seed_wiring = 4123
cfg.seeds = {'conn': cfg.seed_wiring,
			'stim': 1234, 
			'loc': 3214}
cfg.printPopAvgRates = True

cfg.scale = 1.0
cfg.sizeY = 1600
cfg.sizeX = 400
cfg.sizeZ = 300


#------------------------------------------------------------------------------
# Recording
#------------------------------------------------------------------------------
L5 = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4']
PT5 = [v for v in L5 if not v=='PV5']
plateau = [v for v in L5 if not v=='PV5']
8

cfg.cellsrec = 0
if cfg.cellsrec == 0:  #
	cfg.recordCells = ['all']
elif cfg.cellsrec == 1:  #
	cfg.recordCells = [(pop,5) for pop in L5]
elif cfg.cellsrec == 2:  # record selected cells
	cfg.recordCells = [(pop,5) for pop in L5]+[(pop,25) for pop in L5]
elif cfg.cellsrec == 3:  # record selected cells
	cfg.recordCells = [('PT5_1', 5), ('PV5', 0)]
elif cfg.cellsrec == 4:  # record selected cells
	cfg.recordCells = [] # doesn't record any cell


cfg.recordTraces = {'v_soma': {'sec':'soma_2', 'loc':0.5, 'var':'v'}}
#cfg.recordTraces['v_apical'] = {'sec':'apical_0', 'loc':0.5, 'var':'v'}
cfg.recordTraces['v_basal'] = {'sec':'basal_8', 'loc':0.5, 'var':'v'}


cfg.recordStims = False
cfg.recordStep = 0.1 #sampling rate, orig =1.0, 1=1khz, 0.1=10khz, 0.05=20khz


#------------------------------------------------------------------------------
# Saving
#------------------------------------------------------------------------------
cfg.simLabel = 'network_jwg_004'
cfg.saveFolder = os.path.join('batch_data', cfg.simLabel) #'../../data/v46'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']
cfg.backupCfgFile = None 
cfg.gatherOnlySimData = False
cfg.saveCellSecs = False
cfg.saveCellConns = False

#------------------------------------------------------------------------------
# Analysis and plotting
#------------------------------------------------------------------------------
cfg.cell_list = [5] #,45, 85, 125, 165] #,11,24,35] #plotmat gids of cells
analysisList = [() for i in range((len(PT5))-1)]
for k,v in enumerate(PT5): 
	if not k == 0: analysisList[k-1] = (v,range(0,40))

#cfg.analysis['plotRaster'] = {'include':[],'orderBy': 'gid','timeRange':[100,500], 'orderInverse':True,'saveFig': True, 'labels':'overlay','popRates': False, 'syncLines': False, 'figSize': (12,10),'showFig': True,'lw': 2.0,'marker': '|'}#, 'popColors': {'PT5':'red','PV5': 'blue'}}

cfg.analysis['plotRaster'] = {'include':[],'orderBy': 'gid', 'orderInverse':True,'saveFig': True, 'labels':'overlay','popRates': False, 'syncLines': False, 'figSize': (12,8),'showFig': True,'lw': 2.0,'marker': '|'}#, 'popColors': {'PT5':'red','PV5': 'blue'}}

cfg.analysis['plotTraces'] = {'include': [],'oneFigPer':'cell', 'colors': ['black'], 'figSize': (12,8),'saveFig': True ,'saveData': False,'showFig': False, 'ylim':[-100,30]} 

#cfg.analysis['plotConn'] = {'includePre':L5, 'includePost':L5,'feature': 'strength','synOrConn':'conn','synMech':['AMPA'],'groupBy': 'pop', 'saveFig': True, 'showFig': False}

#cfg.analysis['plot2Dnet'] = {'include': L5, 'view': 'xy', 'showConns': True, 'showFig': False, 'saveFig': True}

#cfg.analysis['plotSpikeStats'] = {'include':analysisList, 'timeRange': [200,500],'graphType':'boxplot','stats':['sync'],'saveFig': True , 'xlim': [0,1], 'showFig': False}


#------------------------------------------------------------------------------
# Cells
#------------------------------------------------------------------------------
cfg.singleCellPops = 0

#------------------------------------------------------------------------------
# Connections
#------------------------------------------------------------------------------
cfg.addConns = True

#------------------------------------------------------------------------------
# Parameter to control for Rm in all secs of eee7ps cell
#------------------------------------------------------------------------------
cfg.RmScale    = 1.0 #20.0
cfg.RaScale    = 0.7

#------------------------------------------------------------------------------
# Parameter to control for Ih in all secs of eee7ps cell
#------------------------------------------------------------------------------
cfg.ihScale     = 0.0 # Scales ih conductance

#------------------------------------------------------------------------------
# Parameter to control for vinit in all secs of eee7ps cell
#------------------------------------------------------------------------------
cfg.vinit_PT5 = -80 #-70

#------------------------------------------------------------------------------
# Sodium, potassium, and calcium conductance scaling
#------------------------------------------------------------------------------
cfg.allNaScale  = 1.2
cfg.dendNaScale = 1.0 # Scales dendritic Na conductance
cfg.dendKScale  = 1.0 # Scales dendritic K  conductance
cfg.dendCaScale = 1.0 # Scales dendritic Ca conductance

#------------------------------------------------------------------------------
# Parameters AMPA, NMDA, AMPA/NMDA ratio
#------------------------------------------------------------------------------


# DMS NMDA params
cfg.NMDAAlphaScale = 1.0   # Scales original value of 4.0
cfg.NMDABetaScale  = 14.0  # Scales original value of 0.0015
cfg.CdurNMDAScale  = 1.0   # Scales original value of 1.0
cfg.NMDAgmax       = 0.01
cfg.ratioAMPANMDA  = 4.0 
cfg.eNMDA		   = -10.0


# glutamate stim parameters
cfg.synTime           = 200.0
cfg.numSyns           = 24
cfg.numExSyns         = cfg.numSyns
cfg.glutAmp           = 2.0
cfg.glutAmpExSynScale = 1.0
cfg.glutAmpDecay      = 0.0 # percent/um
cfg.synLocMiddle      = 0.3 #0.45 
cfg.synLocRadius      = 0.15 
cfg.initDelay         = 10.0
cfg.synDelay          = 2.0 # ms/um
cfg.exSynDelay        = 4.0 # ms/um


#------------------------------------------------------------------------------
# Noise params
#------------------------------------------------------------------------------

cfg.noise = 1 #add synaptic noise to soma of PT5
cfg.noise_ptps = 0 # add noise as point process with addstim method

cfg.noise_tau = 1.0
cfg.noise_seed = [0,1,2,3,4,5,6,7,8,9,10] #different noise seed for different subset
cfg.e_inh_noise = cfg.vinit_PT5 - 10.0 #-2
cfg.e_exc_noise = cfg.vinit_PT5 + 60.0 #80
cfg.exc_noise_amp = 0.22 * 6.0
cfg.inh_noise_amp = 0.22 #*4.0


#------------------------------------------------------------------------------
# Synaptic weigth 
#------------------------------------------------------------------------------
cfg.EEgain = 1.0#0.0008 # basal dend 
cfg.IEgain = 0.001 #0.04    #PV to exc s
cfg.EIgain = 2.0 #0.15  # exc to PV
cfg.IIgain = 0.00012  #0.00001 #0.003   # PV to PV

cfg.ratioapical = [0.8, 0.2] #AMPA/NMDA ratio for apical dendrite * 4.0
cfg.ratiobdend = [0.666,0.334]# 2.0 AMPA/NMDA 

cfg.GABAAfast_e = -80
cfg.GABAAslow_e = -90

#------------------------------------------------------------------------------
# Long range inputs
#------------------------------------------------------------------------------
cfg.addLongConn = 1 #control all long connectivty, including glut stim 
cfg.longConnPT5 = 0
cfg.longConnPV5 = 1


cfg.numCellsLong = 500  # num of cells per population
cfg.noiseLong = 1.0   # firing rate random noise
cfg.delayLong = 1.0  # (ms)

cfg.weightLong =  0.0 #2.8  # to PT5 
cfg.weightLongInh = 3.0 #1.4 # to PV5

cfg.startLong = 0  # start at 0 ms
cfg.ratesLong = {'dTC':[80.0, 100.0]}#, 'HC':[40.0,80.0]}

#------------------------------------------------------------------------------
# NetStim inputs
#------------------------------------------------------------------------------

cfg.addNetStim = 1

cfg.secStim  = 'basal_9'#'apical_0'
cfg.synTime2 = 50
cfg.synTime3 = 250
cfg.intervalStim = 10
cfg.stimNumber2 = 5
cfg.glutAmp2 = 7.5
cfg.glutDelay = 1.0

cfg.Stim_2 = {'loc': 0.5, 'sec': cfg.secStim, 'synMech': ['NMDA','AMPA'], 'start': cfg.synTime2, 'interval': cfg.intervalStim, 'noise': 0.0, 'number': cfg.stimNumber2, 'weight': [cfg.glutAmp2, cfg.glutAmp2], 'delay': cfg.glutDelay}

cfg.Stim_3 = {'loc': 0.5, 'sec': cfg.secStim, 'synMech': ['NMDA','AMPA'], 'start': cfg.synTime3, 'interval': cfg.intervalStim, 'noise': 0.0, 'number': cfg.stimNumber2, 'weight': [cfg.glutAmp2, cfg.glutAmp2], 'delay': cfg.glutDelay}

cfg.NetStimSyn = {'loc': list(np.linspace(cfg.synLocMiddle-cfg.synLocRadius, cfg.synLocMiddle+cfg.synLocRadius, cfg.numSyns)), 'sec': 'basal_8', 'synMech': ['NMDA','AMPA'], 'start': cfg.synTime, 'interval': 1000, 'noise': 0.0, 'number': 1, 'weight': cfg.glutAmp, 'delay': cfg.synDelay}

cfg.NetStimExSyn = {'loc': list(np.linspace(cfg.synLocMiddle-cfg.synLocRadius, cfg.synLocMiddle+cfg.synLocRadius, cfg.numExSyns)), 'sec': 'basal_8', 'synMech': ['NMDA'], 'start': cfg.synTime, 'interval': 1000, 'noise': 0.0, 'number': 1, 'weight': cfg.glutAmp * cfg.glutAmpExSynScale, 'delay': cfg.exSynDelay}


#------------------------------------------------------------------------------
# Current inputs (IClamp)
#------------------------------------------------------------------------------
cfg.addIClamp = 0

ampl = 0.4
durat = 1000

cfg.IClamp1 = {'pop': 'PV5', 'sec': 'soma_2', 'loc': 0.5, 'start': 5, 'dur': durat, 'amp': ampl}


