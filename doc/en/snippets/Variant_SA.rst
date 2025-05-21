.. index::
    single: Variant
    pair: Variant ; GeneralizedSimulatedAnnealing
    pair: Variant ; DualAnnealing

Variant
  *Predefined name*. This key allows to choose one of the possible variants
  for the main algorithm. The default variant is the original "DualAnnealing",
  and the possible choices are
  "GeneralizedSimulatedAnnealing" (Generalized Simulated Annealing ou GSA),
  "DualAnnealing" (Dual Annealing).

  It is recommended to try the "DualAnnealing" variant with a very small number
  of iterations and a limited number of simulation function evaluations.

  Example :
  ``{"Variant":"DualAnnealing"}``
