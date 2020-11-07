.. index:: single: Quantiles

Quantiles
  *List of real values*. This list indicates the values of quantile, between 0
  and 1, to be estimated by simulation around the optimal state. The sampling
  uses a multivariate Gaussian random sampling, directed by the *a posteriori*
  covariance matrix. This option is useful only if the supplementary
  calculation "SimulationQuantiles" has been chosen. The default is a void
  list.

  Example:
  ``{"Quantiles":[0.1,0.9]}``
