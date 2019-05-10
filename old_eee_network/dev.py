import json
from pprint import pprint



def load_json(filename, show=False):
    """Loads a json file into Python and pretty prints it."""
    with open(filename) as data_file:
        data = json.load(data_file)
        if show: pprint(data)
        return data


def detectDepolBlock(volt, minSamples=120, vRange=[-35, 0]):
    cumm = 0
    for v in volt:
        if v >= vRange[0] and v<= vRange[1]:
            cumm += 1
            if cumm > minSamples:
                return 1
        else:
            cumm = 0

    return 0 

def list_all_dbs():
    dbs = []
    for cell in cells:
        trace = data['simData']['v_soma'][cell]
        db = detectDepolBlock(trace)
        if db == 1:
            dbs.append(cell)   
    return dbs

def detectPlateaus(volt, minSamples=350, vRange=[-65, -45]):
    cumm = 0
    for v in volt:
        if v >= vRange[0] and v<= vRange[1]:
            cumm += 1
            if cumm > minSamples:
                return 1
        else:
            cumm = 0
    return 0 

def list_all_plateaus():
    plats = []
    for cell in cells:
        trace = data['simData']['v_soma'][cell]
        plat = detectPlateaus(trace)
        if plat == 1:
            plats.append(cell)   
    return plats


data = load_json('/u/sergioangulo/projects/sergeee/eee/data/v30/network140.json')
cells = ['cell_'+str(i) for i in range(200,1000)]
#cells = data['simData']['v_soma'].keys()
traces = [data['simData']['v_soma'][cell] for cell in cells]

def depblock():
    db_cells = list_all_dbs()         
    db_cells.sort()
    print("Number of Depol Block cells: " + str(len(db_cells)))
    print("Depol block cells:")
    print(db_cells)

def plateaus():
    plat_cells = list_all_plateaus()         
    plat_cells.sort()
    print("Number of plateau cells: " + str(len(plat_cells)))
    print("Percent of plateau cells: "+str((len(plat_cells)/400.0)*100.0)+"%")
    print("Plateau cells:")
    print(plat_cells)

depblock()
plateaus()