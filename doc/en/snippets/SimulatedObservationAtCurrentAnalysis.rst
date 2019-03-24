.. index:: single: SimulatedObservationAtCurrentAnalysis

SimulatedObservationAtCurrentAnalysis
  *List of vectors*. Each element is an observed vector simulated by the
  observation operator from the current analysis, that is, in the observation
  space. This quantity is identical to the observed vector simulated at
  current state in the case of a single-state assimilation.

  Example:
  ``hxs = ADD.get("SimulatedObservationAtCurrentAnalysis")[-1]``
