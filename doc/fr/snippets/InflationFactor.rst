.. index:: single: InflationFactor

InflationFactor
  *Valeur réelle*. Cette clé indique le facteur d'inflation dans les méthodes
  d'ensemble, à appliquer sur la covariance ou les anomalies selon le choix du
  type d'inflation. Sa valeur doit être positive si l'inflation est additive,
  ou supérieure à 1 si l'inflation est multiplicative. La valeur par défaut est
  1, qui conduit à une absence d'inflation multiplicative. L'absence
  d'inflation additive est obtenue en indiquant une valeur de 0.

  Exemple :
  ``{"InflationFactor":1.}``
