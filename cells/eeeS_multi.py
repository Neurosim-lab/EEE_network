"""
CA229simp.py    : Simplified reconstructed morphology of prefrontal layer V pyramidal cell from Acker, Antic (2008)

Original:
https://senselab.med.yale.edu/ModelDB/ShowModel.cshtml?model=117207&file=/acker_antic/Model/CA%20229.hoc#tabs-2

Modified by : Peng (Penny) Gao <penggao.1987@gmail.com>
Feb 01, 2018
The cell class has 3d morphology structure infomation.
They can be placed in a network (logical 3d location).

Ref: https://neuroelectro.org/neuron/111/
     https://senselab.med.yale.edu/ModelDB/ShowModel.cshtml?model=168148&file=/stadler2014_layerV/LayerVinit.hoc#tabs-2

Simplified by : Joe Graham <joe.w.graham@gmail.com>
March 2018

"""
import sys
from neuron import h
from matplotlib import pyplot
from math import sqrt, pi, log, exp

h.load_file('stdrun.hoc')

#########################################
# Parameters
#########################################
# Cell passive properties
global_Ra = 100
spineFACTOR = 1.5
somaRm = 1500/0.04
dendRm = somaRm/spineFACTOR
somaCm = 1.45

dendCm = somaCm*spineFACTOR
spinedist = 40 # distance at which spines start
Vk = -87
VNa = 60
pasVm = -65
# Specify cell biophysics
somaNa = 900  # [pS/um2]
axonNa = 5000   # [pS/um2]
basalNa = 150  # [pS/um2]
mNa = 0.5  # decrease in sodium channel conductance in basal dendrites [pS/um2/um]
apicalNa = 375
gNamax = 2000  # maximum basal sodium conductance
vshiftna = -10

somaKv = 40 # somatic, apical, and initial basal Kv conductance
mKV = 0  # increase in KV conductance in basal dendrites
gKVmax = 500  # maximum basal KV conductance
axonKv = 100
somaKA = 150
mgka = 0.7  # linear rise in IA channel density
mgkaratio = 1./300 # linear drop in KAP portion, 1 at soma
apicalKA = 300  # apical total GKA conductance
gkamax = 2000  # pS/um2


somaCa = 2 #0.5 # total calcium channel conductance density of soma [pS/um^2]
# This value is original 2, set to 1 and 0.5 for better match with TTX trace
dendCa = 0.4 # dendritic total calcium conductance density

SomaCaT = 2
# This value is original 8, set to 4,2,1 or 0 for better match with TTX trace
dendCaT = 1.6  #0.5
cadistB = 30  # dendritic calcium channel conductance equals that of soma up until this distance
cadistA = 30
#gcaratio = 0.2 #portion of gHVA to gHVA+gIT total, 1 is all HVA, 0 is all IT#
gkl = 0.005
ILdist = 15

#############kBK.mod
kBK_gpeak = 2.68e-4 
kBK_caVhminShift = 45


#########################################
# Set up the eeeS cell class
#########################################

