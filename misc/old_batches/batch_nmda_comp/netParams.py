"""
netParams.py 
Specifications for EEE model using NetPyNE

Originally:
High-level specifications for M1 network model using NetPyNE
Contributors: salvadordura@gmail.com
"""

from netpyne import specs
import os
import numpy as np

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
netParams.defaultThreshold = -20.0

###############################################################################
# Cell parameters
###############################################################################

# EEE cell model with physiological spine distribution (7 comps)
cellRule = netParams.importCellParams(label='eee7ps', conds={'cellType': 'eee7ps', 'cellModel': 'HH_reduced'}, fileName=os.path.join(cellpath, 'eee7ps.py'), cellName='eee7ps')

# define section lists
cellRule['secLists']['alldend'] = ['Bdend1', 'Bdend2', 'Adend1', 'Adend2', 'Adend3']
cellRule['secLists']['apicdend'] = ['Adend1', 'Adend2', 'Adend3']
cellRule['secLists']['basaldend'] = ['Bdend1', 'Bdend2']
cellRule['secLists']['stimheads'] = []
cellRule['secLists']['stimnecks'] = []

# set up spine stim
numActiveSpines = cfg.glutSpread
spine_glut_delay  = np.ones(numActiveSpines)
shaft_glut_delay  = spine_glut_delay + cfg.spillDelay * np.ones(numActiveSpines)

indWeightNMDA = cfg.glutAmp / cfg.glutSpread
activeSpineNums = cfg.glutSpine + np.arange(cfg.glutSpread)
activeSpineHeads = ["head_" + str(num) for num in activeSpineNums]
activeSpineNecks = ["neck_" + str(num) for num in activeSpineNums]

spine_NMDA_weight = [indWeightNMDA for head in activeSpineHeads]
shaft_glut_weight = [indWeightNMDA * cfg.spillFraction for neck in activeSpineNecks]

# apply values to parameters
for cell_label, cell_params in netParams.cellParams.iteritems():
    for secName,sec in cell_params['secs'].iteritems(): 
        sec['vinit'] = -75.0413649414  # set vinit for all secs
        if "neck" in secName:
            diam = cellRule['secs'][secName]['geom']['diam']
            leng = cellRule['secs'][secName]['geom']['L']
            if hasattr(cfg, 'Rneck'):
                cellRule['secs'][secName]['geom']['Ra'] = cfg.Rneck * 100 * 3.1416 * (diam/2) * (diam/2) / leng
        

###############################################################################
# Population parameters
###############################################################################

netParams.popParams['e2s']= {'cellModel':'HH_reduced', 'cellType':'eee7ps', 'numCells':1}
netParams.popParams['dms']= {'cellModel':'HH_reduced', 'cellType':'eee7ps', 'numCells':1}


###############################################################################
# Synaptic mechanism parameters
###############################################################################

netParams.synMechParams['NMDAe2s'] = {'mod': 'MyExp2SynNMDABB', 'tau1NMDA': cfg.tau1NMDAscale * 15.0, 'tau2NMDA': cfg.tau2NMDAscale * 150.0, 'e': 0}

netParams.synMechParams['NMDA'] = {'mod': 'NMDA', 'Cdur': cfg.CdurNMDAScale * 1.0, 'Cmax': cfg.CmaxNMDAScale * 1.0, 'Alpha': cfg.NMDAalphaScale * 4.0, 'Beta': cfg.NMDABetaScale * 0.0015}

netParams.synMechParams['AMPA'] = {'mod': 'AMPA'}


###############################################################################
# NetStim inputs
###############################################################################
if cfg.addNetStim:
    
    for nslabel in [k for k in dir(cfg) if k.startswith('NetStim')]:
        ns = getattr(cfg, nslabel, None)

        if ns['sec'] == 'spineheads':
            ns['sec']  = list(activeSpineHeads)
            cur_weight = list([cfg.glutAmp / cfg.glutSpread for head in activeSpineHeads])
            cur_loc    = 0.99999
            cur_delay  = list(spine_glut_delay)
        elif ns['sec'] == 'spinenecks':
            ns['sec']  = list(activeSpineNecks)
            cur_weight = list(shaft_glut_weight)
            cur_loc    = 0.00001
            cur_delay  = list(shaft_glut_delay)
        else:
            print("######################################################")
            print("NetStim sec needs to be 'spineheads' or 'spinenecks'")
            print("######################################################")

        # add stim source
        netParams.stimSourceParams[nslabel] = {'type': 'NetStim', 'start': ns['start'], 'interval': ns['interval'], 'noise': ns['noise'], 'number': ns['number']}

        # connect stim source to target
        for i in range(len(ns['synMech'])):
            if ns['synMech'][i] == 'AMPA': 
                cur_weight = list(np.array(cur_weight) * cfg.ratioAMPANMDA)
            for curpop in ns['pop']:
                netParams.stimTargetParams[nslabel+'_'+curpop+'_'+ns['synMech'][i]] = \
                    {'source': nslabel, 'conds': {'pop': ns['pop']}, 'sec': ns['sec'], 'synsPerConn': numActiveSpines, 'loc': cur_loc, 'synMech': ns['synMech'][i], 'weight': cur_weight, 'delay': cur_delay}

