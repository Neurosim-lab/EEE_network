NEURON {
   SUFFIX vmax
   RANGE vm, tpeak
}

ASSIGNED {
   v (millivolt)
   vm (millivolt)
   tpeak (ms)
}

INITIAL {
    vm = v
    tpeak = t
}

BREAKPOINT { 
   if (v>vm) { 
      vm=v
      tpeak=t 
   }
}