class eeeS():
    """
    A detailed model of Prefrontal layer V pyramidal neuron in Mouse.

    Channel distributions and all other biophysical properties of model basal
    dendrites of prefrontal layer V pyramidal cell from Acker, Antic (2008)
    Membrane Exitability and Action Potential Backpropagation in Basal Dendrites
    of Prefrontal Cortical Pyramidal Neurons.

    soma: soma compartments (soma[0] - soma[3])
    apical: apical dendrites (apical[0] - apical[44])
    basal: basal dendrites (basal[0] - basal[35])
    basals: SectionList of all basal but excluing basal[16]
    axon: SectionList of basal[16] (basal[16] is modeled as axon here)
    all: SectionList of all the above compartments
    """
    def __init__(self):
        self.create_cell()
        self.optimize_nseg()
        self.add_axon()
        self.add_all()
        self.addsomachan()
        self.addapicalchan()
        self.addbasalchan()
        self.addaxonchan()
        self.gna_control()
        self.distCa()
        self.distKV()
        self.distKA()
        self.distspines()
        self.add_ih()
        self.add_CaK()

    ###################
    # Set up nseg number
    ###################
    def geom_nseg (self):
        # local freq, d_lambda, before, after, tmp
        # these are reasonable values for most models
        freq = 100 # Hz, frequency at which AC length constant will be computed
        d_lambda = 0.05
        before = 0
        after = 0

        for sec in self.all: before += sec.nseg
        #soma area(0.5) # make sure diam reflects 3d points
        for sec in self.all:
            # creates the number of segments per section
            # lambda_f takes in the current section

            print
            print(sec.name())
            print(sec.nseg)

            if (sec.name() != "apical[0]") and (sec.name() != "axon[0]") and (sec.name() != "basal[9]") and (sec.name() != "basal[8]"):
                sec.nseg = int((sec.L/(d_lambda*self.lambda_f(sec))+0.9)/2)*2 + 1

            print(sec.nseg)
            print
        for sec in self.all: after += sec.nseg
        print("geom_nseg: changed from ", before, " to ", after, " total segments")

    def lambda_f (self, section):
        # these are reasonable values for most models
        freq = 100
        # The lowest number of n3d() is 2
        if (section.n3d() < 2):
            return 1e5*sqrt(section.diam/(4*pi*freq*section.Ra*section.cm))
        # above was too inaccurate with large variation in 3d diameter
        # so now we use all 3-d points to get a better approximate lambda
        x1 = section.arc3d(0)
        d1 = section.diam3d(0)
        self.lam = 0
        #print section, " n3d:", section.n3d(), " diam3d:", section.diam3d(0)
        for i in range(section.n3d()): #h.n3d()-1
            x2 = section.arc3d(i)
            d2 = section.diam3d(i)
            self.lam += (x2 - x1)/sqrt(d1 + d2)
            x1 = x2
            d1 = d2
            #  length of the section in units of lambda
        self.lam *= sqrt(2) * 1e-5*sqrt(4*pi*freq*section.Ra*section.cm)
        return section.L/self.lam

    def optimize_nseg (self):
        """
        Set up nseg
        """
        # Set up sectionList - easy to modify properties
        self.all = h.SectionList()
        self.all_no_axon = h.SectionList()
        for section in self.soma:
            self.all.append(sec = section)
            self.all_no_axon.append(sec = section)
        for section in self.basal:
            self.all.append(sec = section)
        for section in self.apical:
            self.all.append(sec = section)
            self.all_no_axon.append(sec = section)
        self.basals = h.SectionList()
        self.axons = h.SectionList()
        for section in self.axon:
            self.axons.append(sec = section)
            self.all.append(sec = section)
        for section in self.basal:
            self.basals.append(sec = section)
        #self.basals.remove(sec = self.basal[16])
        for section in self.basals:
            self.all_no_axon.append(sec = section)

        for sec in self.all:
            # Set up Ra and cm first, since the nseg calculation depends on the value of Ra and cm
            sec.Ra = global_Ra
            sec.cm = 1
        # give each compartment segment number
        #self.geom_nseg() # commented out by JWG, else simp model gets nsegs added

    ###################
    # Reset axon length
    ###################
    def add_axon(self):
        """
        Set up the SectionLists and temporal axon branch.
        """

        # self.axon[0].L = 200
        # self.axon[0].nseg = 5
        # h.distance(0,0.5,sec=self.soma[0])
        # for seg in self.axon[0].allseg():
        #     dist = h.distance(seg.x, sec=self.axon[0])
        #     if (dist <= 15):
        #         self.axon[0](seg.x).diam = 1.725
        #     elif (dist > 15 and dist<= 30):
        #         self.axon[0](seg.x).diam = 1.119
        #     else:
        #         self.axon[0](seg.x).diam = 0.96

        pass


    ###################
    # Add basic properties
    ###################
    def add_all(self):

        for sec in self.all:
            sec.insert('vmax')
            sec.insert('pas')
            sec.e_pas = pasVm
            sec.insert('na')
            sec.insert('na_ion')
            sec.insert('k_ion')
            sec.ena = VNa
            h.vshift_na = vshiftna
            sec.ek = Vk
            sec.insert('kv')


        for sec in self.all_no_axon:
            sec.insert('kap')
            sec.insert('ca')
            sec.insert('it')  # Properties from CaT.mod
            sec.vh1_it = 56
            sec.vh2_it = 415
            sec.ah_it = 30
            sec.v12m_it = 45
            sec.v12h_it = 65
            sec.am_it = 3
            sec.vshift_it = 10
            sec.vm1_it = 50
            sec.vm2_it = 125
            sec.insert('ca_ion')
            sec.eca = 140
            h.vshift_ca = 10
            sec.insert('cad')
            h.taur_cad = 100

    ###################
    # Set up properties only in soma
    ###################
    def addsomachan(self):
        for sec in self.soma:
            sec.cm = somaCm
            sec.g_pas = 1./somaRm
            # if h.ismembrane('na', sec = sec):
            #     sec.ena = VNa
            #     h.vshift_na = vshiftna
            # if h.ismembrane ('ca_ion', sec = sec):
            #     sec.eca = 140
            #     h.ion_style("ca_ion", 0, 1, 0, 0, 0)
            #     h.vshift_ca = 10

    ###################
    # Set up properties in apical dendrites
    ###################
    def addapicalchan(self):
        for sec in self.apical:
            sec.insert('kad')

    ###################
    # Set up properties in basal dendrites
    ###################
    def addbasalchan(self):
        for sec in self.basals:
            sec.insert('kad')

    ###################
    # Set up properties only in axon
    ###################
    def addaxonchan(self):
        for sec in self.axon:
            sec.cm = somaCm
            sec.g_pas = 1./somaRm
            h.thi1_na = -58
            h.thi2_na = -58

            sec.insert('kl')
            h.distance(0,0.5,sec=self.soma[0])
            for seg in sec.allseg():
                dist = h.distance(seg.x, sec=sec)
                if (dist>= ILdist):
                    sec(seg.x).gbar_kl = gkl
                else:
                    sec(seg.x).gbar_kl = 0

