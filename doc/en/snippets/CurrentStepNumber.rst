.. index:: single: CurrentStepNumber

CurrentStepNumber
  *List of integers*. Each element is the index of the current step in the
  iterative process, driven by the series of observations, of the algorithm
  used. This corresponds to the observation step used. Note: it is not the
  index of the current iteration of the algorithm even if it coincides for
  non-iterative algorithms.

  Example:
  ``i = ADD.get("CurrentStepNumber")[-1]``
