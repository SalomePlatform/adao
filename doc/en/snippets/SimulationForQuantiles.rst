.. index:: single: SimulationForQuantiles

SimulationForQuantiles
  This key indicates the type of simulation, linear (with the tangent
  observation operator applied to perturbation increments around the optimal
  state) or non-linear (with standard observation operator applied to
  perturbed states), one want to do for each perturbation. It changes mainly
  the time of each elementary calculation, usually longer in non-linear than
  in linear. This option is useful only if the supplementary calculation
  "SimulationQuantiles" has been chosen. The default value is "Linear", and
  the possible choices are "Linear" and "NonLinear".

  Example:
  ``{"SimulationForQuantiles":"Linear"}``
