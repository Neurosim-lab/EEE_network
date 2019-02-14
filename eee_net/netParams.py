from netpyne import specs
import os
import copy
try:
    from __main__ import cfg
except:
    from cfg import cfg


## Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

netParams.sizeX = 100 # x-dimension (horizontal length) size in um
netParams.sizeY = 1000 # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = 100 # z-dimension (horizontal length) size in um
netParams.propVelocity = 100.0 # propagation velocity (um/ms)
netParams.probLengthConst = 150.0 # length constant for conn probability (um)


## Population parameters
netParams.popParams['PT5_1'] = {'cellType': 'PT5', 'numCells': int(cfg.numPT5cells/4), 'ynormRange': cfg.ynormRange, 'cellModel': 'HH'}
netParams.popParams['PT5_2'] = {'cellType': 'PT5', 'numCells': int(cfg.numPT5cells/4), 'ynormRange': cfg.ynormRange, 'cellModel': 'HH'}
netParams.popParams['PT5_3'] = {'cellType': 'PT5', 'numCells': int(cfg.numPT5cells/4), 'ynormRange': cfg.ynormRange, 'cellModel': 'HH'}
netParams.popParams['PT5_4'] = {'cellType': 'PT5', 'numCells': int(cfg.numPT5cells/4), 'ynormRange': cfg.ynormRange, 'cellModel': 'HH'}
netParams.popParams['PV5'] = {'cellType': 'PV5', 'numCells': cfg.numPV5cells, 'ynormRange': cfg.ynormRange, 'cellModel': 'HH'}


## Set path to cells directory
cellpath = '../cells'
eeeS_path = os.path.join(cellpath, 'eeeS.py')
PV_path   = os.path.join(cellpath, 'FS3.hoc')


## Import PV5 cell
cellRule = netParams.importCellParams(label='PV5', conds={'cellType':'PV5'}, fileName=PV_path, cellName='FScell1', cellInstance=True)
netParams.cellParams['PV5'] = cellRule

## Import eeeS cell (PT5)
cellRule = netParams.importCellParams(label='PT5_1', conds={'pop':'PT5_1'}, fileName=eeeS_path, cellName='MakeCell', cellInstance=True)
netParams.cellParams['PT5_1'] = cellRule

## Then copy the cellRule for the other pops (faster than importing again)
## Note: we are creating 1 cell type per pop because they could potentially have different noise and connectivity params           
for label in ['PT5_2', 'PT5_3', 'PT5_4']:    
    cellRule = copy.deepcopy(netParams.cellParams['PT5_1'].todict())
    cellRule['conds']['pop'] = [label]
    netParams.cellParams[label] = cellRule


## Synaptic mechanism parameters
ESynMech = ['AMPA','NMDA']
ISynMech = ['GABAAfast','GABAAslow']

## Inhibitory GABA synaptic mechs
netParams.synMechParams['GABAAfast'] = {'mod':'MyExp2SynBB','tau1': 0.07,'tau2': 18.2,'e': cfg.GABAAfast_e}
netParams.synMechParams['GABAAslow'] = {'mod': 'MyExp2SynBB','tau1': 10, 'tau2': 200, 'e': cfg.GABAAslow_e}

## Excitatory NMDA and AMPA synaptic mechs
netParams.synMechParams['AMPA'] = {'mod': 'AMPA', 'gmax': cfg.AMPAgmax}
netParams.synMechParams['NMDA'] = {'mod': 'NMDA', 'Cdur': 10.0, 'Beta': 0.02, 'gmax': cfg.NMDAgmax}



## Stimulation parameters
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau1': 0.8, 'tau2': 5.3, 'e': 0}
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 20, 'noise': 0.3}
netParams.stimTargetParams['bkg->all'] = {'source': 'bkg', 'conds': {'cellType': ['PV5','PT5']}, 'weight': 0.01, 'delay': 'max(1, normal(5,2))', 'synMech': 'exc'}


## Cell connectivity rules


# Excitatory --> Excitatory

EPops = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4']

for prePop in EPops:
    for postPop in EPops:
        ruleLabel = prePop+'->'+postPop
        netParams.connParams[ruleLabel] = {
            'preConds': {'pop': prePop},
            'postConds': {'pop': postPop},
            'synMech': ESynMech, 
            'weight': [cfg.AMPAweight, cfg.NMDAweight],
            'delay': 'defaultDelay+dist_3D/propVelocity',
            'convergence': cfg.EEconv,
            'loc': 0.3,
            'sec': 'basal_8'}

# Excitatory --> Inhibitory

for prePop in EPops:
    for postPop in ['PV5']:
        ruleLabel = prePop+'->'+postPop
        netParams.connParams[ruleLabel] = {
            'preConds': {'pop': prePop},
            'postConds': {'pop': postPop},
            'synMech': 'AMPA',
            'weight': cfg.AMPAweight, 
            'delay': 'defaultDelay+dist_3D/propVelocity',
            'convergence': cfg.EIconv,
            'loc': 0.5,
            'sec': 'soma'}

# Inhibitory --> Excitatory

for prePop in ['PV5']:
    for postPop in EPops:
        ruleLabel = prePop+'->'+postPop
        netParams.connParams[ruleLabel] = {
            'preConds': {'pop': prePop},
            'postConds': {'pop': postPop},
            'synMech': ISynMech, 
            'weight': [cfg.GABAAfastWeight, cfg.GABAAslowWeight],
            'delay': 'defaultDelay+dist_3D/propVelocity',
            'convergence': cfg.IEconv,
            'loc': 0.5,
            'sec': 'soma'}


# netParams.connParams['PV5->PT5'] = {
#   'preConds': {'cellType': 'PV5'},
#   'postConds': {'cellType': 'PT5'},
#   'probability': 0.1,
#   'weight': [cfg.GABAAfastWeight, cfg.GABAAslowWeight],
#   'delay': 'dist_3D/propVelocity',
#   'synMech': ISynMech} 

netParams.connParams['PV5->PV5'] = {
  'preConds': {'cellType': 'PV5'},
  'postConds': {'cellType': 'PV5'},
  'probability': 0.1,
  'weight': cfg.GABAAfastWeight,
  'delay': 'dist_3D/propVelocity',
  'synMech': 'GABAAfast'} 

