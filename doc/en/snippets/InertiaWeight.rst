.. index:: single: InertiaWeight

InertiaWeight
  *Real value*. This key indicates the part of the insect velocity which is
  imposed by the swarm, named "inertia weight". It is a positive floating point
  value. It is a floating point value between 0 and 1. The default value is
  about :math:`1/(2*ln(2))` and it is recommended to adapt it to the physical
  case that is being treated.

  Example :
  ``{"InertiaWeight":0.72135}``
