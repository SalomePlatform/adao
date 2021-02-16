.. index:: single: SimulatedObservationAtOptimum
.. index:: single: Forecast

SimulatedObservationAtOptimum
  *List of vectors*. Each element is a vector of observation obtained by the
  observation operator from the analysis or optimal state :math:`\mathbf{x}^a`.
  It is the observed forecast from the analysis or the optimal state, and it is
  sometimes called "*Forecast*".

  Example:
  ``hxa = ADD.get("SimulatedObservationAtOptimum")[-1]``
