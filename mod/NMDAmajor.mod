:nmda.mod G. Major 20/2/95 23.i.99 synaptic conductance with nmda v-dependence

COMMENT

g_max has voltage dependence of nmda receptor
g_max not same as maximum gNMDA
looks like model from Brodin et al. J. Neurophysiol.
66(2) 1991: 473-84
with some parameters (alpha and beta) from Ascher and Novak 1988
J. Physiol. 399 247-266
need to change Mg to 1
kinetics of 3-exponential envelope based on
D'Angelo Rossi and Taglietti
Eur. J. Neurosci 6:640-645 (1994)
p_vspread=12.484 mV  p_vhalf=-19.906 mv Brodin et al 91, Ascher Novak 88 Mg 1.8
ENDCOMMENT

UNITS {
    (molar) = (/liter)
    (mM) = (millimolar)
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (umho) = (micromho)
    (uS) = (micromho)
}

NEURON {
    SUFFIX nmda
    POINT_PROCESS nmda
    NONSPECIFIC_CURRENT i
    RANGE onset, gmax, e, i, g, genv, q,
          Mg, taup, pinf,
          alf, alfA, alfslope,
          bet, betA, betslope,
          tau_on, tau_on0, tau_onslope,
          tau_off1, tau_off1_0, tau_off1slope,
          tau_off2, tau_off2_0, tau_off2slope,
          f_fast, f0, fslope,
          q10, Mg_time_factor
}

PARAMETER {
    celsius= 32 : 22 (degC)
    q10 = 3 ()
    Mg_time_factor = 1 ()
    dt (ms)
    onset=0 (ms)
    e=0	(mV)
    v	(mV)
    Mg= 1.8
    gmax = 0 (umho)  : uS
    alfslope = 47 (mV)
    alfA = 5.4 (/ms)
    betslope = 17 (mV)
    betA = 0.61(/mM-ms)
    tau_on0 = 2.915 (ms)
    tau_onslope = -0.004125 (ms/mV)
    tau_off1_0 = 61.5 (ms)
    tau_off1slope = 0.5625 (ms/mV)
    tau_off2_0 = 352.5 (ms)
    tau_off2slope = 5.7375 (ms/mV)
    f0 = 0.515  : should be unitless? was (mV) until 5/Mar/08
    fslope = -0.003125 (/mV)
}

ASSIGNED {
i (nA)  g (uS) genv (uS) pinf alf bet
taup (ms) tau_on (ms) tau_off1 (ms) tau_off2 (ms) f_fast
}

STATE {
 p q (nanocoulombs)
}

UNITSOFF

INITIAL {
   nmda_rates(v)
   nmda_taus(v,1.1*onset)
   p = pinf
   q = 0  : charge
}

BREAKPOINT {
    LOCAL trel
    SOLVE nmda_states METHOD cnexp
    if (t>onset) {
        trel= t - onset
    	genv = gmax*( -            exp(-trel/tau_on)
                   +     f_fast*exp(-trel/tau_off1)
                   + (1-f_fast)*exp(-trel/tau_off2)
                 ) : time dependent "maximum possible" or envelope conductance
        g=genv*p  : voltage dependency
    } else {
        genv=0
        g=0
    }
    i = g*(v - e)
}

DERIVATIVE nmda_states {
      nmda_rates(v) : compute p at this v and dt
      nmda_taus(v,t)
      p' = (pinf - p)/taup
      q' = i*(1e-3)  : dt  is in ms: want nC/ms not nC/s (nA)? i is in nA=10^-9 C/s, q' is in nC/ms = 10^-9/10^-3 C/s =10^-6 C/s
}

PROCEDURE nmda_taus(v,t) { : call once from HOC to initialise for each nmda syn
        LOCAL temp_factor
        temp_factor = q10^((celsius - 28.50)/10)
        if (t>onset) {
           f_fast= f0 + fslope*v
           if (f_fast>1) {
             f_fast=1
           }
           if (f_fast<0) {
             f_fast = 0
           }
           tau_on  =(tau_on0 + tau_onslope*v)/temp_factor
           tau_off1=(tau_off1_0 + tau_off1slope*v)/temp_factor
           tau_off2=(tau_off2_0 + tau_off2slope*v)/temp_factor
           if (tau_off1<tau_off1_0/10) {
              tau_off1=tau_off1_0/10
           }
           if (tau_off2<tau_off1) {
              tau_off2=tau_off1
           }
        }
}

PROCEDURE nmda_rates(v) { : call once from HOC to initialise
        LOCAL  temperature_factor :
        TABLE pinf, taup, alf, bet
          DEPEND q10, celsius,
                 alfA, betA, Mg, alfslope, betslope
          FROM -100 TO 100 WITH 200
        temperature_factor = q10^((celsius - 20)/10)
        alf = temperature_factor*alfA*exp(v/alfslope)
        bet = temperature_factor*betA*Mg*exp(-v/betslope)
        : Mg_time_factor = : is 1 in standard formula
	taup = Mg_time_factor/(alf + bet)
        :printf("\n NMDA taup %g  ms  (from time_factor %g) ", taup, Mg_time_factor)
        pinf = alf/(alf + bet)
}

UNITSON
