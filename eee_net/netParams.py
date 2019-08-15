from netpyne import specs
import os
import copy
import numpy as np

try:
    from __main__ import cfg
except:
    from cfg import cfg


## Hash function
def id32(obj):
    return hash(obj) & 0xffffffff

## Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

netParams.version = 1

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
PV_path   = os.path.join(cellpath, 'FS3.py')



## Import PV5 cell
cellRule = netParams.importCellParams(label='PV5', conds={'cellType':'PV5'}, fileName=PV_path, cellName='MakeCell', cellInstance=True)
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

# PT5_1 noise
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

# PV5 noise
if cfg.noisePV5:
    netParams.cellParams['PV5']['secs']['soma']['pointps'] = {
                        'noise': {'mod': 'Gfluctp', 
                        'loc': 0.5,
                        'std_e': 0.012,
                        'g_e0' : 0.0121 * cfg.PV5_exc_noise_amp, 
                        'tau_i': 10.49 * cfg.PV5_inh_noise_tau, 
                        'tau_e': 2.728 * cfg.PV5_exc_noise_tau, 
                        'std_i': 0.0264, 
                        'g_i0' : 0.0573 * cfg.PV5_inh_noise_amp, 
                        'E_e'  : cfg.PV5_exc_noise_e, 
                        'E_i'  : cfg.PV5_inh_noise_e, 
                        'seed1': 'gid', 
                        'seed2': id32('gfluctp'), 
                        'seed3': cfg.seeds['stim']}}


# All PT5_1 parameters have been set (including noise), so now copy the 
#   cellRule for the other PT pops
# Note: we are creating 1 cell type per pop because they could potentially 
#   have different noise and connectivity params  

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

if cfg.glutamate:

    for nslabel in [k for k in dir(cfg) if k.startswith('glutPuff')]:

        ns = getattr(cfg, nslabel, None)        
            
        branch_length = netParams.cellParams['PT5_1']['secs'][ns['sec']]['geom']['L']

        if "ExSyn" in nslabel:
            cur_locs = np.linspace(cfg.synLocMiddle-cfg.synLocRadius, cfg.synLocMiddle+cfg.synLocRadius, cfg.numExSyns)
            cur_dists = branch_length * np.abs(cur_locs - cfg.synLocMiddle)
            cur_weights = (cfg.glutAmp * cfg.glutAmpExSynScale) * (1 - cur_dists * cfg.glutAmpDecay/100)
            cur_weights = [weight if weight > 0.0 else 0.0 for weight in cur_weights]
            cur_delays = cfg.initDelay + (cfg.exSynDelay * cur_dists)
                  
              
        elif "Syn" in nslabel:
            cur_locs = np.linspace(cfg.synLocMiddle-cfg.synLocRadius, cfg.synLocMiddle+cfg.synLocRadius, cfg.numSyns)
            cur_dists = branch_length * np.abs(cur_locs - cfg.synLocMiddle)
            cur_weights = cfg.glutAmp * (1 - cur_dists * cfg.glutAmpDecay/100)
            cur_weights = [weight if weight > 0.0 else 0.0 for weight in cur_weights]
            cur_delays = cfg.initDelay + (cfg.synDelay * cur_dists)                
              
        else:
            raise Exception("Should have had Syn or ExSyn in name. See netParams.py")             
        
        # add stim source
        netParams.stimSourceParams[nslabel] = {'type': 'NetStim', 'start': ns['start'], 'interval': ns['interval'], 'noise': ns['noise'], 'number': ns['number']}  

        # connect stim source to target
        for cur_pop in cfg.glutPops:    

            for i in range(len(ns['synMech'])):
                
                netParams.stimTargetParams[nslabel+'_'+cur_pop+'_'+ns['synMech'][i]] = {'source': nslabel, 'conds': {'pop': cur_pop}, 'sec': ns['sec'], 'synsPerConn': cfg.numSyns, 'loc': list(cur_locs), 'synMech': ns['synMech'][i], 'weight': list(cur_weights), 'delay': list(cur_delays)}


if cfg.addIClamp:

    for iclabel in [k for k in dir(cfg) if k.startswith('IClamp')]:
        ic = getattr(cfg, iclabel, None)  # get dict with params

        # add stim source
        #netParams.stimSourceParams[iclabel] = {'type': 'IClamp', 'del': ic['del'], 'dur': ic['dur'], 'amp': ic['amp']}
        netParams.stimSourceParams[iclabel] = {'type': 'IClamp', 'del': ic['del'], 'dur': ic['dur'], 'amp': cfg.ampIClamp1}
        
        # add stim target
        for curpop in ic['pop']:
            netParams.stimTargetParams[iclabel+'_'+curpop] = \
                {'source': iclabel, 'conds': {'popLabel': ic['pop']}, 'sec': ic['sec'], 'loc': ic['loc']}

if cfg.addCommonInput1:

    netParams.stimSourceParams['CommonInput1'] = {'type': 'NetStim', 'start': cfg.delCommonInput1, 'interval': cfg.intCommonInput1, 'number': cfg.numCommonInput1}
                  
    for postPop in cfg.popCommonInput1:             
        
        ruleLabel = 'CommonInput1->'+postPop
        netParams.stimTargetParams[ruleLabel] = {
            'source' : 'CommonInput1', 
            'conds'  : {'pop': postPop}, 
            'sec'    : cfg.secCommonInput1, 
            'loc'    : cfg.locCommonInput1, 
            'synMech': ['AMPA', 'NMDA'], 
            'weight' : cfg.wgtCommonInput1, 
            'delay'  : 0.0}


if cfg.addCommonInput2:

    netParams.stimSourceParams['CommonInput2'] = {'type': 'NetStim', 'start': cfg.delCommonInput2, 'interval': cfg.intCommonInput2, 'number': cfg.numCommonInput2}
                  
    for postPop in cfg.popCommonInput2:             
        
        ruleLabel = 'CommonInput2->'+postPop
        netParams.stimTargetParams[ruleLabel] = {
            'source' : 'CommonInput2', 
            'conds'  : {'pop': postPop}, 
            'sec'    : cfg.secCommonInput2, 
            'loc'    : cfg.locCommonInput2, 
            'synMech': ['AMPA', 'NMDA'], 
            'weight' : cfg.wgtCommonInput2, 
            'delay'  : 0.0}



