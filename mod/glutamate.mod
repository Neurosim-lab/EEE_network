COMMENT
//****************************//
// Created by Alon Polsky 	//
//    apmega@yahoo.com		//
//		2010			//
//****************************//
ENDCOMMENT

TITLE NMDA synapse with depression

NEURON {
	POINT_PROCESS glutamate
	NONSPECIFIC_CURRENT inmda,iampa
	RANGE del,Tspike,Nspike
	RANGE e ,gampamax,gnmdamax,local_v,inmda,iampa
	RANGE decayampa,decaynmda,dampa,dnmda
	RANGE gnmda,gampa

	GLOBAL n, gama,tau_ampa,taudampa,taudnmda
	GLOBAL tau1,tau2

	:USEION canmda WRITE icanmda VALENCE 2
	USEION ca WRITE ica
	GLOBAL icaconst
}

UNITS {
	(nA) 	= (nanoamp)
	(mV)	= (millivolt)
	(nS) 	= (nanomho)
	(mM)    = (milli/liter)
        F	= 96480 (coul)
        R       = 8.314 (volt-coul/degC)
 	PI = (pi) (1)
	(mA) = (milliamp)
	(um) = (micron)

}

PARAMETER {
	icaconst =0.1
	gnmdamax=1	(nS)
	gampamax=1	(nS)
	e= 0.0	(mV)
	tau1=50	(ms)
	tau2=2	(ms)
	tau_ampa=1	(ms)
	n=0.25 	(/mM)
	gama=0.08 	(/mV)
	dt (ms)
	v		(mV)
	del=30	(ms)
	Tspike=10	(ms)
	Nspike=1
 	decayampa=.5
	decaynmda=.5
	taudampa=200	(ms):tau decay
	taudnmda=200	(ms):tau decay
}

ASSIGNED {
	inmda		(nA)
	iampa		(nA)
	gnmda		(nS)
	local_v	(mV):local voltage
	:icanmda			(nA)
	ica			(nA)

}
STATE {
	A 		(nS)
	B 		(nS)
	gampa 	(nS)
	dampa
	dnmda
}

INITIAL {
      gnmda=0
      gampa=0
	A=0
	B=0
	dampa=1
	dnmda=1
	:icanmda=0
}

BREAKPOINT {

	LOCAL count
	SOLVE state METHOD cnexp
	FROM count=0 TO Nspike-1 {
		IF(at_time(count*Tspike+del)){
			state_discontinuity( A, A+ gnmdamax*(dnmda))
			state_discontinuity( B, B+ gnmdamax*(dnmda))
			state_discontinuity( gampa, gampa+ gampamax*dampa)
			state_discontinuity( dampa, dampa* decayampa)
			state_discontinuity( dnmda, dnmda* decaynmda)
		}
	}

	gnmda=(A-B)/(1+n*exp(-gama*v) )
	inmda =(1e-3)* gnmda  * (v-e)
	iampa= (1e-3)*gampa* (v- e)
	local_v=v
	:icanmda=inmda/10
	ica=inmda*0.1/(PI*diam)*icaconst
	inmda=inmda*.9

}

DERIVATIVE state {
	A'=-A/tau1
	B'=-B/tau2
	gampa'=-gampa/tau_ampa
	dampa'=(1-dampa)/taudampa
	dnmda'=(1-dnmda)/taudnmda
}
