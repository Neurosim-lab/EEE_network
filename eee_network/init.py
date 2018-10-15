"""
init.py

Usage:
    python init.py # Run simulation, optionally plot a raster

MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py

Contributors: salvadordura@gmail.com
"""

import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers
from netpyne import sim
from neuron import h
import matplotlib.pyplot as plt
#import sys

#sys.path.insert(1,'/usr/site/nrniv/local/python/netpyne')

cfg, netParams = sim.readCmdLineArgs()

L5 = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4', 'PV5']

def myinit1():  #different seed per subset
    for i,v in enumerate(L5):
        if i==0:
            for c in sim.net.cells:
                if c.tags['pop'] in v:
                    for isec,sec in c.secs.iteritems():
                        if isec == 'soma':                          
                            for ip, pointp in enumerate(sec.pointps.values()):
                                if pointp['mod'] == 'Gfluctp':                                  
                                    pointp.hPointp.noiseFromRandom123(c.gid, len(c.conns), ip)

        else:     
            for k,c in enumerate(sim.net.cells):
                if c.tags['pop'] in v:
                    for isec,sec in c.secs.iteritems():
                        if isec == 'soma':
                            for ip, pointp in enumerate(sec.pointps.values()):
                                if pointp['mod'] == 'Gfluctp':
                                    pointp.hPointp.noiseFromRandom123(i, i*2, i*3)

def myinit2(): #different seed per cell
    for i,v in enumerate(L5):
        for c in sim.net.cells:
                if c.tags['pop'] in v:                  
                    for isec,sec in c.secs.iteritems():
                        if isec == 'soma_2':
                            for ip, pointp in enumerate(sec.pointps.values()):
                                if pointp['mod'] == 'Gfluctp':
                                    pointp.hPointp.noiseFromRandom123(c.gid, len(c.conns), ip)
                        elif isec =='soma':
                            for ip, pointp in enumerate(sec.pointps.values()):
                                if pointp['mod'] == 'Gfluctp':
                                    pointp.hPointp.noiseFromRandom123(c.gid, len(c.conns), ip)


ss=h.SaveState()

def savestate (fn='svst'):
    f = h.File(fn)
    ss.save()
    ss.fwrite(f)

def restorestate (fn='svst'):
    f = h.File(fn)
    ss.fread(f)
    ss.restore()

def rerun (t=400):
    h.finitialize()
    restorestate()
    sim.preRun() # to do sim.pc.set_maxstep(10)
    sim.pc.psolve(t)


#restorestate()
sim.initialize(
    simConfig = cfg,
    netParams = netParams)                  # create network object and set cfg and net params

sim.net.createPops()                        # instantiate network populations
sim.net.createCells()                       # instantiate network cells based on defined populations
sim.net.connectCells()                      # create connections between cells based on params

sim.net.addStims()                          # add network stimulation

#myinit2()

#sim.fih.append(h.FInitializeHandler(1,myinit()))

sim.setupRecording()                        # setup variables to record for each cell (spikes, V traces, etc)

#rerun()
#restorestate()

sim.runSim()                                # run parallel Neuron simulation

#savestate()


sim.gatherData()                            # gather spiking data and cell info from each node

sim.saveData()                              # save params, cell info and sim output to file (pickle,mat,txt,etc)#

sim.analysis.plotData()                     # plot spike raster etc

#fig1 = sim.analysis.plotRaster(include=[], labels='overlay', 
#            popRates=0, orderInverse=True, lw=0, markerSize=3.5, marker='.', popColors=[], 
#            showFig=0, saveFig=0, figSize=(8.5, 10), orderBy='gid')

fig1 = sim.analysis.plotRaster(orderInverse=True, markerSize=3.5, marker='.')
        
ax = fig1.gca()

[i.set_linewidth(0.5) for i in ax.spines.itervalues()] # make border thinner

plt.ylabel('Neuron number (ordered by NCD within each pop)')
plt.title('')

filename='%s/%s_raster_mod.png'%(cfg.saveFolder, cfg.simLabel)
plt.savefig(filename, dpi=600)
