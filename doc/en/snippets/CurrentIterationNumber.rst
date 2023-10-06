.. index:: single: CurrentIterationNumber

CurrentIterationNumber
  *List of integers*. Each element is the iteration index at the current step
  during the iterative algorithm procedure. There is one iteration index value
  per assimilation step corresponding to an observed state.

  Example:
  ``cin = ADD.get("CurrentIterationNumber")[-1]``
