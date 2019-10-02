"""
init.py

Usage:
    python init.py # Run simulation, optionally plot a raster

MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py

Contributors: salvadordura@gmail.com
"""

#import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers
from netpyne import sim

cfg, netParams = sim.readCmdLineArgs()

sim.initialize(
    simConfig = cfg,    
    netParams = netParams)    # create network object and set cfg and net params
sim.net.createPops()          # instantiate network populations
sim.net.createCells()         # instantiate network cells based on defined populations
sim.net.connectCells()        # create connections between cells based on params
sim.net.addStims()            # add network stimulation
sim.setupRecording()          # setup variables to record (spikes, V traces, etc)
# sim.runSim()                  # run parallel Neuron simulation  
# sim.gatherData()              # gather spiking data and cell info from each node
sim.saveData()                # save params, cell info and sim output to file
#sim.analysis.plotData()       # plot spike raster etc



# connDict = {}

# for pop in sim.net.pops.keys():

#     print("Population: ", pop)
#     connDict[pop] = {}

#     popGids = sim.net.pops[pop].cellGids

#     for cellGid in popGids:

#         cell = sim.net.cells[cellGid]
#         allConns = cell.conns
#         synConns = [conn for conn in allConns if isinstance(conn['preGid'], int)]
#         excConns = [conn for conn in synConns if conn['synMech'] in ['NMDA', 'AMPA']]
#         inhConns = [conn for conn in synConns if conn['synMech'] in ['GABAAfast', 'GABAAslow']]

#         print("  Cell: ", cellGid, "excConns", len(excConns), "inhConns", len(inhConns))

#         # for conn in allConns:
#         #     if isinstance(conn['preGid'], int):
#         #         print("    preGid: ", conn['preGid'], "   synMech: ", conn['synMech'])









includePre  = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4','PV5']
includePost = ['PT5_1', 'PT5_2', 'PT5_3', 'PT5_4','PV5']
feature     = 'numConns' #'divergence' #'convergence' #'strength' # 
groupBy     = 'cell'
orderBy     = 'gid'

#sim.analysis.plotConn(includePre=includePre, includePost=includePost, feature=feature, groupBy=groupBy, orderBy=orderBy)

groupBy     = 'pop'

#sim.analysis.plotConn(includePre=includePre, includePost=includePost, feature=feature, groupBy=groupBy, orderBy=orderBy)














