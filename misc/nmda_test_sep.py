from neuron import h
h.load_file('stdrun.hoc')
import matplotlib.pyplot as plt
plt.ion()
import numpy as np

weight = 0.2

def nmda_test(weight, Tau2, Cdur, Beta, Alpha, title):

    sece2s = h.Section(name="sece2s")
    secdms = h.Section(name="secdms")

    e2s = h.MyExp2SynNMDABB(0.5, sec=sece2s)
    dms = h.NMDA(0.5, sec=secdms)
    
    e2s.tau2NMDA = Tau2
    dms.Cdur = Cdur
    dms.Beta = Beta
    dms.Alpha = Alpha

    t_vec = h.Vector()
    t_vec.record(h._ref_t)

    v_vece2s = h.Vector()
    v_vece2s.record(sece2s(0.5)._ref_v)

    v_vecdms = h.Vector()
    v_vecdms.record(secdms(0.5)._ref_v)

    dms_vec = h.Vector()
    dms_vec.record(dms._ref_g)
    dms_ivec = h.Vector()
    dms_ivec.record(dms._ref_iNMDA)
    dms_icavec = h.Vector()
    dms_icavec.record(dms._ref_ica)

    e2s_vec = h.Vector()
    e2s_vec.record(e2s._ref_g)
    e2s_ivec = h.Vector()
    e2s_ivec.record(e2s._ref_iNMDA)
    e2s_icavec = h.Vector()
    e2s_icavec.record(e2s._ref_ica)

    ns = h.NetStim() 
    ns.number = 1
    ns.interval = 200
    ns.start = 50
    ns.noise = 0

    nc1 = h.NetCon(ns, dms)
    nc1.delay = 1.0
    nc1.weight[0] = weight

    nc2 = h.NetCon(ns, e2s)
    nc2.delay = 1.0
    nc2.weight[0] = weight

def plot ():
    plt.figure()
    plt.plot(t_vec, dms_vec, 'b-', linewidth=1.5, label="DMS g")
    plt.plot(t_vec, e2s_vec, 'r-', linewidth=1.0, label="E2S g")
    plt.title(title)
    plt.legend()
    
    '''
    plt.figure()
    plt.plot(t_vec, dms_ivec, 'b-', linewidth=1.5, label="DMS iNMDA")
    plt.plot(t_vec, e2s_ivec, 'r-', linewidth=1.0, label="E2S iNMDA")
    plt.title(title)
    plt.legend()

    plt.figure()
    plt.plot(t_vec, dms_icavec, 'b-', linewidth=1.5, label="DMS iCa")
    plt.plot(t_vec, e2s_icavec, 'r-', linewidth=1.0, label="E2S iCa")
    plt.title(title)
    plt.legend()

    plt.figure()
    plt.plot(t_vec, v_vecdms, 'b-', linewidth=1.5, label="DMS V")
    plt.plot(t_vec, v_vece2s, 'r-', linewidth=1.0, label="E2S V")
    plt.title(title)
    plt.legend()        
    '''

# default values
Tau2 = 150
Cdur = 1.0
Beta = 0.01
Alpha = 4.0
title = "Default: Tau2=150, Cdur=1.0, Beta=0.01, Alpha=4.0"

#nmda_test(weight, Tau2, Cdur, Beta, Alpha, title)

# new values
Tau2 = 600
Cdur = 1.0 #40.0
Beta = 0.001667 #0.0015
Alpha = 1.0 #0.065
title = "New: Tau2=600, Cdur=40.0, Beta=0.001667, Alpha=0.065"

#nmda_test(weight, Tau2, Cdur, Beta, title)

weights = [0.1] #[0.06, 0.08, 0.10, 0.12]

def test ():
  for weight in weights:
    title = "Weight: " + str(weight)
    nmda_test(weight, Tau2, Cdur, Beta, Alpha, title)

