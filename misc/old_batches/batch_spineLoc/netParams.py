"""
netParams.py 
Specifications for EEE model using NetPyNE

Originally:
High-level specifications for M1 network model using NetPyNE
Contributors: salvadordura@gmail.com
"""

from netpyne import specs
import os

# Find path to cells directory
curpath = os.getcwd()
while os.path.split(curpath)[1] != "sim":
    curpath = os.path.split(curpath)[0]
cellpath = os.path.join(curpath, "cells")

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg  # if no simConfig in parent module, import directly from cfg module

###############################################################################
#
# NETWORK PARAMETERS
#
###############################################################################

netParams = specs.NetParams()   # object of class NetParams to store the network parameters

###############################################################################
# Cell parameters
###############################################################################

# Original cell model
cellRule = netParams.importCellParams(label='SPI6', conds={'cellType': 'SPI6Type', 'cellModel': 'HH_reduced'}, fileName=os.path.join(cellpath, 'SPI6.py'), cellName='SPI6')

# EEE cell model (6 compartments, Bdend L = 200)
cellRule = netParams.importCellParams(label='eee6', conds={'cellType': 'eee6Type', 'cellModel': 'HH_reduced'}, fileName=os.path.join(cellpath, 'eee6.py'), cellName='eee6')

# EEE cell model (7 compartments: extra Bdend)
cellRule = netParams.importCellParams(label='eee7', conds={'cellType': 'eee7Type', 'cellModel': 'HH_reduced'}, fileName=os.path.join(cellpath, 'eee7.py'), cellName='eee7')

# EEE cell model with uniform spine distribution (7 comps)
cellRule = netParams.importCellParams(label='eee7us', conds={'cellType': 'eee7usType', 'cellModel': 'HH_reduced'}, fileName=os.path.join(cellpath, 'eee7us.py'), cellName='eee7us')

# EEE cell model with physiological spine distribution (7 comps)
cellRule = netParams.importCellParams(label='eee7ps', conds={'cellType': 'eee7psType', 'cellModel': 'HH_reduced'}, fileName=os.path.join(cellpath, 'eee7ps.py'), cellName='eee7ps')

# define section lists
cellRule['secLists']['alldend'] = ['Bdend1', 'Bdend2', 'Adend1', 'Adend2', 'Adend3']
cellRule['secLists']['apicdend'] = ['Adend1', 'Adend2', 'Adend3']
cellRule['secLists']['basaldend'] = ['Bdend1', 'Bdend2']

for cell_label, cell_params in netParams.cellParams.iteritems():
    for secName,sec in cell_params['secs'].iteritems(): 
        sec['vinit'] = -75.0413649414  # set vinit for all secs
        if secName in cellRule['secLists']['alldend']:  
            sec['mechs']['nax']['gbar'] = cfg.dendNa # set dend Na gmax for all dends
            sec['mechs']['kdr']['gbar'] = cfg.dendK * sec['mechs']['kdr']['gbar'] 
            sec['mechs']['kap']['gbar'] = cfg.dendK * sec['mechs']['kap']['gbar']  
        if secName in cellRule['secLists']['basaldend']:
            sec["geom"]["Ra"] = cfg.BdendRa
        if "neck" in secName:
            diam = sec['geom']['diam']
            leng = sec['geom']['L']
            sec['geom']['Ra'] = cfg.Rneck * 100 * 3.1416 * (diam/2) * (diam/2) / leng

###############################################################################
# Population parameters
###############################################################################

#netParams.popParams['PT5B'] =  {'cellModel': 'HH_reduced', 'cellType': 'PT', 'numCells': 1}

netParams.popParams['SPI6Pop'] =    {'cellModel': 'HH_reduced', 'cellType': 'SPI6Type', 'numCells': 1}
netParams.popParams['eee6Pop'] =    {'cellModel': 'HH_reduced', 'cellType': 'eee6Type', 'numCells': 1}
netParams.popParams['eee7Pop'] =    {'cellModel': 'HH_reduced', 'cellType': 'eee7Type', 'numCells': 1}
netParams.popParams['eee7usPop'] =  {'cellModel': 'HH_reduced', 'cellType': 'eee7usType', 'numCells': 1}
netParams.popParams['eee7psPop'] =  {'cellModel': 'HH_reduced', 'cellType': 'eee7psType', 'numCells': 1}


###############################################################################
# Synaptic mechanism parameters
###############################################################################

netParams.synMechParams['NMDA'] = {'mod': 'MyExp2SynNMDABB', 'tau1NMDA': cfg.tau1NMDA, 'tau2NMDA': cfg.tau2NMDA, 'e': 0}
netParams.synMechParams['AMPA'] = {'mod': 'AMPA'}

###############################################################################
# Current inputs (IClamp)
###############################################################################

if cfg.addIClamp:   
    for iclabel in [k for k in dir(cfg) if k.startswith('IClamp')]:
        ic = getattr(cfg, iclabel, None)  # get dict with params

        # add stim source
        netParams.stimSourceParams[iclabel] = {'type': 'IClamp', 'del': ic['start'], 'dur': ic['dur'], 'amp': ic['amp']}
        
        # connect stim source to target
        #netParams.stimTargetParams[iclabel+'_'+ic['pop']] = \
        #   {'source': iclabel, 'conds': {'popLabel': ic['pop']}, 'sec': ic['sec'], 'loc': ic['loc']}
        
        for curpop in ic['pop']:
            netParams.stimTargetParams[iclabel+'_'+curpop] = \
                {'source': iclabel, 'conds': {'popLabel': ic['pop']}, 'sec': ic['sec'], 'loc': ic['loc']}

###############################################################################
# NetStim inputs
###############################################################################
if cfg.addNetStim:
    for nslabel in [k for k in dir(cfg) if k.startswith('NetStim')]:
        ns = getattr(cfg, nslabel, None)

        # add stim source
        netParams.stimSourceParams[nslabel] = {'type': 'NetStim', 'start': ns['start'], 'interval': ns['interval'], 'noise': ns['noise'], 'number': ns['number']}

        # connect stim source to target
        for i in range(len(ns['synMech'])):
            if ns['synMech'][i] == 'AMPA': 
                ns['weight'][i] = ns['weight'][0] * cfg.ratioAMPANMDA
            for curpop in ns['pop']:
                #netParams.stimTargetParams[nslabel+'_'+curpop+'_'+ns['synMech'][i]] = \
                #    {'source': nslabel, 'conds': {'popLabel': ns['pop']}, 'sec': ns['sec'], 'loc': ns['loc'], 'synMech': ns['synMech'][i], 'weight': ns['weight'][i], 'delay': ns['delay']}
                netParams.stimTargetParams[nslabel+'_'+curpop+'_'+ns['synMech'][i]] = \
                    {'source': nslabel, 'conds': {'popLabel': curpop}, 'sec': ns['sec'], 'loc': ns['loc'], 'synMech': ns['synMech'][i], 'weight': ns['weight'][i], 'delay': ns['delay']}
                
