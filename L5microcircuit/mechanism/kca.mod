TITLE Slow Ca-dependent potassium current
:   Ca++ dependent K+ current responsible for slow AHP

NEURON {
	SUFFIX kca
	USEION k READ ko, ki WRITE ik
	USEION ca READ cai
	RANGE  gbar, po, ik
	GLOBAL m_inf, tau_m
}


UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	(molar) = (1/liter)
	(mM) = (millimolar)
}

ASSIGNED {       : parameters needed to solve DE
	v               (mV)
	celsius         (degC)
	ek              (mV)
	cai             (mM)           : initial [Ca]i
	ik              (mA/cm2)
	po
	ki 		(mM)
	ko		(mM)
	m_inf
	tau_m           (ms)

}

PARAMETER {
	gbar    = 10   (mho/cm2)
	taumin  = 0	(ms)  
	b 	= 0.008 (/ms)  : changed oct 17, 2006 for pfc 

}


STATE {
	m   
}

BREAKPOINT { 
	SOLVE states METHOD cnexp
	ek = 25 * log(ko/ki)
	po = m*m
	ik = gbar*po*(v - ek)    : potassium current induced by this channel
}

DERIVATIVE states {
	rates(cai)


	m' = (m_inf - m) / tau_m 

	
} 


INITIAL {
	rates(cai)
	m = 0

}


PROCEDURE rates(cai(mM)) { 
	LOCAL a
:	a=100
:	m_inf=(a*cai*cai)/(a*cai*cai+b)
:	tau_m=(1/(a*cai*cai+b))
	
:old equations	
	a = cai/b
	m_inf = a/(a+1)

	tau_m = taumin+ 1(ms)*1(mM)*b/(cai+b)

}
