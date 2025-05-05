.. index:: single: GlobalCostReductionTolerance

GlobalCostReductionTolerance
  *Real value*. This key indicates the limit reduction factor, leading to the
  iterative optimization process being stopped when the cost function decreases
  by at least this tolerance over the entire optimal search. The default value
  is 1.e-16 (equivalent to no effect), and it is recommended to adapt it to the
  needs of real problems.

  Example:
  ``{"GlobalCostReductionTolerance":1.e-16}``
