.. index:: single: AmplitudeOfTangentPerturbation

AmplitudeOfTangentPerturbation
  *Real value*. This key indicates the relative numerical magnitude of the
  perturbation used to estimate the tangent value of the operator at the
  evaluation point, i.e. its directional derivative. The conservative default
  is 1.e-2, and it is strongly recommended to adapt it to the needs of real
  problems, by decreasing its value by several orders of magnitude.

  Example :
  ``{"AmplitudeOfTangentPerturbation":1.e-2}``
