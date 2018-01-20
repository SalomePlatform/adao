.. index:: single: APosterioriVariances

APosterioriVariances
  *List of matrices*. Each element is an *a posteriori* error variance
  errors diagonal matrix of the optimal state, coming from the
  :math:`\mathbf{A}*` covariance matrix.

  Example :
  ``V = ADD.get("APosterioriVariances")[-1]``
