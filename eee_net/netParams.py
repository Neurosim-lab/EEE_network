from netpyne import specs

# Network parameters
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

netParams.popParams['PT5_1'] = {'cellType': 'E', 'numCells': int(numPT5cells/4), 'ynormRange': ynormRange, 'cellModel': 'HH'}
netParams.popParams['PT5_2'] = {'cellType': 'E', 'numCells': int(numPT5cells/4), 'ynormRange': ynormRange, 'cellModel': 'HH'}
netParams.popParams['PT5_3'] = {'cellType': 'E', 'numCells': int(numPT5cells/4), 'ynormRange': ynormRange, 'cellModel': 'HH'}
netParams.popParams['PT5_4'] = {'cellType': 'E', 'numCells': int(numPT5cells/4), 'ynormRange': ynormRange, 'cellModel': 'HH'}
netParams.popParams['PV5'] = {'cellType': 'I', 'numCells': numPV5cells, 'ynormRange': ynormRange, 'cellModel': 'HH'}


## Cell property rules
cellRule = {'conds': {'cellType': 'E'},  'secs': {}}  # cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'mechs': {}}                              # soma params dict
cellRule['secs']['soma']['geom'] = {'diam': 15, 'L': 14, 'Ra': 120.0}                   # soma geometry
cellRule['secs']['soma']['mechs']['hh'] = {'gnabar': 0.13, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}      # soma hh mechanism
netParams.cellParams['Erule'] = cellRule                          # add dict to list of cell params

cellRule = {'conds': {'cellType': 'I'},  'secs': {}}  # cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'mechs': {}}                              # soma params dict
cellRule['secs']['soma']['geom'] = {'diam': 10.0, 'L': 9.0, 'Ra': 110.0}                  # soma geometry
cellRule['secs']['soma']['mechs']['hh'] = {'gnabar': 0.11, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}      # soma hh mechanism
netParams.cellParams['Irule'] = cellRule                          # add dict to list of cell params


## Synaptic mechanism parameters
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau1': 0.8, 'tau2': 5.3, 'e': 0}  # NMDA synaptic mechanism
netParams.synMechParams['inh'] = {'mod': 'Exp2Syn', 'tau1': 0.6, 'tau2': 8.5, 'e': -75}  # GABA synaptic mechanism


# Stimulation parameters
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 20, 'noise': 0.3}
netParams.stimTargetParams['bkg->all'] = {'source': 'bkg', 'conds': {'cellType': ['E','I']}, 'weight': 0.01, 'delay': 'max(1, normal(5,2))', 'synMech': 'exc'}


## Cell connectivity rules
netParams.connParams['E->all'] = {
  'preConds': {'cellType': 'E'}, 'postConds': {'y': [100,1000]},  #  E -> all (100-1000 um)
  'probability': 0.1 ,                  # probability of connection
  'weight': '0.005*post_ynorm',         # synaptic weight 
  'delay': 'dist_3D/propVelocity',      # transmission delay (ms) 
  'synMech': 'exc'}                     # synaptic mechanism 

netParams.connParams['I->E'] = {
  'preConds': {'cellType': 'I'}, 'postConds': {'pop': ['E']},       #  I -> E
  'probability': '0.4*exp(-dist_3D/probLengthConst)',   # probability of connection
  'weight': 0.001,                                      # synaptic weight 
  'delay': 'dist_3D/propVelocity',                      # transmission delay (ms) 
  'synMech': 'inh'}                                     # synaptic mechanism 
