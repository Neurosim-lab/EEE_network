"""
batch_utils.py
Functions to deal with EEE batch data.
contact: joe.w.graham@gmail.com
"""

from netpyne.batch import Batch
import numpy as np
import os
from collections import OrderedDict
import json
import pickle
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from pprint import pprint
from netpyne import specs

batchdatadir = "data"


def getspineLocs(numspines, spinedist=[1]):
    numspines += 2
    numsecs = len(spinedist)
    spinespersec = []
    total_weight = sum(spinedist)
    for weight in spinedist:
        weight = float(weight)
        if weight > 0:
            share = weight / total_weight
        else:
            share = 0.0
        distributed = round(share * numspines)
        spinespersec.append(distributed)
        total_weight -= weight
        numspines -= distributed
    spineLocs = []
    for index, spines in enumerate(spinespersec):
        start = index * (1./numsecs)
        stop = (index + 1) * (1./numsecs)
        spineLocs.extend(np.linspace(start, stop, num=spines, endpoint=False).tolist())
    spineLocs = spineLocs[1:-1]
    return spineLocs


def run_batch(label, params, cfgFile, netParamsFile, batchdatadir="batch_data", grouped=None):
    """Runs a batch of simulations."""

    b = Batch(cfgFile=cfgFile, netParamsFile=netParamsFile)
    for k,v in params.iteritems():
        b.params.append({'label': k, 'values': v})
    if grouped is not None:
        for p in b.params:
            if p['label'] in grouped: 
                p['group'] = True
    b.batchLabel = label
    b.saveFolder = os.path.join(batchdatadir, b.batchLabel)
    b.method = 'grid'
    b.runCfg = {'type': 'mpi', 
                'script': 'batch_init.py', 
                'skip': True}
    b.run()


def readBatchData(dataFolder, batchLabel, loadAll=False, saveAll=True, vars=None, maxCombs=None, listCombs=None):
    # load from previously saved file with all data
    if loadAll:
        print('\nLoading single file with all data...')
        filename = '%s/%s/%s_allData.json' % (dataFolder, batchLabel, batchLabel)
        with open(filename, 'r') as fileObj:
            dataLoad = json.load(fileObj, object_pairs_hook=specs.OrderedDict)
        params = dataLoad['params']
        data = dataLoad['data']
        return params, data

    if isinstance(listCombs, basestring):
        filename = str(listCombs)
        with open(filename, 'r') as fileObj:
            dataLoad = json.load(fileObj)
        listCombs = dataLoad['paramsMatch']

    # read the batch file and cfg
    batchFile = '%s/%s/%s_batch.json' % (dataFolder, batchLabel, batchLabel)
    with open(batchFile, 'r') as fileObj:
        b = json.load(fileObj)['batch']

    # read params labels and ranges
    params = b['params']

    # read vars from all files - store in dict 
    if b['method'] == 'grid':
        labelList, valuesList = zip(*[(p['label'], p['values']) for p in params])
        valueCombinations = product(*(valuesList))
        indexCombinations = product(*[range(len(x)) for x in valuesList])
        data = {}
        print('Reading data...')
        missing = 0
        for i,(iComb, pComb) in enumerate(zip(indexCombinations, valueCombinations)):
            if (not maxCombs or i<= maxCombs) and (not listCombs or list(pComb) in listCombs):
                #print i, iComb
                # read output file
                iCombStr = ''.join([''.join('_'+str(i)) for i in iComb])
                simLabel = b['batchLabel']+iCombStr
                outFile = b['saveFolder']+'/'+simLabel+'.json'
                try:
                    with open(outFile, 'r') as fileObj:
                        output = json.load(fileObj, object_pairs_hook=specs.OrderedDict)

                    # save output file in data dict
                    data[iCombStr] = {}  
                    data[iCombStr]['paramValues'] = pComb  # store param values
                    if not vars: vars = output.keys()
                    for key in vars:
                        data[iCombStr][key] = output[key]

                except:
                    missing = missing + 1
                    output = {}
            else:
                missing = missing + 1

        print('%d files missing' % (missing))

        # save
        if saveAll:
            print('Saving to single file with all data')
            filename = '%s/%s/%s_allData.json' % (dataFolder, batchLabel, batchLabel)
            dataSave = {'params': params, 'data': data}
            with open(filename, 'w') as fileObj:
                json.dump(dataSave, fileObj)
        
        return params, data


