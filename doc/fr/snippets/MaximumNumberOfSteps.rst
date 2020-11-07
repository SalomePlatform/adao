.. index:: single: MaximumNumberOfSteps

MaximumNumberOfSteps
  *Valeur entière*. Cette clé indique le nombre maximum d'itérations possibles
  en optimisation itérative. Le défaut est 15000, qui est très similaire à une
  absence de limite sur les itérations. Il est ainsi recommandé d'adapter ce
  paramètre aux besoins pour des problèmes réels. Pour certains optimiseurs, le
  nombre de pas effectif d'arrêt peut être légèrement différent de la limite à
  cause d'exigences de contrôle interne de l'algorithme.

  Exemple :
  ``{"MaximumNumberOfSteps":100}``
