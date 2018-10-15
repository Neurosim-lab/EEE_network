COMMENT

Plateau-like conductance. Does not summate (1 shot only).

Corey Acker
September 2008

ENDCOMMENT

NEURON {
	POINT_PROCESS PlateauConductance
	RANGE onset, dur, tau_on, tau_off, gmax, e, i
	NONSPECIFIC_CURRENT i
    RANGE g
}
UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
}

PARAMETER {
	onset=0 (ms)
	dur=10 (ms)
	tau_on=.5 (ms)	<1e-3,1e6>
	tau_off=5 (ms)	<1e-3,1e6>
	gmax=0 (uS)	<0,1e9>
	e=0	(mV)
}

ASSIGNED { i (nA) g (uS) }

INITIAL {
	i = 0
      g = 0
}

BREAKPOINT {
	if (gmax) {
         at_time(onset)
         at_time(onset+dur)
      }
      if (t-onset < 0 || t-onset > 5*tau_off+dur) {
            i = 0
      } else {
            if (t - onset < dur) {
                 g = gmax*(1-exp(-(t-onset)/tau_on))
            } else {
                 g = gmax*(1-exp(-dur/tau_on))*exp(-(t-dur-onset)/tau_off)
            }
            i = g*(v-e)
      }
}