#########################################
# Distribution of sodium channels
#########################################
    def gna_control(self):
        for sec in self.soma:
            sec.gbar_na = somaNa

        for sec in self.basals:
            h.distance(0, 0.5, sec = self.soma[0])
            for seg in sec.allseg():
                dist = h.distance(seg.x, sec = sec)
                gNalin = basalNa - mNa * dist
                if (gNalin > gNamax):
                    gNalin = gNamax
                    print("Setting basal Na to maximum ",gNamax,
                    " at distance ",dist," in basal dendrite ", sec.name())
                elif (gNalin < 0):
                    gNalin = 0
                    print("Setting basal Na to zero at distance ",dist,
                    " in basal dendrite ",sec.name())
                sec(seg.x).gbar_na = gNalin

        for sec in self.axon:
            h.distance(0, 0.5, sec = self.soma[0])
            for seg in sec.allseg():
                dist = h.distance(seg.x, sec = sec)
                if (dist >= 50 and dist <= 100):
                    sec(seg.x).gbar_na = axonNa
                else:
                    sec(seg.x).gbar_na = somaNa

        for sec in self.apical:
            sec.gbar_na = apicalNa

#########################################
# Distribution of potassium channels
#########################################
    def distKV(self):
        for sec in self.soma:
            sec.gbar_kv = somaKv

        for sec in self.basals:
            h.distance(0,0.5,sec=self.soma[0])
            for seg in sec.allseg():
                dist = h.distance(seg.x, sec=sec)
                gKVlin = somaKv + mKV * dist
                if (gKVlin > gKVmax):
                    gKVlin = gKVmax
                    print("Setting basal GKV to maximum ",gKVmax," at distance ",dist," in basal dendrite",sec.name())
                elif (gKVlin < 0):
                    gKVlin = 0
                    print("Setting basal GKV to zero at distance ",dist," in basal dendrite ",sec.name())
                sec(seg.x).gbar_kv = gKVlin

        for sec in self.axon:
            sec.gbar_kv = axonKv

        for sec in self.apical:
            sec.gbar_kv = somaKv

