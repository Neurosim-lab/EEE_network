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
netParams.synMechParams['GLU']        = {'mod': 'ampa'}
netParams.synMechParams['GLUIN']      = {'mod': 'ampain'}
netParams.synMechParams['GABAa']      = {'mod': 'gabaa'}
netParams.synMechParams['GABAain']    = {'mod': 'gabaain'}
netParams.synMechParams['GABAb']      = {'mod': 'gabab'}
netParams.synMechParams['NMDA']       = {'mod': 'NMDA'}
netParams.synMechParams['nmda_spike'] = {'mod': 'NMDA_syn'}
netParams.synMechParams['SinClamp']   = {'mod': 'sinclamp'}

## Connectivity

# # pyr --> pyr
# for prePop in EPops:
#     for postPop in EPops:
#         ruleLabel = prePop+'->'+postPop
#         netParams.connParams[ruleLabel] = {
#             'preConds': {'pop': prePop},
#             'postConds': {'pop': postPop},
#             'synMech': ESynMech, 
#             'weight': [cfg.AMPAweight, cfg.NMDAweight],
#             'delay': 'defaultDelay', #'defaultDelay+dist_3D/propVelocity',
#             cfg.connType: EEconn,
#             'loc': 0.3,
#             'sec': 'basal_8'} #,
#             #'synsPerConn': 'int(uniform(1,' + str(cfg.EEspc) + '))'}

# # Excitatory --> Inhibitory
# for prePop in EPops:
#     for postPop in IPops:
#         ruleLabel = prePop+'->'+postPop
#         netParams.connParams[ruleLabel] = {
#             'preConds': {'pop': prePop},
#             'postConds': {'pop': postPop},
#             'synMech': 'AMPA',
#             'weight': cfg.AMPAweight, 
#             'delay': 'defaultDelay', #'defaultDelay+dist_3D/propVelocity',
#             cfg.connType: EIconn,
#             'loc': 0.5,
#             'sec': 'soma'} #,
#             #'synsPerConn': 'int(uniform(1,' + str(cfg.EIspc) + '))'}

# # Inhibitory --> Excitatory
# for prePop in IPops:
#     for postPop in EPops:
#         ruleLabel = prePop+'->'+postPop
#         netParams.connParams[ruleLabel] = {
#             'preConds': {'pop': prePop},
#             'postConds': {'pop': postPop},
#             'synMech': ISynMech, 
#             'weight': [cfg.GABAAfastWeight, cfg.GABAAslowWeight],
#             'delay': 'defaultDelay', #'defaultDelay+dist_3D/propVelocity',
#             cfg.connType: IEconn,
#             'loc': 0.5,
#             'sec': 'soma'} #,
#             #'synsPerConn': 'int(uniform(1,' + str(cfg.IEspc) + '))'}

# # Inhibitory --> Inhibitory
# for prePop in IPops:
#     for postPop in IPops:
#         ruleLabel = prePop+'->'+postPop
#         netParams.connParams[ruleLabel] = {
#             'preConds': {'pop': prePop},
#             'postConds': {'pop': postPop},
#             'synMech': 'GABAAfast',
#             'weight': cfg.GABAAfastWeight, 
#             'delay': 'defaultDelay', #'defaultDelay+dist_3D/propVelocity',
#             cfg.connType: IIconn,
#             'loc': 0.5,
#             'sec': 'soma'} #,
#             #'synsPerConn': 'int(uniform(1,' + str(cfg.IIspc) + '))'}





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






