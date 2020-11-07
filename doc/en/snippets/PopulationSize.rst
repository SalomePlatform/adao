.. index:: single: PopulationSize

PopulationSize
  *Integer value*. This key is used to define the (approximate) size of the
  population at each generation. This size is slightly adjusted to take into
  account the number of state variables to be optimized. The default value is
  100, and it is recommended to choose a population between 1 and about ten
  times the number of state variables, the size being smaller as the number of
  variables increases.

  Example:
  ``{"PopulationSize":100}``
