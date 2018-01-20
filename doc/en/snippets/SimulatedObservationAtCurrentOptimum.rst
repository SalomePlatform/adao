.. index:: single: SimulatedObservationAtCurrentOptimum

SimulatedObservationAtCurrentOptimum
  *List of vectors*. Each element is a vector of observation simulated from
  the optimal state obtained at the current step the optimization algorithm,
  that is, in the observation space.

  Example :
  ``hxo = ADD.get("SimulatedObservationAtCurrentOptimum")[-1]``
