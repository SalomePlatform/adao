.. index:: single: InflationFactor

InflationFactor
  *Real value*. This key specifies the inflation factor in the ensemble
  methods, to be applied on the covariance or the anomalies depending on the
  choice of the type of inflation. Its value must be positive if the inflation
  is additive, or greater than 1 if the inflation is multiplicative. The
  default value is 1, which leads to an absence of multiplicative inflation.
  The absence of additive inflation is obtained by entering a value of 0.

  Example :
  ``{"InflationFactor":1.}``