#########################################
# Distribution of potassium channels
#########################################
    def distKA(self):

        for sec in self.soma:
            gkabar_kap = somaKA/1e4

        for sec in self.basals:
            h.distance(0,0.5,sec=self.soma[0])
            for seg in sec.allseg():
                dist = h.distance(seg.x, sec=sec)
                gkalin = somaKA + mgka*dist
                ratiolin = 1 - mgkaratio*dist
                if (ratiolin < 0):
                    ratio = 0
                else:
                    ratio = ratiolin

                if (gkalin > gkamax):
                    gkalin = gkamax
                    print("Setting GKA to maximum ",gkamax," in basal dendrite",sec.name())
                elif (gkalin < 0):
                    gkalin = 0
                    print("Setting GKA to 0 in basal dendrite",sec.name())
                sec(seg.x).gkabar_kap = gkalin * ratio/1e4
                sec(seg.x).gkabar_kad = gkalin * (1-ratio)/1e4

        for sec in self.apical:
            h.distance(0,0.5,sec=self.soma[0])
            for seg in sec.allseg():
                dist = h.distance(seg.x, sec=sec)
                ratiolin = 1 - mgkaratio*dist
                if (ratiolin < 0):
                    ratio = 0
                else:
                    ratio = ratiolin
                sec(seg.x).gkabar_kap = apicalKA*ratio/1e4
                sec(seg.x).gkabar_kad = apicalKA*(1-ratio)/1e4

#########################################
# Distribution of Ca channels
#########################################
    def distCa(self):
        for sec in self.soma:
            sec.gbar_ca = somaCa
            sec.gbar_it = SomaCaT/1e4

        for sec in self.basals:
            h.distance(0,0.5,sec = self.soma[0])
            for seg in sec.allseg():
                dist = h.distance(seg.x, sec = sec)
                if (dist > cadistB):
                    sec(seg.x).gbar_ca = dendCa
                    sec(seg.x).gbar_it = dendCaT/1e4
                else:
                    sec(seg.x).gbar_ca = somaCa
                    sec(seg.x).gbar_it = SomaCaT/1e4

        for sec in self.apical:
            h.distance(0,0.5,sec = self.soma[0])
            for seg in sec.allseg():
                dist = h.distance(seg.x, sec=sec)
                if (dist > cadistA):
                    sec(seg.x).gbar_ca = dendCa
                    sec(seg.x).gbar_it = dendCaT/1e4
                else:
                    sec(seg.x).gbar_ca = somaCa
                    sec(seg.x).gbar_it = SomaCaT/1e4

#########################################
# Distribution of spines on dendrites (This should be optimized!!!)
#########################################
    def distspines(self):
        for sec in self.basals:
            h.distance(0,0.5,sec = self.soma[0])
            for seg in sec.allseg():
                dist = h.distance(seg.x, sec=sec)
                if (dist >= spinedist):
                    sec(seg.x).cm = dendCm
                    sec(seg.x).g_pas = 1./dendRm
                else:
                    sec(seg.x).cm = somaCm
                    sec(seg.x).g_pas = 1./somaRm

        for sec in self.apical:
            h.distance(0,0.5,sec = self.soma[0])
            for seg in sec.allseg():
                dist = h.distance(seg.x, sec=sec)
                if (dist >= spinedist):
                    sec(seg.x).cm = dendCm
                    sec(seg.x).g_pas = 1./dendRm
                else:
                    sec(seg.x).cm = somaCm
                    sec(seg.x).g_pas = 1./somaRm

#########################################
# Add Ih channels
#########################################
    def add_ih(self):
        for sec in self.soma:
            sec.insert('Ih')
            sec.gIhbar_Ih = 0.0001

        for sec in self.basals:
            sec.insert('Ih')
            sec.gIhbar_Ih = 0.0001

        for sec in self.apical:
            sec.insert('Ih')
            h.distance(0,0.5,sec=self.soma[0])
            for seg in sec.allseg():
                dist = h.distance(seg.x, sec=sec)
                sec(seg.x).gIhbar_Ih = 0.0002*(-0.8696 + 2.0870*exp(dist/323))

