TITLE Fluctuating conductances with parallel random streams

COMMENT
-----------------------------------------------------------------------------
	Fluctuating conductance model for synaptic bombardment
        adapted from Gfluct.mod -- see for full comments
ENDCOMMENT        

: headers
NEURON	{ 
  POINT_PROCESS Gfluctp_old2
  THREADSAFE : only true if every instance has its own distinct Random
  RANGE g_e, g_i, E_e, E_i, g_e0, g_i0, g_e1, g_i1, seed1, seed2, seed3
  RANGE std_e, std_i, tau_e, tau_i, D_e, D_i

  RANGE rv, id
  NONSPECIFIC_CURRENT i
  POINTER internalpointer
}

UNITS {
	(nA) = (nanoamp) 
	(mV) = (millivolt)
	(umho) = (micromho)
}

PARAMETER {
  dt		(ms)
  E_e	= 0 	(mV)	: reversal potential of excitatory conductance
  E_i	= -75 	(mV)	: reversal potential of inhibitory conductance

  g_e0	= 0.0121 (umho)	: average excitatory conductance
  g_i0	= 0.0573 (umho)	: average inhibitory conductance

  std_e	= 0.0030 (umho)	: standard dev of excitatory conductance
  std_i	= 0.0066 (umho)	: standard dev of inhibitory conductance

  tau_e	= 2.728	(ms)	: time constant of excitatory conductance
  tau_i	= 10.49	(ms)	: time constant of inhibitory conductance
  seed1 = 1
  seed2 = 1
  seed3 = 1
}

ASSIGNED {
  internalpointer
  v	(mV)		: membrane voltage
  i 	(nA)		: fluctuating current
  g_e	(umho)		: total excitatory conductance
  g_i	(umho)		: total inhibitory conductance
  g_e1	(umho)		: fluctuating excitatory conductance
  g_i1	(umho)		: fluctuating inhibitory conductance
  D_e	(umho umho /ms) : excitatory diffusion coefficient
  D_i	(umho umho /ms) : inhibitory diffusion coefficient
  exp_e
  exp_i
  amp_e	(umho)
  amp_i	(umho)

  rv
  id
}

: some verbatim stuff
VERBATIM
#include "nrnran123.h"
ENDVERBATIM

: CONSTRUCTOR and INITIAL block
CONSTRUCTOR {
  VERBATIM
  id=ifarg(2)?(int)*getarg(2):17.2;
  ENDVERBATIM
  
}

INITIAL {
  VERBATIM
  // only this style initializes the stream on finitialize
  if (_p_internalpointer) { nrnran123_setseq((nrnran123_State*)_p_internalpointer, 0, 0); }
  ENDVERBATIM
  noiseFromRandom123()
  g_e1 = 0
  g_i1 = 0
  if(tau_e != 0) {
    D_e = 2 * std_e * std_e / tau_e
    exp_e = exp(-dt/tau_e)
    amp_e = std_e * sqrt( (1-exp(-2*dt/tau_e)) )
  }
  if(tau_i != 0) {
    D_i = 2 * std_i * std_i / tau_i
    exp_i = exp(-dt/tau_i)
    amp_i = std_i * sqrt( (1-exp(-2*dt/tau_i)) )
  }
}	

: BREAKPOINT
BREAKPOINT {
  SOLVE oup
  if(tau_e==0) {
    g_e = std_e * rand()
  }
  if(tau_i==0) {
    g_i = std_i * rand()
  }
  g_e = g_e0 + g_e1
  if(g_e < 0) { g_e = 0 }
  g_i = g_i0 + g_i1
  if(g_i < 0) { g_i = 0 }
  i = g_e * (v - E_e) + g_i * (v - E_i)
}

PROCEDURE oup() {
   if(tau_e!=0) {
	g_e1 =  exp_e * g_e1 + amp_e * rand()
   }
   if(tau_i!=0) {
	g_i1 =  exp_i * g_i1 + amp_i * rand()
   }
}

: FUNCTION rand()
FUNCTION rand () {
VERBATIM
  // Supports separate independent but reproducible streams for eaach instance. However, the corresponding hoc Random distribution MUST be set to Random.negexp(1)
  if (_p_internalpointer) {
     // _lrand = nrnran123_negexp((nrnran123_State*)_p_internalpointer);
     _lrand = nrnran123_normal((nrnran123_State*)_p_internalpointer);
  }
  ENDVERBATIM
}

: PROCEDURE noiseFromRandom123()
PROCEDURE noiseFromRandom123 () {
VERBATIM
  nrnran123_State** pv = (nrnran123_State**)(&_p_internalpointer);
  if (*pv) {
    nrnran123_deletestream(*pv);
    *pv = (nrnran123_State*)0;
  }
  if (ifarg(3)) {
    *pv = nrnran123_newstream3((uint32_t)*getarg(1), (uint32_t)*getarg(2), (uint32_t)*getarg(3));
  } else if (ifarg(2)) {
    *pv = nrnran123_newstream((uint32_t)*getarg(1), (uint32_t)*getarg(2));
  } else if (ifarg(1)) {
    *pv = nrnran123_newstream((uint32_t)*getarg(1), (uint32_t)0);
  } else {
    *pv = nrnran123_newstream3((uint32_t)seed1, (uint32_t)seed2, (uint32_t)seed3);
  }
ENDVERBATIM
}
