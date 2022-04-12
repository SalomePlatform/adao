.. index:: single: MaximumNumberOfIterations

MaximumNumberOfIterations
  *Valeur entière*. Cette clé indique le nombre maximum d'itérations internes
  possibles en optimisation itérative. Le défaut est 15000, qui est très
  similaire à une absence de limite sur les itérations. Il est ainsi recommandé
  d'adapter ce paramètre aux besoins pour des problèmes réels. Pour certains
  optimiseurs, le nombre de pas effectif d'arrêt peut être légèrement différent
  de la limite à cause d'exigences de contrôle interne de l'algorithme. On peut
  se reporter à la partie décrivant les manières de
  :ref:`subsection_iterative_convergence_control` pour des recommandations plus
  détaillées.

  Exemple :
  ``{"MaximumNumberOfIterations":100}``
