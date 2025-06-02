.. index::
    single: Variant
    pair: Variant ; 3DVAR
    pair: Variant ; ExtendedBlue
    pair: Variant ; DerivativeFreeOptimization
    pair: Variant ; CanonicalPSO
    pair: Variant ; SPSO-2011-AIS-VLS
    pair: Variant ; 3DVARGradientOptimization
    pair: Variant ; ExtendedBlueOptimization
    pair: Variant ; DerivativeFreeOptimization
    pair: Variant ; CanonicalParticuleSwarmOptimization
    pair: Variant ; VariationalParticuleSwarmOptimization

Variant
  *Predefined name*. This key allows to choose one of the possible variants for
  the main calibration algorithm. The default variant is the original "3DVAR",
  and the possible choices are
  "3DVARGradientOptimization" or "3DVAR" (3DVAR type variational analysis),
  "ExtendedBlueOptimization" or "ExtendedBlue" (BLUE type semi-linear estimation),
  "DerivativeFreeOptimization" or "DFO" (derivative-free optimization using simplex or other approximations),
  "CanonicalParticuleSwarmOptimization" or "CanonicalPSO" ou "PSO" (canonical particle swarm optimization),
  "VariationalParticuleSwarmOptimization" or "SPSO-2011-AIS-VSL" (2011 standard particle swarm optimization, accelerated by local variational search),
  It is highly recommended to keep the default value.

  Example :
  ``{"Variant":"3DVAR"}``
