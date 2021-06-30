.. index:: single: ForecastCovariance

ForecastCovariance
  *Liste of matrices*. Each element is a forecast state error covariance
  matrix predicted by the model during the time iteration of the algorithm
  used.

  Example :
  ``Pf = ADD.get("ForecastCovariance")[-1]``
