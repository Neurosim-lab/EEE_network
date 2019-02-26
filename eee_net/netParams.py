from netpyne import specs
import os
import copy
try:
    from __main__ import cfg
except:
    from cfg import cfg


## Hash function
def id32(obj):
    return hash(obj) & 0xffffffff

## Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

netParams.sizeX = cfg.sizeX # x-dimension (horizontal length) size in um
netParams.sizeY = cfg.sizeY # y-dimension (vertical height or cortical depth)
netParams.sizeZ = cfg.sizeZ # z-dimension (horizontal depth)
netParams.shape = 'cylinder' # cylindrical (column-like) volume
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


## Synaptic mechanism parameters
ESynMech = ['AMPA','NMDA']
ISynMech = ['GABAAfast','GABAAslow']

## Inhibitory GABA synaptic mechs
netParams.synMechParams['GABAAfast'] = {'mod':'MyExp2SynBB','tau1': 0.07,'tau2': 18.2,'e': cfg.GABAAfast_e}
netParams.synMechParams['GABAAslow'] = {'mod': 'MyExp2SynBB','tau1': 10, 'tau2': 200, 'e': cfg.GABAAslow_e}

## Excitatory NMDA and AMPA synaptic mechs
netParams.synMechParams['AMPA'] = {'mod': 'AMPA', 'gmax': cfg.AMPAgmax}
netParams.synMechParams['NMDA'] = {'mod': 'NMDA', 'Cdur': 10.0, 'Beta': 0.02, 'gmax': cfg.NMDAgmax}



## Noise

#netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau1': 0.8, 'tau2': 5.3, 'e': 0}
#netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 20, 'noise': 0.3}
#netParams.stimTargetParams['bkg->all'] = {'source': 'bkg', 'conds': {'cellType': ['PV5','PT5']}, 'weight': 0.01, 'delay': 'max(1, normal(5,2))', 'synMech': 'exc'}

if cfg.noisePT5:
    netParams.cellParams['PT5_1']['secs']['soma']['pointps'] = {
                        'noise': {'mod': 'Gfluctp', 
                        'loc': 0.5,
                        'std_e': 0.012,
                        'g_e0' : 0.0121 * cfg.PT5_exc_noise_amp, 
                        'tau_i': 10.49 * cfg.PT5_inh_noise_tau, 
                        'tau_e': 2.728 * cfg.PT5_exc_noise_tau, 
                        'std_i': 0.0264, 
                        'g_i0' : 0.0573 * cfg.PT5_inh_noise_amp, 
                        'E_e'  : cfg.PT5_exc_noise_e, 
                        'E_i'  : cfg.PT5_inh_noise_e, 
                        'seed1': 'gid', 
                        'seed2': id32('gfluctp'), 
                        'seed3': cfg.seeds['stim']}}


# Now that all PT5_1 parameters have been set, copy the cellRule for the other pops
# Note: we are creating 1 cell type per pop because they could potentially have 
# different noise and connectivity params  

for label in ['PT5_2', 'PT5_3', 'PT5_4']:    
    cellRule = copy.deepcopy(netParams.cellParams['PT5_1'].todict())
    cellRule['conds']['pop'] = [label]
    netParams.cellParams[label] = cellRule





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


# Inhibitory --> Inhibitory

for prePop in ['PV5']:
    for postPop in ['PV5']:
        ruleLabel = prePop+'->'+postPop
        netParams.connParams[ruleLabel] = {
            'preConds': {'pop': prePop},
            'postConds': {'pop': postPop},
            'synMech': 'GABAAfast',
            'weight': cfg.GABAAfastWeight, 
            'delay': 'defaultDelay+dist_3D/propVelocity',
            'convergence': cfg.IIconv,
            'loc': 0.5,
            'sec': 'soma'}



