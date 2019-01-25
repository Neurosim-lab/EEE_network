from netpyne import specs
import os
import copy

## Network variables (move to cfg.py later)
NMDAgmax        = 0.005
NMDA2AMPA       = 0.1
AMPAgmax        = NMDAgmax / NMDA2AMPA
NMDAweight      = 0.8
AMPAweight      = NMDAweight
GABAAfastWeight = 0.0001
GABAAslowWeight = 0.0001


## Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

netParams.sizeX = 100 # x-dimension (horizontal length) size in um
netParams.sizeY = 1000 # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = 100 # z-dimension (horizontal length) size in um
netParams.propVelocity = 100.0 # propagation velocity (um/ms)
netParams.probLengthConst = 150.0 # length constant for conn probability (um)


## Population parameters
numPT5cells = 80 #800
numPV5cells = 20 #200
ynormRange = [0.2,0.623]

netParams.popParams['PT5_1'] = {'cellType': 'PT5', 'numCells': int(numPT5cells/4), 'ynormRange': ynormRange, 'cellModel': 'HH'}
netParams.popParams['PT5_2'] = {'cellType': 'PT5', 'numCells': int(numPT5cells/4), 'ynormRange': ynormRange, 'cellModel': 'HH'}
netParams.popParams['PT5_3'] = {'cellType': 'PT5', 'numCells': int(numPT5cells/4), 'ynormRange': ynormRange, 'cellModel': 'HH'}
netParams.popParams['PT5_4'] = {'cellType': 'PT5', 'numCells': int(numPT5cells/4), 'ynormRange': ynormRange, 'cellModel': 'HH'}
netParams.popParams['PV5'] = {'cellType': 'PV5', 'numCells': numPV5cells, 'ynormRange': ynormRange, 'cellModel': 'HH'}


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
ESynMech = ['NMDA','AMPA']
ISynMech = ['GABAAfast','GABAAslow']

## Inhibitory GABA synaptic mechs
netParams.synMechParams['GABAAfast'] = {'mod':'MyExp2SynBB','tau1': 0.07,'tau2': 18.2,'e': cfg.GABAAfast_e}
netParams.synMechParams['GABAAslow'] = {'mod': 'MyExp2SynBB','tau1': 10, 'tau2': 200, 'e': cfg.GABAAslow_e}

## Excitatory NMDA and AMPA synaptic mechs
netParams.synMechParams['NMDA'] = {'mod': 'NMDA', 'Cdur': 10.0, 'Beta': 0.02, 'gmax': NMDAgmax}
netParams.synMechParams['AMPA'] = {'mod': 'AMPA', 'gmax': AMPAgmax}


## Stimulation parameters
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 20, 'noise': 0.3}
netParams.stimTargetParams['bkg->all'] = {'source': 'bkg', 'conds': {'cellType': ['PV5','PT5']}, 'weight': 0.01, 'delay': 'max(1, normal(5,2))', 'synMech': 'exc'}


## Cell connectivity rules
netParams.connParams['PT5->all'] = {
  'preConds': {'cellType': 'PT5'},
  'postConds': {'cellType': ['PT5','PV5']},
  'probability': 0.5,
  'weight': [NMDAweight, AMPAweight],
  'delay': 'dist_3D/propVelocity',
  'synMech': 'ESynMech'}

netParams.connParams['PV5->PT5'] = {
  'preConds': {'cellType': 'PV5'},
  'postConds': {'cellType': 'PT5'},
  'probability': 0.5,
  'weight': [GABAAfastWeight, GABAAslowWeight],
  'delay': 'dist_3D/propVelocity',
  'synMech': 'ISynMech'} 

netParams.connParams['PV5->PV5'] = {
  'preConds': {'cellType': 'PV5'},
  'postConds': {'cellType': 'PV5'},
  'probability': 0.5,
  'weight': GABAAfastWeight,
  'delay': 'dist_3D/propVelocity',
  'synMech': 'GABAAfast'} 


# ## Cell connectivity rules
# netParams.connParams['PT5->all'] = {
#   'preConds': {'cellType': 'PT5'}, 'postConds': {'y': [100,1000]},  #  E -> all (100-1000 um)
#   'probability': 0.1 ,                  # probability of connection
#   'weight': '0.005*post_ynorm',         # synaptic weight 
#   'delay': 'dist_3D/propVelocity',      # transmission delay (ms) 
#   'synMech': 'exc'}                     # synaptic mechanism 

# netParams.connParams['PV5->PT5'] = {
#   'preConds': {'cellType': 'PV5'}, 'postConds': {'cellType': ['PT5']},       #  I -> E
#   'probability': '0.4*exp(-dist_3D/probLengthConst)',   # probability of connection
#   'weight': 0.001,                                      # synaptic weight 
#   'delay': 'dist_3D/propVelocity',                      # transmission delay (ms) 
#   'synMech': 'inh'}                                     # synaptic mechanism 


