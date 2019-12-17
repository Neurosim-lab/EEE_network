COMMENT
//****************************//
// Created by Alon Polsky 	//
//    apmega@yahoo.com		//
//		2007			//
//****************************//
ENDCOMMENT

TITLE NMDA synapse 

NEURON {
	POINT_PROCESS nmda_spike
	USEION ca READ cai WRITE ica VALENCE 2
	NONSPECIFIC_CURRENT inmda 

	RANGE e ,gmax,inmda
	RANGE gnmda

	GLOBAL n, gama,tau1,tau2

}

UNITS {
	(nA) 	= (nanoamp)
	(mV)	= (millivolt)
	(nS) 	= (nanomho)
	(mM)    = (milli/liter)
        F	= 96480 (coul)
        R       = 8.314 (volt-coul/degC)

}

PARAMETER {
	gmax=1	(nS)
	e= 0.0	(mV)
	tau1=90	(ms)
	tau2=5	(ms)	
	gama=0.08 	(/mV) 
	dt (ms)
	v		(mV)
	n=0.25		(/mM) 
}

ASSIGNED { 
	inmda		(nA)   
	gnmda		(nS)
	ica 		(mA/cm2)
	cai		(mM)	
}
STATE {
	A (nS)
	B (nS)
}

INITIAL {
      gnmda=0 
	A=0
	B=0
}

BREAKPOINT {
	
	SOLVE state METHOD cnexp
	
	gnmda=(A-B)/(1+n*exp(-gama*v))
	
	inmda = (1e-3) * gnmda * (v-e)
	ica = inmda/10
}

DERIVATIVE state {
	
	A'=-A/tau1
	B'=-B/tau2
	
}

NET_RECEIVE (weight) {
	gmax=weight
	state_discontinuity( A, A+ gmax)
	state_discontinuity( B, B+ gmax)
}

