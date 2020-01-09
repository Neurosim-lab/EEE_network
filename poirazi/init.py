"""
init.py

Usage:
    python init.py

MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py
"""

#import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers
from netpyne import sim

cfg, netParams = sim.readCmdLineArgs()

sim.initialize(simConfig=cfg, netParams=netParams)
sim.net.createPops()
sim.net.createCells()
sim.net.connectCells()
sim.net.addStims()
sim.setupRecording()
sim.runSim()
sim.gatherData()
sim.saveData()
sim.analysis.plotData()
