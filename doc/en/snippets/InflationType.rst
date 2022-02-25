.. index:: single: InflationType

InflationType
  *Predefined name*. This key is used to set the inflation method in ensemble
  methods, for those that require such a technique. Inflation can be applied in
  various ways, according to the following options: multiplicative or additive
  by the specified inflation factor, applied on the background or on the
  analysis, applied on covariances or on anomalies. The *multiplicative
  inflation on anomalies*, that are obtained by subtracting the ensemble mean,
  is elaborated by multiplying these anomalies by the inflation factor, then by
  rebuilding the ensemble members by adding the previously evaluated mean. Only
  one type of inflation is applied at the same time, and the default value is
  "MultiplicativeOnAnalysisAnomalies". The possible names are in the following
  list: [
  "MultiplicativeOnAnalysisAnomalies",
  "MultiplicativeOnBackgroundAnomalies",
  ].

  Example :
  ``{"InflationType":"MultiplicativeOnAnalysisAnomalies"}``
