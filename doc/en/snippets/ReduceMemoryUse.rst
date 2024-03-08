.. index:: single: ReduceMemoryUse

ReduceMemoryUse
  *Boolean value*. The variable leads to the activation, or not, of the memory
  footprint reduction mode at runtime, at the cost of a potential increase in
  calculation time. Results may differ above a certain precision (1.e-12 to
  1.e-14), usually close to machine precision (1.e-16). The default is "False",
  the choices are "True" or "False".

  Example:
  ``{"ReduceMemoryUse":False}``
