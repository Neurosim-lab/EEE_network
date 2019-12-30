# /* 4-compartment model of a deep layer PFC pyramidal cell */
# /* Based on Durstewitz et al. (2000), J.Neurophysiol. 83: 1733-50 */
# /* Papoutsi et al. (2014), Plos Computational Biology*/

from neuron import h

# Soma properties
soma_nseg = 3
soma_L    = 75.0
soma_diam = 10.14

# Axon properties
axon_nseg = 1
axon_L    = 113.2 
axon_diam = 1.1

# Basal dendrite properties
dend0_nseg = 9
dend0_L    = 150.0
dend0_diam = 1.0

# Proximal apical dendrite properties
dend1_nseg = 17
dend1_L    = 400.0 
dend1_diam = 3.4

# Distal apical dendrite properties
dend2_nseg = 5
dend2_L    = 400.0 
dend2_diam = 2.6

# General properties
e_pas       = -66.0  # mV
gCAN        = 0
h.ko0_k_ion = 3.82   # mM
h.ki0_k_ion = 140.0  # mM
cao0_ca_ion = 2.0    # mM
cai0_ca_ion = 50e-6  # mM


class pyr():

    def __init__(self):
        self.create_cell()
        self.add_soma_channels()
        self.add_axon_channels()
        self.add_dend0_channels()
        self.add_dend1_channels()
        self.add_dend2_channels()


    def create_cell(self):

        self.soma = h.Section(name='soma')
        self.soma.L    = soma_L
        self.soma.diam = soma_diam
        self.soma.nseg = soma_nseg

        self.axon = h.Section(name='axon')
        self.axon.L    = axon_L
        self.axon.diam = axon_diam
        self.axon.nseg = axon_nseg
        self.axon.connect(self.soma(0.5))
        
        self.dend = [h.Section(name='dend[%d]' % i) for i in range(3)]

        self.dend[0].L    = dend0_L
        self.dend[0].diam = dend0_diam
        self.dend[0].nseg = dend0_nseg
        self.dend[0].connect(self.soma(0.0))

        self.dend[1].L    = dend1_L
        self.dend[1].diam = dend1_diam
        self.dend[1].nseg = dend1_nseg
        self.dend[1].connect(self.soma(1.0))

        self.dend[2].L    = dend2_L
        self.dend[2].diam = dend2_diam
        self.dend[2].nseg = dend2_nseg
        self.dend[2].connect(self.dend[1](1.0))


    def add_soma_channels(self):

        self.soma.cm = 1.2
        self.soma.Ra = 100

        self.soma.insert('pas')
        self.soma.g_pas = 6e-5
        self.soma.e_pas = e_pas

        self.soma.insert('Naf')
        self.soma.gnafbar_Naf = 0.108 * 1.675

        self.soma.insert('Nap')
        self.soma.gnapbar_Nap = 1.8e-06 

        self.soma.insert('cal')
        self.soma.gcalbar_cal = 3e-05

        self.soma.insert('can')
        self.soma.gcabar_can = 2e-5 

        self.soma.insert('car')
        self.soma.gcabar_car = 3e-08 * 1000

        self.soma.insert('cat')
        self.soma.gcatbar_cat = 6e-06 

        self.soma.insert('kdr')
        self.soma.gkdrbar_kdr = 0.0054*4

        self.soma.insert('IKs')
        self.soma.gKsbar_IKs = 6e-4 *1.71 

        self.soma.insert('kad')
        self.soma.gkabar_kad = 7e-4 

        self.soma.insert('iC')
        self.soma.gkcbar_iC = 2.2e-3 

        self.soma.insert('h')
        self.soma.gbar_h = 9e-06 * 0.8
        
        self.soma.insert('kca')
        self.soma.gbar_kca = 0.025 * 5.6 

        self.soma.insert('ican')
        self.soma.gbar_ican = gCAN

        self.soma.insert('cadyn')


    def add_axon_channels(self):

        self.axon.cm = 1.2
        self.axon.Ra = 150

        self.axon.insert('pas')
        self.axon.g_pas = 8.5e-5
        self.axon.e_pas = e_pas

        self.axon.insert('Naf')
        self.axon.gnafbar_Naf = 0.18

        self.axon.insert('kdr')
        self.axon.gkdrbar_kdr = 0.0054


    def add_dend0_channels(self):

        self.dend[0].cm = 2.0
        self.dend[0].Ra = 100

        self.dend[0].insert('pas')
        self.dend[0].g_pas = 1.7e-04
        self.dend[0].e_pas = e_pas

        self.dend[0].insert('Naf')
        self.dend[0].gnafbar_Naf = 1.8e-3 

        self.dend[0].insert('Nap')
        self.dend[0].gnapbar_Nap = 1.8e-05 

        self.dend[0].insert('can')
        self.dend[0].gcabar_can = 6e-05 
        
        self.dend[0].insert('kdr')
        self.dend[0].gkdrbar_kdr = 0.0054 

        self.dend[0].insert('IKs')
        self.dend[0].gKsbar_IKs = 0.0006
        
        self.dend[0].insert('kad')
        self.dend[0].gkabar_kad = 0.0007

        self.dend[0].insert('h')
        self.dend[0].gbar_h = 9e-06 

        self.dend[0].insert('ican')
        self.dend[0].gbar_ican = gCAN*0.1

        self.dend[0].insert('cadyn')


    def add_dend1_channels(self):

        self.dend[1].cm = 1.2
        self.dend[1].Ra = 150

        self.dend[1].insert('pas')
        self.dend[1].g_pas = 8.5e-5 * 2
        self.dend[1].e_pas = e_pas

        self.dend[1].insert('Naf')
        self.dend[1].gnafbar_Naf = 5e-3

        self.dend[1].insert('Nap')
        self.dend[1].gnapbar_Nap = 5.4e-05 

        self.dend[1].insert('cal')
        self.dend[1].gcalbar_cal = 1.9e-4  

        self.dend[1].insert('can')
        self.dend[1].gcabar_can = 6e-05   

        self.dend[1].insert('car')
        self.dend[1].gcabar_car = 9e-08 * 1000

        self.dend[1].insert('cat')
        self.dend[1].gcatbar_cat = 6e-05  

        self.dend[1].insert('kdr')
        self.dend[1].gkdrbar_kdr = 2.16e-05 

        self.dend[1].insert('IKs')
        self.dend[1].gKsbar_IKs = 0.0012 

        self.dend[1].insert('kad')
        self.dend[1].gkabar_kad = 0.0007

        self.dend[1].insert('iC')
        self.dend[1].gkcbar_iC = 2.2e-05

        self.dend[1].insert('kca')
        self.dend[1].gbar_kca = 0.0025 *1.1

        self.dend[1].insert('h')
        self.dend[1].gbar_h = 1.4e-5      

        self.dend[1].insert('ican')
        self.dend[1].gbar_ican = gCAN*0.1

        self.dend[1].insert('cadyn')


    def add_dend2_channels(self):

        self.dend[2].cm = 1.2
        self.dend[2].Ra = 150

        self.dend[2].insert('pas')
        self.dend[2].g_pas = 8.5e-5 * 2
        self.dend[2].e_pas = e_pas

        self.dend[2].insert('Naf')
        self.dend[2].gnafbar_Naf = 3.6e-3

        self.dend[2].insert('Nap')
        self.dend[2].gnapbar_Nap = 1.8e-4  

        self.dend[2].insert('cal')
        self.dend[2].gcalbar_cal = 3.6e-6

        self.dend[2].insert('can')
        self.dend[2].gcabar_can = 0.001  

        self.dend[2].insert('car')
        self.dend[2].gcabar_car = 1.5e-06  *1000

        self.dend[2].insert('cat')
        self.dend[2].gcatbar_cat = 6e-06

        self.dend[2].insert('kdr')
        self.dend[2].gkdrbar_kdr = 5.4e-06    

        self.dend[2].insert('IKs')
        self.dend[2].gKsbar_IKs = 0.0012   

        self.dend[2].insert('kad')
        self.dend[2].gkabar_kad = 7e-05 

        self.dend[2].insert('iC')
        self.dend[2].gkcbar_iC = 2.2e-06 
        
        self.dend[2].insert('kca')
        self.dend[2].gbar_kca = 0.0025 * 1.1 * 0.01

        self.dend[2].insert('h')
        self.dend[2].gbar_h = 9e-05 

        self.dend[2].insert('ican')
        self.dend[2].gbar_ican = gCAN * 0.1

        self.dend[2].insert('cadyn')



############################################
# Function for importing cell into NetPyNE
############################################

def makeCell():
    cell = pyr()
    return cell