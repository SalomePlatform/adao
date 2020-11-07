.. index:: single: MaximumNumberOfFunctionEvaluations

MaximumNumberOfFunctionEvaluations
  *Valeur entière*. Cette clé indique le nombre maximum d'évaluations possibles
  de la fonctionnelle à optimiser. Le défaut est de 15000, qui est une limite
  arbitraire. Il est ainsi recommandé d'adapter ce paramètre aux besoins pour
  des problèmes réels. Pour certains optimiseurs, le nombre effectif
  d'évaluations à l'arrêt peut être légèrement différent de la limite à cause
  d'exigences de déroulement interne de l'algorithme.

  Exemple :
  ``{"MaximumNumberOfFunctionEvaluations":50}``
