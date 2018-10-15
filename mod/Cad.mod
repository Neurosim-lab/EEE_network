
TITLE decay of internal calcium concentration
:
: Internal calcium concentration calculated from calcium currents
: and buffered by endogenous buffer and extrusion mechanism.
:
: Uses differential equations from Helmchen 1996
:dCa/dt = (dCa_T delta_t - (gamma*(dCa - Ca_rest)))/kb
: or dCa/dt = (dCa_T delta_t)/kb - (dCa - Ca_rest)/taur
: with  taur = kb/gamma
:
: to add exogenous buffer kb = 1+kendo+kexo
: for OGB-1 kexo = concOGB1/kd = 200uM/0.2uM => kb=1020
: for OGB-6 kexo = concOGB6/kd = 200uM/3uM   => kb=80
:
: mod file was modified from original version (Destexhe 92)
: use diam/4 instead of depth to calculate [Ca]
: Units checked using "modlunit" -> factor 10000 needed in ca entry
:
: Written by B Kampa May 2006


INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX cad
	USEION ca READ ica, cai WRITE cai
	RANGE ca
	GLOBAL depth,cainf,taur
}

UNITS {
	(molar) = (1/liter)			: moles do not appear in units
	(mM)	= (millimolar)
	(um)	= (micron)
	(mA)	= (milliamp)
	(msM)	= (ms mM)
	FARADAY = (faraday) (coulomb)
}


PARAMETER {
	diam		(um)
	depth	= .1	(um)		: no used anymore, uses diam/4 now
	taur	= 15	(ms)		: Ca decay from Sabatini 2002, uses kb/gamma now
	kb 	= 20			: buffer ratio from Sabatini 2002
	cainf	= 100e-6(mM)	: will be adjusted during init phase
	cai		(mM)
	gamma = 1.2	(1/ms)    : Tried 0.1 and 0.6 on Jan 31 by Penny, almost no difference on TTX condition
}

STATE {
	ca		(mM) <1e-5>
}

INITIAL {
	ca = cainf
	cai = ca
}

ASSIGNED {
	ica		(mA/cm2)
	drive_channel	(mM/ms)
}

BREAKPOINT {
	SOLVE state METHOD euler
}

DERIVATIVE state {
	depth = diam/4
	drive_channel =  - (10000) * ica / (2 * FARADAY * depth)
	if (drive_channel <= 0.) { drive_channel = 0. }	: cannot pump inward
	taur = kb/gamma
	ca' = (drive_channel/kb) + ((cainf-ca)/taur)
	cai = ca
}
