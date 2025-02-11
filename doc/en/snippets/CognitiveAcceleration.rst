.. index:: single: CognitiveAcceleration

CognitiveAcceleration
  *Real value*. This key indicates the recall rate at the best previously known
  value of the current insect's history. It is a floating point positive value.
  The default value is about :math:`1/2+ln(2)=1.19315`, and it is recommended
  to adapt it, rather by reducing it, to the physical case that is being
  treated.

  In the standard (non-adaptive) case, this rate is constant and is equal to
  the indicated value. In the ASAPSO adaptive case [Wang09]_, the value of this
  key indicates the initial recall rate, which then decreases linearly with the
  number of generations and the associated "*CognitiveAccelerationControl*"
  factor.

  Example :
  ``{"CognitiveAcceleration":1.19315}``
