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

out = sim.analysis.iplotConn(saveFig=True, includePre=['pyrs_plat', 'pyrs', 'inhs', 'bkg'], includePost=['pyrs_plat', 'pyrs', 'inhs'], feature='numConns')
out = sim.analysis.iplotConn(saveFig=True, includePre=['pyrs_plat', 'pyrs', 'inhs', 'bkg'], includePost=['pyrs_plat', 'pyrs', 'inhs'], feature='strength')

out = sim.analysis.iplotConn(saveFig=True, includePre=['bkg'], includePost=['pyrs_plat', 'pyrs', 'inhs'], feature='numConns', groupBy='cell')
out = sim.analysis.iplotConn(saveFig=True, includePre=['bkg'], includePost=['pyrs_plat', 'pyrs', 'inhs'], feature='weight', groupBy='cell')

out = sim.analysis.iplotConn(saveFig=True, includePre=['pyrs_plat', 'pyrs', 'inhs'], includePost=['pyrs_plat', 'pyrs', 'inhs'], feature='numConns', groupBy='cell')
out = sim.analysis.iplotConn(saveFig=True, includePre=['pyrs_plat', 'pyrs', 'inhs'], includePost=['pyrs_plat', 'pyrs', 'inhs'], feature='weight', groupBy='cell')


out = sim.analysis.plotRaster(saveFig=True, orderInverse=True, popRates=True)
out = sim.analysis.plotRaster(saveFig=True, orderInverse=True, popRates=True, include=['pyrs_plat', 'pyrs', 'inhs'])

