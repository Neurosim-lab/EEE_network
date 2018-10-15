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
from neuron import h

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

# EEE cell model with uniform spine distribution (7 comps)
cellRule = netParams.importCellParams(label='eee7us', conds={'cellType': 'eee7us', 'cellModel': 'HH_reduced'}, fileName=os.path.join(cellpath, 'eee7us.py'), cellName='eee7us')

# EEE cell model with physiological spine distribution (7 comps)
cellRule = netParams.importCellParams(label='eee7ps', conds={'cellType': 'eee7ps', 'cellModel': 'HH_reduced'}, fileName=os.path.join(cellpath, 'eee7ps.py'), cellName='eee7ps')

# define section lists
cellRule['secLists']['alldend'] = ['Bdend1', 'Bdend2', 'Adend1', 'Adend2', 'Adend3']
cellRule['secLists']['apicdend'] = ['Adend1', 'Adend2', 'Adend3']
cellRule['secLists']['basaldend'] = ['Bdend1', 'Bdend2']
cellRule['secLists']['stimheads'] = []
cellRule['secLists']['stimnecks'] = []

# apply values to parameters
activeSpines = {}
for cell_label, cell_params in netParams.cellParams.iteritems():

    activeSpines[cell_label] = {}
    activeSpines[cell_label]['activeSpineNecks'] = []
    activeSpines[cell_label]['activeSpineHeads'] = []
    activeSpines[cell_label]['spineDelay']  = []
    activeSpines[cell_label]['spineWeight'] = []

    for secName,sec in cell_params['secs'].iteritems(): 
        sec['vinit'] = -75.0413649414  # set vinit for all secs
        
        if hasattr(cfg, 'allNaScale') or hasattr(cfg, 'dendNaScale'):
            if 'nax' in sec['mechs']:
                orig_nax = sec['mechs']['nax']['gbar']
                print
                print(secName)
                print("orig nax gbar")
                print(orig_nax)
                if hasattr(cfg, 'dendNaScale'):
                    print('dendNaScale = %s' % (str(cfg.dendNaScale)))
                    sec['mechs']['nax']['gbar'] = cfg.dendNaScale * orig_nax       
                if hasattr(cfg, 'allNaScale'):
                    print('allNaScale = %s' % (str(cfg.allNaScale)))
                    sec['mechs']['nax']['gbar'] = cfg.allNaScale * orig_nax
                print(sec['mechs']['nax']['gbar'])
        
        if hasattr(cfg, 'allKScale') or hasattr(cfg, 'dendKScale'):
            if 'kdr' in sec['mechs']:
                orig_kdr = sec['mechs']['kdr']['gbar']
                print
                print(secName)
                print("orig kdr gbar")
                print(orig_kdr)
                if hasattr(cfg, 'dendKScale'):
                    print('dendKScale = %s' % (str(cfg.dendKScale)))
                    sec['mechs']['kdr']['gbar'] = cfg.dendKScale * orig_kdr
                if hasattr(cfg, 'allKScale'):
                    print('allKScale = %s' % (str(cfg.allKScale)))
                    sec['mechs']['kdr']['gbar'] = cfg.allKScale * orig_kdr
                print(sec['mechs']['kdr']['gbar'])
            
            if 'kap' in sec['mechs']:
                orig_kap = sec['mechs']['kap']['gbar']
                print
                print(secName)
                print("orig kap gbar")
                print(orig_kap)
                if hasattr(cfg, 'dendKScale'):
                    print('dendKScale = %s' % (str(cfg.dendKScale)))
                    sec['mechs']['kap']['gbar'] = cfg.dendKScale * orig_kap
                if hasattr(cfg, 'allKScale'):
                    print('allKScale = %s' % (str(cfg.allKScale)))
                    sec['mechs']['kap']['gbar'] = cfg.allKScale * orig_kap
                print(sec['mechs']['kap']['gbar'])
        


        


        if "neck" in secName:
            neckLoc = sec['topol']['parentX']
            if neckLoc > cfg.glutLoc-(cfg.glutSpread/(2*200.)) and neckLoc < cfg.glutLoc+(cfg.glutSpread/(2*200.)):
                activeSpines[cell_label]['activeSpineNecks'].append(secName)
                activeSpines[cell_label]['activeSpineHeads'].append("head_" + secName.split('_')[1])
                distance = 200. * np.abs(cfg.glutLoc-neckLoc)
                activeSpines[cell_label]['spineDelay'].append(distance*cfg.glutDelay)
                if (cfg.glutDecay * distance) < 100.0:
                    spineWeight = cfg.glutAmp * ((100.0 - (cfg.glutDecay * distance))/100.0)
                else:
                    spineWeight = 0.0
                activeSpines[cell_label]['spineWeight'].append(spineWeight)

            diam = cellRule['secs'][secName]['geom']['diam']
            leng = cellRule['secs'][secName]['geom']['L']
            
            if hasattr(cfg, 'Rneck'):
                cellRule['secs'][secName]['geom']['Ra'] = cfg.Rneck * 100 * 3.1416 * (diam/2) * (diam/2) / leng


