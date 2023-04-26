.. index:: single: CognitiveAcceleration

CognitiveAcceleration
  *Real value*. This key indicates the recall rate at the best previously known
  value of the current insect. It is a floating point positive value. The
  default value is about :math:`1/2+ln(2)`, and it is recommended to adapt it,
  rather by reducing it, to the physical case that is being treated.

  Example :
  ``{"CognitiveAcceleration":1.19315}``
