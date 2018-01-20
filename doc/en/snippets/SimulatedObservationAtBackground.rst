.. index:: single: SimulatedObservationAtBackground
.. index:: single: Dry

SimulatedObservationAtBackground
  *List of vectors*. Each element is a vector of observation simulated by the
  observation operator from the background :math:`\mathbf{x}^b`. It is the
  forecast from the background, and it is sometimes called "*Dry*".

  Example :
  ``hxb = ADD.get("SimulatedObservationAtBackground")[-1]``
