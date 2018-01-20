.. index:: single: CostFunctionJoAtCurrentOptimum

CostFunctionJoAtCurrentOptimum
  *List of values*. Each element is a value of the error function :math:`J^o`,
  that is of the observation difference part. At each step, the value
  corresponds to the optimal state found from the beginning.

  Example :
  ``JoACO = ADD.get("CostFunctionJoAtCurrentOptimum")[:]``
