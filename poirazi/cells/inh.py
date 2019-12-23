#//Interneuron for PFC - fast spiking parvalbumin interneuron 
#//Based on Durstewitz and Gabriel 2006
#//"Irregular spiking in NMDA-driven prefrontal cortex neurons"

from neuron import h

# Soma properties
soma_nseg = 1
soma_L    = 53.0
soma_diam = 42.0

# Axon properties
axon_nseg = 1
axon_L    = 113.2 
axon_diam = 0.7

# General properties
cm    = 1.2    # microF/cm2
Ra    = 150.0
g_pas = 1.0/15000 # mho/cm
e_pas = -70

h.ko0_k_ion = 3.82   # mM
h.ki0_k_ion = 140.0  # mM


class inh():

    def __init__(self):
        self.create_cell()
        self.add_soma_channels()
        self.add_axon_channels()

    def create_cell(self):

        self.soma = h.Section(name='soma')
        self.soma.L    = soma_L
        self.soma.diam = soma_diam
        self.soma.nseg = soma_nseg
        self.soma.cm   = cm
        self.soma.Ra   = Ra

        self.axon = h.Section(name='axon')
        self.axon.L    = axon_L
        self.axon.diam = axon_diam
        self.axon.nseg = axon_nseg
        self.axon.cm   = cm
        self.axon.Ra   = Ra
        self.axon.connect(self.soma(0.5))

    def add_soma_channels(self):

        self.soma.insert('pas')
        self.soma.g_pas = g_pas
        self.soma.e_pas = e_pas

        self.soma.insert('Naf')
        self.soma.gnafbar_Naf = 0.045 * 5

        self.soma.insert('kdr')
        self.soma.gkdrbar_kdr = 0.018

        self.soma.insert('IKs')
        self.soma.gKsbar_IKs = 0.000725 * 0.1

    def add_axon_channels(self):

        self.axon.insert('pas')
        self.axon.g_pas = g_pas
        self.axon.e_pas = e_pas

        self.axon.insert('Naf')
        self.axon.gnafbar_Naf = 0.045 * 12

        self.axon.insert('kdr')
        self.axon.gkdrbar_kdr = 0.018


############################################
# Function for importing cell into NetPyNE
############################################

def makeCell():
    cell = inh()
    return cell