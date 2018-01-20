.. index:: single: CostFunctionJbAtCurrentOptimum

CostFunctionJbAtCurrentOptimum
  *List of values*. Each element is a value of the error function :math:`J^b`. At
  each step, the value corresponds to the optimal state found from the
  beginning. If this part does not exist in the error function, its value is
  zero.

  Example :
  ``JbACO = ADD.get("CostFunctionJbAtCurrentOptimum")[:]``
