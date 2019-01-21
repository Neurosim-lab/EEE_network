from netpyne import specs
import os
import copy

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

# ## Import eeeS cell (PT5)
# cellRule = netParams.importCellParams(label='PT5_1', conds={'cellType':'PT5_1'}, fileName=eeeS_path, cellName='MakeCell', cellInstance=True)
# netParams.cellParams['PT5_1'] = cellRule

## Then copy the cellRule for the other pops (faster than importing again)
## Note: we are creating 1 cell type per pop because they could potentially have different noise and connectivity params           
for label in ['PT5_2', 'PT5_3', 'PT5_4']:    
    cellRule = copy.deepcopy(netParams.cellParams['PT5_1'].todict())
    cellRule['conds']['pop'] = [label]
    netParams.cellParams[label] = cellRule

# ## Then copy the cellRule for the other pops (faster than importing again)
# ## Note: we are creating 1 cell type per pop because they could potentially have different noise and connectivity params           
# for label in ['PT5_2', 'PT5_3', 'PT5_4']:    
#     cellRule = copy.deepcopy(netParams.cellParams['PT5_1'].todict())
#     cellRule['conds']['cellType'] = [label]
#     netParams.cellParams[label] = cellRule


## Synaptic mechanism parameters
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau1': 0.8, 'tau2': 5.3, 'e': 0}  # NMDA synaptic mechanism
netParams.synMechParams['inh'] = {'mod': 'Exp2Syn', 'tau1': 0.6, 'tau2': 8.5, 'e': -75}  # GABA synaptic mechanism


# Stimulation parameters
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 20, 'noise': 0.3}
netParams.stimTargetParams['bkg->all'] = {'source': 'bkg', 'conds': {'cellType': ['PV5','PT5']}, 'weight': 0.01, 'delay': 'max(1, normal(5,2))', 'synMech': 'exc'}


## Cell connectivity rules
netParams.connParams['PT5->all'] = {
  'preConds': {'cellType': 'PT5'}, 'postConds': {'y': [100,1000]},  #  E -> all (100-1000 um)
  'probability': 0.1 ,                  # probability of connection
  'weight': '0.005*post_ynorm',         # synaptic weight 
  'delay': 'dist_3D/propVelocity',      # transmission delay (ms) 
  'synMech': 'exc'}                     # synaptic mechanism 

netParams.connParams['PV5->PT5'] = {
  'preConds': {'cellType': 'PV5'}, 'postConds': {'cellType': ['PT5']},       #  I -> E
  'probability': '0.4*exp(-dist_3D/probLengthConst)',   # probability of connection
  'weight': 0.001,                                      # synaptic weight 
  'delay': 'dist_3D/propVelocity',                      # transmission delay (ms) 
  'synMech': 'inh'}                                     # synaptic mechanism 

