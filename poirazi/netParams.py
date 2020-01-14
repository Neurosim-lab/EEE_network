from netpyne import specs, sim
import os

try:
    from __main__ import cfg
except:
    from cfg import cfg

netParams = specs.NetParams()


## Population parameters

numPyrCells = 8
numInhCells = 2

netParams.popParams['pyrs'] = {'cellType': 'pyr', 'numCells': numPyrCells}
netParams.popParams['inhs'] = {'cellType': 'inh', 'numCells': numInhCells}


## Set path to cells directory

cellpath = 'cells'
pyrPath  = os.path.join(cellpath, 'pyr.py')
inhPath  = os.path.join(cellpath, 'inh.py')


## Import cells

netParams.cellParams['pyr'] = netParams.importCellParams(label='pyr', conds={'pop':'pyrs'}, fileName=pyrPath, cellName='makeCell', cellInstance=True)
netParams.cellParams['inh'] = netParams.importCellParams(label='inh', conds={'pop':'inhs'}, fileName=inhPath, cellName='makeCell', cellInstance=True)


## Synaptic mechanisms

netParams.synMechParams['GLU']        = {'mod': 'GLU'}          # ampa.mod
netParams.synMechParams['GLUIN']      = {'mod': 'GLUIN'}        # ampain.mod
netParams.synMechParams['GABAa']      = {'mod': 'GABAa'}        # gabaa.mod
netParams.synMechParams['GABAain']    = {'mod': 'GABAain'}      # gabaain.mod
netParams.synMechParams['GABAb']      = {'mod': 'GABAb'}        # gabab.mod
netParams.synMechParams['NMDA']       = {'mod': 'NMDA'}         # NMDA.mod
netParams.synMechParams['nmda_spike'] = {'mod': 'nmda_spike'}   # NMDA_syn.mod
netParams.synMechParams['SinClamp']   = {'mod': 'SinClamp'}     # sinclamp.mod


## Stimulation

netParams.stimSourceParams['stimulation'] = {
    'type'    : 'NetStim', 
    'start'   : 0, 
    'interval': 50, 
    'number'  : 10,
    'noise'   : 0}
    
ruleLabel = 'stimulation->pyrs'
netParams.stimTargetParams[ruleLabel] = {
    'source'   : 'stimulation', 
    'conds'    : {'pop': 'pyrs'}, 
    'sec'      : 'dend_1', 
    'loc'      : 0.5, 
    'synMech'  : ['GLU', 'nmda_spike'], 
    'weight'   : [cfg.stimAMPAweight, cfg.stimNMDAweight], 
    'delay'    : 500,
    'threshold': -20}


## Noise






## Connectivity

# pyrs --> pyrs
ruleLabel = 'pyrs->pyrs'
netParams.connParams[ruleLabel] = {
    'preConds'   : {'pop': 'pyrs'},
    'postConds'  : {'pop': 'pyrs'},
    'synMech'    : ['GLU', 'nmda_spike'], 
    'weight'     : [cfg.PyrPyrAMPAweight, cfg.PyrPyrNMDAweight],
    'delay'      : 'max(0.38, normal(1.7, 0.9))',
    'probability': 1.0,
    'loc'        : [1.0, 1.0],
    'sec'        : 'dend_0',
    'synsPerConn': cfg.numSynsPyrPyr,
    'threshold'  : -20}

# pyrs --> inhs
ruleLabel = 'pyrs->inhs'
netParams.connParams[ruleLabel] = {
    'preConds'   : {'pop': 'pyrs'},
    'postConds'  : {'pop': 'inhs'},
    'synMech'    : ['GLUIN', 'NMDA'], 
    'weight'     : [cfg.PyrInhAMPAweight, cfg.PyrInhNMDAweight],
    'delay'      : 'max(0.38, normal(0.6, 0.2))',
    'probability': 1.0,
    'loc'        : [0.5, 0.5],
    'sec'        : 'soma',
    'synsPerConn': cfg.numSynsPyrInh,
    'threshold'  : -20}

# inhs --> pyrs
ruleLabel = 'inhs->pyrs'
netParams.connParams[ruleLabel] = {
    'preConds'   : {'pop': 'inhs'},
    'postConds'  : {'pop': 'pyrs'},
    'synMech'    : ['GABAa', 'GABAb'], 
    'weight'     : [cfg.PyrInhGABAaWeight, cfg.PyrInhGABAbWeight],
    'delay'      : 'max(0.38, normal(1.8, 0.8))',
    'probability': 1.0,
    'loc'        : [0.5, 0.5],
    'sec'        : 'soma',
    'synsPerConn': cfg.numSynsInhPyr,
    'threshold'  : -20}

# inhs --> inhs
ruleLabel = 'inhs->inhs'
netParams.connParams[ruleLabel] = {
    'preConds'   : {'pop': 'inhs'},
    'postConds'  : {'pop': 'inhs'},
    'synMech'    : ['GABAain'], 
    'weight'     : [cfg.InhInhGABAaWeight],
    'delay'      : 'max(0.38, normal(1.76, 0.07))',
    'probability': 1.0,
    'loc'        : [0.5],
    'sec'        : 'soma',
    'synsPerConn': cfg.numSynsInhInh,
    'threshold'  : -20}



# if cfg.addCommonInput1:

#     netParams.stimSourceParams['CommonInput1'] = {'type': 'NetStim', 'start': cfg.delCommonInput1, 'interval': cfg.intCommonInput1, 'number': cfg.numCommonInput1}
                  
#     for postPop in cfg.popCommonInput1:             
        
#         ruleLabel = 'CommonInput1->'+postPop
#         netParams.stimTargetParams[ruleLabel] = {
#             'source' : 'CommonInput1', 
#             'conds'  : {'pop': postPop}, 
#             'sec'    : cfg.secCommonInput1, 
#             'loc'    : cfg.locCommonInput1, 
#             'synMech': ['AMPA', 'NMDA'], 
#             'weight' : cfg.wgtCommonInput1, 
#             'delay'  : 0.0}






