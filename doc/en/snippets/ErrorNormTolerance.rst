.. index:: single: ErrorNormTolerance

ErrorNormTolerance
  *Real value*. This key specifies the value at which the residual associated
  with the approximation is acceptable, which leads to stop the optimal search.
  The default value is 1.e-7 (which is usually equivalent to almost no stopping
  criterion because the approximation is less precise), and it is recommended
  to adapt it to the needs for real problems. A usual value, recommended to
  stop the search on residual criterion, is 1.e-2.

  Example :
  ``{"ErrorNormTolerance":1.e-7}``
