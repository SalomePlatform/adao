.. index:: single: InflationType

InflationType
  *Nom prédéfini*. Cette clé permet d'indiquer la méthode d'inflation dans les
  méthodes d'ensemble, pour celles qui nécessitent une telle technique.
  L'inflation peut être appliquée de diverses manières, selon les options
  suivantes : multiplicative ou additive du facteur d'inflation spécifié,
  appliquée sur l'ébauche ou sur l'analyse, appliquée sur les covariances ou
  sur les anomalies. Un seul type d'inflation est appliqué à la fois, et la
  valeur par défaut est "MultiplicativeOnAnalysisAnomalies". Les noms possibles
  sont dans la liste suivante : [
  "MultiplicativeOnAnalysisAnomalies",
  "MultiplicativeOnBackgroundAnomalies",
  ].

  Exemple :
  ``{"InflationType":"MultiplicativeOnAnalysisAnomalies"}``
