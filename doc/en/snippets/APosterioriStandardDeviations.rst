.. index:: single: APosterioriStandardDeviations

APosterioriStandardDeviations
  *List of matrices*. Each element is an *a posteriori* error standard errors
  diagonal matrix of the optimal state, coming from the :math:`\mathbf{A}`
  covariance matrix. In order to get them, this *a posteriori* error
  covariances calculation has to be requested at the same time.

  Example:
  ``S = ADD.get("APosterioriStandardDeviations")[-1]``