###############################################################################
# Population parameters
###############################################################################

netParams.popParams['eee7us']= {'cellModel':'HH_reduced', 'cellType':'eee7us', 'numCells':1}
netParams.popParams['eee7ps']= {'cellModel':'HH_reduced', 'cellType':'eee7ps', 'numCells':1}


###############################################################################
# Synaptic mechanism parameters
###############################################################################

netParams.synMechParams['NMDA'] = {'mod': 'NMDA', 'Cdur': cfg.CdurNMDAScale * 1.0, 'Cmax': cfg.CmaxNMDAScale * 1.0, 'Alpha': cfg.NMDAAlphaScale * 4.0, 'Beta': cfg.NMDABetaScale * 0.0015}

netParams.synMechParams['AMPA'] = {'mod': 'AMPA'}

h.gmax_NMDA = cfg.NMDAgmax
h.gmax_AMPA = cfg.ratioAMPANMDA * cfg.NMDAgmax

###############################################################################
# NetStim inputs
###############################################################################
if cfg.addNetStim:
    
    for nslabel in [k for k in dir(cfg) if k.startswith('NetStim')]:
        ns = getattr(cfg, nslabel, None)

        cur_pop = ns['pop'][0]

        activeSpineHeads = activeSpines[cur_pop]['activeSpineHeads']
        activeSpineNecks = activeSpines[cur_pop]['activeSpineNecks']
        numActiveSpines = len(activeSpineHeads)

        spineWeights = activeSpines[cur_pop]['spineWeight']
        spineDelays = activeSpines[cur_pop]['spineDelay']

        if ns['sec'] == 'spineheads':
            ns['sec']  = activeSpineHeads
            cur_weight = spineWeights #[cfg.glutAmp for head in activeSpineHeads]
            cur_loc    = 0.99999
            cur_delay  = spineDelays #[cfg.glutDelay for head in activeSpineHeads]
        elif ns['sec'] == 'spinenecks':
            ns['sec']  = activeSpineNecks
            cur_weight = [cfg.glutAmp * cfg.spillFraction for neck in activeSpineNecks]
            cur_loc    = 0.00001
            cur_delay  = [cfg.glutDelay + cfg.spillDelay for neck in activeSpineNecks]
        else:
            print("######################################################")
            print("NetStim sec needs to be 'spineheads' or 'spinenecks'")
            print("######################################################")

        # add stim source
        netParams.stimSourceParams[nslabel] = {'type': 'NetStim', 'start': ns['start'], 'interval': ns['interval'], 'noise': ns['noise'], 'number': ns['number']}

        # connect stim source to target
        for i in range(len(ns['synMech'])):
            netParams.stimTargetParams[nslabel+'_'+cur_pop+'_'+ns['synMech'][i]] = \
                {'source': nslabel, 'conds': {'pop': ns['pop']}, 'sec': ns['sec'], 'synsPerConn': numActiveSpines, 'loc': cur_loc, 'synMech': ns['synMech'][i], 'weight': cur_weight, 'delay': cur_delay}

        print
        print("===============================================")
        print("cur_pop   = %s" % (cur_pop))
        print("glutAmp   = %f" % (cfg.glutAmp))
        print("glutLoc   = %f" % (cfg.glutLoc))
        print("numSpines = %f" % (numActiveSpines))
        print
        zipped = zip(activeSpineHeads, cur_weight, cur_delay)
        zipped.sort(key = lambda x: x[0])
        for spine, weight, delay in zipped:
            print(spine)
            print("  weight (%%) = %f" % (100*weight/cfg.glutAmp))
            print("  delay (ms) = %f" % (delay))
        print("===============================================")



