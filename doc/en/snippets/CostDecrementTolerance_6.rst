.. index:: single: CostDecrementTolerance

CostDecrementTolerance
  This key indicates a limit value, leading to stop successfully the
  iterative optimization process when the cost function decreases less than
  this tolerance at the last step. The default is 1.e-6, and it is
  recommended to adapt it to the needs on real problems.

  Example : ``{"CostDecrementTolerance":1.e-6}``
