.. index:: single: NumberOfSamplesForQuantiles

NumberOfSamplesForQuantiles
  This key indicates the number of simulation to be done in order to estimate
  the quantiles. This option is useful only if the supplementary calculation
  "SimulationQuantiles" has been chosen. The default is 100, which is often
  sufficient for correct estimation of common quantiles at 5%, 10%, 90% or
  95%.

  Example :
  ``{"NumberOfSamplesForQuantiles":100}``
