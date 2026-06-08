.. index:: single: APosterioriCorrelations

APosterioriCorrelations
  *List of matrices*. Each element is an *a posteriori* error correlations
  matrix of the optimal state, coming from the :math:`\mathbf{A}` covariance
  matrix. In order to get them, this *a posteriori* error covariances
  supplementary calculation has to be requested at the same time by the keyword
  "APosterioriCovariance".

  Example:
  ``apc = ADD.get("APosterioriCorrelations")[-1]``
