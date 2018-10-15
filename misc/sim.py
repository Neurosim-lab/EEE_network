"""
sim.py  : Runs simulations and analysis for EEE model
path    : eee/sim/
author  : Joe Graham <joe.w.graham@gmail.com>

Runs simulations and analysis for the EEE project.
For first use, include "runsims" at the command line to run all batches of
simulations.  It may then be necessary to run this file again to complete 
the analysis.

Usage:
% python eee/sim/sim.py runsims
% python eee/sim/sim.py

Interactive usage:
% ipython -i eee/sim/sim.py runsims
% ipython -i eee/sim/sim.py
"""

import eee_utils as eee
import os
import subprocess
import sys
import batches.batch_utils as batch_utils
import batches.batch_analysis as batch_analysis

orig_dir = os.getcwd()

all_batches = ['batch_fi']

############################################################
# Run all batches of simulations
############################################################

def run_batches(batches):
    for batch in batches:
        os.chdir(os.path.join(eee.simdir, 'batches', batch))
        subprocess.call("./runmybatches", shell=True)

# Calculate frequency-current relationships
def fi_curve():
    orig_dir = os.getcwd()
    os.chdir(os.path.join("batches", "batch_fi"))
    batch_analysis.plot_vtraces('fi_curve', par1label = "i", par2label="")
    params, data = batch_utils.load_batch('fi_curve')
    output = batch_analysis.meas_freq(params, data)
    batch_analysis.plot_measure(output, params, swapaxes=True)
    os.chdir(orig_dir)

# Calculate rheobase

# Calculate bAP amplitude and delay vs. distance from soma

# Increasing glutamate stim --> plateau figure

# Variety of parameter values vs glutamate stim amplitude:

#  NMDA decay time constant

#  Glutamate stim location

#  Spine neck resistance


if __name__ == "__main__":

    if "runsims" in sys.argv:
        print
        print("Running all batch simulations from eee/sim/sim.py")
        print("It may be necessary to re-execute this file to conduct analysis.")
        print
        run_batches(all_batches)
    else:
        print
        print("Running all analysis from eee/sim/sim.py")
        print
        fi_curve()

    
