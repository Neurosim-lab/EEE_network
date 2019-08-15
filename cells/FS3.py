#//Interneuron for PFC - fast spiking parvalbumin interneuron 
#//Based on Durstewitz and Gabriel 2006
#//"Irregular spiking in NMDA-driven prefrontal cortex neurons"

from neuron import h

# Soma properties
soma_nseg = 1
soma_L    = 27.0
soma_diam = 29.0

soma_nafin   = 0.045 
soma_kdrin   = 0.018  
soma_Kslowin = 0.000725 * 0.1
soma_hin     = 0.00001
soma_kapin   = 0.0032 * 15
soma_canin   = 0.0003
soma_kctin   = 0.0001

# Axon properties
axon_nseg = 1
axon_L    = 115.0 
axon_diam = 1.5

axon_gnafbar_Nafx  = soma_nafin * 10  # Nafx
axon_gkdrbar_kdrin = soma_kdrin * 0.5 # kdrin

# Dend properties
dend_nseg = 1
dend_L    = 44.0 
dend_diam = 7.0

dend_gnafbar_Nafx  = 0.018 * 5       # Nafx
dend_gkdrbar_kdrin = 0.018 * 0.5     # kdrin
dend_gkabar_kapin  = soma_kapin * 10 # kapin

# General properties
cm    = 1.2    # microF/cm2
Ra    = 150.0
g_pas = 0.0001 # mho/cm
e_pas = -73.0  # (Kawaguchi k Kubota, 1993 --> -73+-3.9)

h.ko0_k_ion = 3.82   # mM
h.ki0_k_ion = 140.0  # mM
#h.celsius   = 23  # Temperature setting from original hoc file


class FS3():

    def __init__(self):
        self.create_cell()
        self.add_soma_channels()
        self.add_axon_channels()
        self.add_dend_channels()

    def create_cell(self):

        self.soma = h.Section(name='soma')
        self.soma.L    = 27.0
        self.soma.diam = 29.0
        self.soma.nseg = 1
        self.soma.cm   = cm
        self.soma.Ra   = Ra

        self.axon = h.Section(name='axon')
        self.axon.L    = 115.0
        self.axon.diam = 1.5
        self.axon.nseg = 1
        self.axon.cm   = cm
        self.axon.Ra   = Ra
        self.axon.connect(self.soma(0.5))

        self.dend = h.Section(name='dend')
        self.dend.L    = 44.0
        self.dend.diam = 7.0
        self.dend.nseg = 1
        self.dend.cm   = cm
        self.dend.Ra   = Ra
        self.dend.connect(self.soma(0.0))

    def add_soma_channels(self):

        self.soma.insert('pas')
        self.soma.g_pas = g_pas
        self.soma.e_pas = e_pas

        self.soma.insert('Nafx')
        self.soma.gnafbar_Nafx = soma_nafin

        self.soma.insert('kdrin')
        self.soma.gkdrbar_kdrin = soma_kdrin

        self.soma.insert('IKsin')
        self.soma.gKsbar_IKsin = soma_Kslowin

        self.soma.insert('hin')
        self.soma.gbar_hin = soma_hin

        self.soma.insert('kapin')
        self.soma.gkabar_kapin = soma_kapin

        self.soma.insert('canin')
        self.soma.gcalbar_canin = soma_canin

        self.soma.insert('kctin')
        self.soma.gkcbar_kctin = soma_kctin

        self.soma.insert('cadyn')

    def add_axon_channels(self):

        self.axon.insert('pas')
        self.axon.g_pas = g_pas
        self.axon.e_pas = e_pas

        self.axon.insert('Nafx')
        self.axon.gnafbar_Nafx = axon_gnafbar_Nafx

        self.axon.insert('kdrin')
        self.axon.gkdrbar_kdrin = axon_gkdrbar_kdrin

    def add_dend_channels(self):
        
        self.dend.insert('pas')
        self.dend.g_pas = g_pas
        self.dend.e_pas = e_pas

        self.dend.insert('Nafx')
        self.dend.gnafbar_Nafx = dend_gnafbar_Nafx

        self.dend.insert('kdrin')
        self.dend.gkdrbar_kdrin = dend_gkdrbar_kdrin

        self.dend.insert('kapin')
        self.dend.gkabar_kapin = dend_gkabar_kapin



############################################
# Function for importing cell into NetPyNE
############################################

def MakeCell():
    cell = FS3()
    return cell