#########################################
# Add calcium activated potassium current
#########################################
    # def add_SK(self):
    #     for sec in self.soma:
    #         sec.insert('SK_E2')
    #         sec.gSK_E2bar_SK_E2 = 0.00024 #0.0024 #0.00441
    #     # for sec in self.basals:
    #     #     sec.insert('SK_E2')
    #     #     sec.gSK_E2bar_SK_E2 = 0.0004 #0.0024 #0.00441
    #     for sec in self.apical:
    #         sec.insert('SK_E2')
    #         sec.gSK_E2bar_SK_E2 = 0.0012

    def add_CaK(self):
        for sec in self.apical:
            sec.insert('kBK')
            sec.gpeak_kBK = kBK_gpeak
            sec.caVhmin_kBK = -46.08 + kBK_caVhminShift
        for sec in self.basals:
            sec.insert('kBK')
            sec.gpeak_kBK = kBK_gpeak
            sec.caVhmin_kBK = -46.08 + kBK_caVhminShift
        for sec in self.soma:
            sec.insert('kBK')
            sec.gpeak_kBK = kBK_gpeak
            sec.caVhmin_kBK = -46.08 + kBK_caVhminShift

#########################################
# TTX
#########################################
    def TTX(self):
        for sec in self.all:
            sec.gbar_na = 0


#########################################
# No calcium
#########################################
    def no_ca(self):
        for sec in self.soma:
            sec.gbar_ca = 0
            sec.gbar_it = 0
        for sec in self.apical:
            sec.gbar_ca = 0
            sec.gbar_it = 0
        for sec in self.basals:
            sec.gbar_ca = 0
            sec.gbar_it = 0