def compare(source_file, target_file, source_key=None, target_key=None):
    from deepdiff import DeepDiff 
    with open(source_file, 'r') as fileObj:
        if source_file.endswith('.json'):
            source = json.load(fileObj, object_pairs_hook=specs.OrderedDict)
        elif source_file.endswith('.pkl'):
            source = pickle.load(fileObj)
    if source_key: source = source[source_key]

    with open(target_file, 'r') as fileObj:
        if target_file.endswith('.json'):
            target = json.load(fileObj, object_pairs_hook=specs.OrderedDict)
        elif source_file.endswith('.pkl'):
            target = pickle.load(fileObj)
    if target_key: target = target[target_key]
    
    ddiff = DeepDiff(source, target)
    pprint(ddiff)
    return ddiff


def setPlotFormat(numColors=8):
    from cycler import cycler
    plt.style.use('ggplot')
    #plt.style.use(['dark_background', 'presentation'])

    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 'large'

    NUM_COLORS = numColors
    colormap = plt.get_cmap('gist_rainbow')
    colorlist = [colormap(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]
    plt.rc('axes', prop_cycle=(cycler('color', colorlist)))


def load_json(filename, show=False):
    """Loads a json file into Python and pretty prints it."""
    with open(filename) as data_file:
        data = json.load(data_file)
        if show: pprint(data)
        return data


def list_batches():
    """Returns a list of all batchLabels (dir names in the current batchdatadir)."""
    files = os.listdir(batchdatadir)
    batches = []
    for file in files:
        if os.path.isdir(os.path.join(batchdatadir, file)):
            batches.append(file)
    return batches


def load_batch(batchLabel, batchdatadir=batchdatadir):
    """Returns the parameters and data from a batch, given its batchLabel."""
    params, data = readBatchData(batchdatadir, batchLabel, loadAll=0, saveAll=0, vars=None, maxCombs=None) 
    return params, data


def delete_batchdata(deletefigs=True):
    """Deletes the directory eee/sim/batch_data/. If deletefigs==True, also
    deletes eee/sim/batch_figs/."""
    
    batchdatadir = os.path.join(simdir, "batch_data")
    batchfigdir = os.path.join(simdir, "batch_figs")

    if os.path.isdir(batchdatadir):
        print("Removing directory: " + batchdatadir)
        if (os.path.realpath(batchdatadir) != batchdatadir):
            os.remove(os.path.join(os.curdir, batchdatadir))
        else:
            shutil.rmtree(batchdatadir, ignore_errors=True)
    if deletefigs:
        if os.path.isdir(batchfigdir):
            print("Removing directory: " + batchfigdir)
            if (os.path.realpath(batchfigdir) != batchfigdir):
                os.remove(batchfigdir)
            else:
                shutil.rmtree(batchfigdir, ignore_errors=True)


def rel_symlinks(batchesDir=None):
    """Create relative symlinks to necessary utility code in each batch dir."""

    import os
    if batchesDir is None:
        batchesDir = os.getcwd()

    os.chdir(batchesDir)
    print("Current directory: %s" % (os.getcwd()))

    links = ["batch_analysis.py", "batch_init.py", "batch_utils.py", "runmybatches", "x86_64"]

    batch_dirs = [name for name in os.listdir(batchesDir) if os.path.isdir(os.path.join(batchesDir, name)) and name.startswith("batch_")]

    for batch_dir in batch_dirs:
        os.chdir(batch_dir)
        print("  Current directory: %s" % (os.getcwd()))

        for link in links:
            if os.path.islink(link):
                print("    Current link: %s" % (link))
                print("      rm " + link)
                os.system("rm " + link)
            if link == "x86_64":
                print("      ln -s ../../" + link + " " + link)
                os.system("ln -s ../../" + link + " " + link)
            else:
                print("      ln -s ../" + link + " " + link)
                os.system("ln -s ../" + link + " " + link)

        os.chdir(os.path.dirname(os.getcwd()))


def import_excel(filename, index_col=0):
    """Imports data from Excel.  Returns a Pandas data frame as well as an 
    array for time and an array for each trace.  
    Assumes first column is time and remaining columns are traces.
    Assumes deciVolts and Seconds, and converts to mV and ms. 
    """

    import pandas as pd
    import numpy as np
    
    data = pd.read_excel(filename, index_col=index_col)

    data.index *= 1000 # convert s to ms
    data.iloc[:,:] *= 100 # convert to mV

    #time = data[data.columns[0]].values.tolist()
    #time = np.vstack(time) # Converts from 1d list to 2d column array

    # traces = np.array([])
    # for colind in np.arange(1, len(data.columns), 1):
    #     if not traces.any():
    #         traces = np.vstack(data[data.columns[colind]].values.tolist())
    #     else:
    #         traces = np.hstack((traces, np.vstack(data[data.columns[colind]].values.tolist())))

    return data #, time, traces



