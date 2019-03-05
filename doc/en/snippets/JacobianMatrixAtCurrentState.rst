.. index:: single: JacobianMatrixAtCurrentState

JacobianMatrixAtCurrentState
  *List of matrices*. Each element is the jacobian matrix of partial
  derivatives of the output of the observation operator with respect to the input
  parameters, one column of derivatives per parameter. It is calculated at the
  current state.

  Example:
  ``GradH = ADD.get("JacobianMatrixAtCurrentState")[-1]``