#########################################
# 3D geometry of the cell
#########################################
    def create_cell(self):
        """
        3D morphology of CA229simp cell.
        The diam and L of each compartment is determined by 3D structure.
        Same as hoc 3D morphology: CA229.hoc
        """
        self.soma = [h.Section(name='soma[%d]' % i) for i in range(4)]
        self.apical = [h.Section(name='apical[0]')]
        self.basal = [h.Section(name='basal[%d]' % i) for i in range(10)]
        self.axon = [h.Section(name='axon[0]')]


        # Set up the 3d morphology and connection of soma
        h.pt3dclear(sec = self.soma[0])
        h.pt3dstyle(1, -53.42,3.52,-5.95,13.43, sec = self.soma[0])
        h.pt3dadd(-53.42,3.52,-5.96,13.43, sec = self.soma[0])

        self.soma[1].connect(self.soma[0])
        h.pt3dclear(sec = self.soma[1])
        h.pt3dadd(-53.42,3.52,-5.96,13.43, sec = self.soma[1])
        h.pt3dadd(-53.74,0.93,-5.96,15.35, sec = self.soma[1])
        h.pt3dadd(-54.06,-1.66,-5.96,11.51, sec = self.soma[1])

        self.soma[3].connect(self.soma[0])
        h.pt3dclear(sec = self.soma[3])
        h.pt3dadd(-53.42,3.52,-5.96,13.43, sec = self.soma[3])
        h.pt3dadd(-53.1,6.12,-5.96,11.19, sec = self.soma[3])
        h.pt3dadd(-52.78,8.71,-5.96,9.59, sec = self.soma[3])
        h.pt3dadd(-52.78,11.62,-5.96,7.36, sec = self.soma[3])
        h.pt3dadd(-53.1,14.22,-5.96,5.76, sec = self.soma[3])

        self.soma[2].connect(self.soma[1])
        h.pt3dclear(sec = self.soma[2])
        h.pt3dadd(-54.06,-1.66,-5.96,11.51, sec = self.soma[2])
        h.pt3dadd(-54.06,-4.25,-5.96,7.99, sec = self.soma[2])

        # Set up the 3d morphology and connection of basal dendrites



        self.basal[0].connect(self.soma[0])
        h.pt3dclear(sec = self.basal[0])
        h.pt3dadd(-53.42,3.52,-5.96,2.5, sec = self.basal[0])
        h.pt3dadd(-60.3,3.99,0.28,1.28, sec = self.basal[0])
        h.pt3dadd(-64.028,3.787,1.455,1.28, sec = self.basal[0])
        h.pt3dadd(-68.616,2.577,1.405,1.28, sec = self.basal[0])
        h.pt3dadd(-72.55,1.133,1.864,1.28, sec = self.basal[0])
        h.pt3dadd(-77.03,0.483,3.784,1.28, sec = self.basal[0])

        self.basal[1].connect(self.basal[0])
        h.pt3dclear(sec = self.basal[1])
        h.pt3dadd(-77.03,0.483,3.784,1.28, sec = self.basal[1])
        h.pt3dadd(-80.68,2.633,0.564,0.96, sec = self.basal[1])
        h.pt3dadd(-84.2,3.613,-0.576,0.96, sec = self.basal[1])
        h.pt3dadd(-88.771,4.452,-1.634,0.96, sec = self.basal[1])
        h.pt3dadd(-93.902,6.048,-2.616,0.96, sec = self.basal[1])
        h.pt3dadd(-96.462,6.688,-4.516,0.96, sec = self.basal[1])
        h.pt3dadd(-100.622,5.718,-5.996,0.96, sec = self.basal[1])
        h.pt3dadd(-102.852,5.718,-7.876,0.96, sec = self.basal[1])

        self.basal[2].connect(self.basal[1])
        h.pt3dclear(sec = self.basal[2])
        h.pt3dadd(-102.852,5.718,-7.876,0.96, sec = self.basal[2])
        h.pt3dadd(-102.852,3.128,-17.756,0.64, sec = self.basal[2])
        h.pt3dadd(-101.262,2.478,-21.296,0.64, sec = self.basal[2])
        h.pt3dadd(-100.622,-1.082,-24.456,0.64, sec = self.basal[2])
        h.pt3dadd(-101.892,-1.732,-27.696,0.64, sec = self.basal[2])
        h.pt3dadd(-103.172,-2.702,-35.536,0.64, sec = self.basal[2])
        h.pt3dadd(-105.092,-3.032,-41.596,0.64, sec = self.basal[2])
        h.pt3dadd(-105.412,-2.052,-46.196,0.64, sec = self.basal[2])
        h.pt3dadd(-107.012,-1.412,-47.816,0.64, sec = self.basal[2])
        h.pt3dadd(-108.932,-1.412,-50.276,0.64, sec = self.basal[2])
        h.pt3dadd(-110.212,0.538,-52.336,0.496, sec = self.basal[2])
        h.pt3dadd(-110.212,1.508,-56.156,0.476, sec = self.basal[2])

        self.basal[3].connect(self.basal[1])
        h.pt3dclear(sec = self.basal[3])
        h.pt3dadd(-102.852,5.718,-7.876,0.96, sec = self.basal[3])
        h.pt3dadd(-104.452,5.398,-7.876,0.96, sec = self.basal[3])
        h.pt3dadd(-108.932,5.718,-9.356,0.804, sec = self.basal[3])

        self.basal[4].connect(self.basal[3])
        h.pt3dclear(sec = self.basal[4])
        h.pt3dadd(-108.932,5.718,-9.356,0.804, sec = self.basal[4])
        h.pt3dadd(-113.092,4.428,-12.676,0.64, sec = self.basal[4])
        h.pt3dadd(-115.332,3.128,-12.676,0.782, sec = self.basal[4])
        h.pt3dadd(-118.842,3.128,-14.996,0.738, sec = self.basal[4])
        h.pt3dadd(-121.402,2.158,-17.416,0.73, sec = self.basal[4])
        h.pt3dadd(-124.282,1.188,-17.416,0.64, sec = self.basal[4])

        self.basal[5].connect(self.basal[4])
        h.pt3dclear(sec = self.basal[5])
        h.pt3dadd(-124.282,1.188,-17.416,0.64, sec = self.basal[5])
        h.pt3dadd(-127.162,0.858,-20.256,0.64, sec = self.basal[5])
        h.pt3dadd(-129.082,0.858,-20.256,0.64, sec = self.basal[5])
        h.pt3dadd(-131.632,-1.732,-22.016,0.64, sec = self.basal[5])
        h.pt3dadd(-134.192,-3.352,-24.736,0.64, sec = self.basal[5])
        h.pt3dadd(-138.352,-4.322,-29.736,0.64, sec = self.basal[5])
        h.pt3dadd(-140.592,-5.622,-32.256,0.64, sec = self.basal[5])
        h.pt3dadd(-143.472,-6.912,-32.256,0.64, sec = self.basal[5])
        h.pt3dadd(-146.342,-6.912,-35.356,0.64, sec = self.basal[5])
        h.pt3dadd(-149.222,-7.562,-37.116,0.64, sec = self.basal[5])
        h.pt3dadd(-152.102,-7.562,-37.936,0.64, sec = self.basal[5])
        h.pt3dadd(-154.022,-7.562,-37.916,0.64, sec = self.basal[5])
        h.pt3dadd(-157.222,-8.212,-39.196,0.64, sec = self.basal[5])
        h.pt3dadd(-159.782,-10.152,-39.636,0.64, sec = self.basal[5])
        h.pt3dadd(-162.332,-11.452,-43.116,0.64, sec = self.basal[5])
        h.pt3dadd(-165.852,-13.392,-44.816,0.516, sec = self.basal[5])
        h.pt3dadd(-168.092,-14.042,-47.096,0.486, sec = self.basal[5])

        self.basal[6].connect(self.basal[4])
        h.pt3dclear(sec = self.basal[6])
        h.pt3dadd(-124.282,1.188,-17.416,0.64, sec = self.basal[6])
        h.pt3dadd(-126.522,-2.052,-19.176,0.58, sec = self.basal[6])
        h.pt3dadd(-130.042,-4.972,-19.176,0.588, sec = self.basal[6])
        h.pt3dadd(-133.872,-5.942,-17.176,0.622, sec = self.basal[6])
        h.pt3dadd(-137.072,-8.212,-17.176,0.664, sec = self.basal[6])
        h.pt3dadd(-139.312,-9.832,-17.176,0.656, sec = self.basal[6])
        h.pt3dadd(-142.512,-12.422,-17.596,0.618, sec = self.basal[6])
        h.pt3dadd(-146.342,-12.752,-16.076,0.648, sec = self.basal[6])
        h.pt3dadd(-149.862,-13.072,-17.236,0.514, sec = self.basal[6])
        h.pt3dadd(-153.062,-12.752,-18.816,0.612, sec = self.basal[6])
        h.pt3dadd(-155.942,-12.422,-20.536,0.498, sec = self.basal[6])
        h.pt3dadd(-159.142,-11.772,-23.916,0.404, sec = self.basal[6])

        self.basal[7].connect(self.basal[3])
        h.pt3dclear(sec = self.basal[7])
        h.pt3dadd(-108.932,5.718,-9.356,0.804, sec = self.basal[7])
        h.pt3dadd(-114.692,7.338,-3.716,0.72, sec = self.basal[7])
        h.pt3dadd(-119.482,8.638,1.824,0.758, sec = self.basal[7])
        h.pt3dadd(-122.362,9.288,5.544,0.658, sec = self.basal[7])
        h.pt3dadd(-125.882,10.578,7.024,0.676, sec = self.basal[7])
        h.pt3dadd(-131.002,10.908,9.624,0.598, sec = self.basal[7])
        h.pt3dadd(-133.552,13.498,10.304,0.652, sec = self.basal[7])
        h.pt3dadd(-136.752,14.788,11.724,0.546, sec = self.basal[7])
        h.pt3dadd(-138.992,16.088,13.144,0.614, sec = self.basal[7])
        h.pt3dadd(-144.112,18.358,14.244,0.476, sec = self.basal[7])

        self.basal[8].connect(self.basal[0])
        h.pt3dclear(sec = self.basal[8])
        h.pt3dadd(-77.03,0.483,3.784,1.28, sec = self.basal[8])
        h.pt3dadd(-80.23,-0.487,1.264,0.788, sec = self.basal[8])
        h.pt3dadd(-82.47,-0.487,1.084,0.852, sec = self.basal[8])
        h.pt3dadd(-85.35,-2.107,0.664,0.75, sec = self.basal[8])
        h.pt3dadd(-88.084,-4.512,0.566,0.848, sec = self.basal[8])
        h.pt3dadd(-90.408,-7.229,0.826,0.952, sec = self.basal[8])
        h.pt3dadd(-93.59,-9.125,0.336,0.918, sec = self.basal[8])
        h.pt3dadd(-96.47,-9.445,-0.304,0.732, sec = self.basal[8])
        h.pt3dadd(-98.07,-11.395,-1.384,0.852, sec = self.basal[8])
        h.pt3dadd(-99.35,-13.985,-1.924,0.806, sec = self.basal[8])
        h.pt3dadd(-101.59,-16.895,-2.324,0.834, sec = self.basal[8])
        h.pt3dadd(-104.47,-20.135,-3.244,0.872, sec = self.basal[8])
        h.pt3dadd(-106.502,-23.151,-3.947,0.784, sec = self.basal[8])
        h.pt3dadd(-108.055,-26.209,-4.515,0.798, sec = self.basal[8])
        h.pt3dadd(-110.728,-29.518,-5.631,0.798, sec = self.basal[8])
        h.pt3dadd(-113.278,-32.758,-9.111,0.756, sec = self.basal[8])
        h.pt3dadd(-116.798,-35.348,-10.931,0.776, sec = self.basal[8])
        h.pt3dadd(-119.038,-37.288,-14.551,0.786, sec = self.basal[8])
        h.pt3dadd(-121.278,-39.558,-17.851,0.732, sec = self.basal[8])
        h.pt3dadd(-124.798,-42.148,-20.151,0.788, sec = self.basal[8])
        h.pt3dadd(-127.15,-46.524,-19.989,0.748, sec = self.basal[8])
        h.pt3dadd(-130.234,-50.645,-19.025,0.712, sec = self.basal[8])
        h.pt3dadd(-132.082,-54.729,-18.852,0.64, sec = self.basal[8])
        h.pt3dadd(-134.952,-57.639,-18.852,0.64, sec = self.basal[8])
        h.pt3dadd(-137.192,-60.229,-22.812,0.64, sec = self.basal[8])
        h.pt3dadd(-140.072,-62.499,-24.332,0.64, sec = self.basal[8])
        h.pt3dadd(-143.272,-64.449,-23.972,0.64, sec = self.basal[8])
        h.pt3dadd(-145.192,-66.709,-23.972,0.64, sec = self.basal[8])
        h.pt3dadd(-147.752,-69.309,-26.752,0.64, sec = self.basal[8])
        h.pt3dadd(-149.982,-72.219,-25.852,0.64, sec = self.basal[8])
        h.pt3dadd(-150.302,-77.079,-26.312,0.64, sec = self.basal[8])
        h.pt3dadd(-152.222,-79.999,-27.112,0.64, sec = self.basal[8])
        h.pt3dadd(-153.182,-83.889,-27.772,0.64, sec = self.basal[8])
        h.pt3dadd(-156.062,-87.119,-28.132,0.64, sec = self.basal[8])
        h.pt3dadd(-157.342,-91.009,-28.052,0.64, sec = self.basal[8])
        h.pt3dadd(-158.822,-95.029,-26.292,0.64, sec = self.basal[8])
        h.pt3dadd(-160.732,-99.569,-26.272,0.64, sec = self.basal[8])
        h.pt3dadd(-162.012,-102.479,-25.372,0.64, sec = self.basal[8])
        h.pt3dadd(-164.572,-106.049,-24.672,0.32, sec = self.basal[8])
        h.pt3dadd(-167.132,-110.579,-24.672,0.32, sec = self.basal[8])
        h.pt3dadd(-168.732,-116.409,-26.352,0.32, sec = self.basal[8])

        # add simplified sections
        self.axon[0].L = 200.0
        self.axon[0].diam = 1.03
        self.axon[0].nseg = 1
        self.axon[0].connect(self.soma[2])
        h.pt3dstyle(0, sec=self.axon[0])

        self.apical[0].L = 454.5
        self.apical[0].diam = 6.00
        self.apical[0].nseg = 1
        self.apical[0].connect(self.soma[3])
        h.pt3dstyle(0, sec=self.apical[0])

        self.basal[9].L = 157.2
        self.basal[9].diam = 6.00
        self.basal[9].nseg = 1
        self.basal[9].connect(self.soma[1])
        h.pt3dstyle(0, sec=self.basal[9])

        h.define_shape()

        self.basal[8].nseg = 3




############################################
# Function for importing cell into NetPyNE
############################################

def MakeCell():
    cell = eeeS()
    return cell
