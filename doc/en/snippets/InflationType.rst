.. index:: single: InflationType

InflationType
  *Predefined name*. This key is used to set the inflation method in ensemble
  methods, for those that require such a technique. Inflation can be applied in
  various ways, according to the following options: multiplicative or additive
  by the specified inflation factor, applied on the background or on the
  analysis, applied on covariances or on anomalies. Only one type of inflation
  is applied at the same time, and the default value is
  "MultiplicativeOnAnalysisAnomalies". The possible names are in the following
  list: [
  "MultiplicativeOnAnalysisAnomalies",
  "MultiplicativeOnBackgroundAnomalies",
  ].

  Example :
  ``{"InflationType":"MultiplicativeOnAnalysisAnomalies"}``
