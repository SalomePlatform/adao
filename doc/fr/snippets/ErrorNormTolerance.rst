.. index:: single: ErrorNormTolerance

ErrorNormTolerance
  *Valeur réelle*. Cette clé indique la valeur à partir laquelle le résidu
  associé à l'approximation est acceptable, ce qui conduit à arrêter la
  recherche optimale. La valeur par défaut est de 1.e-7 (ce qui équivaut
  usuellement à une quasi-absence de critère d'arrêt car l'approximation est
  moins précise), et il est recommandé de l'adapter aux besoins pour des
  problèmes réels. Une valeur habituelle, recommandée pour arrêter la recherche
  sur critère de résidu, est de 1.e-2.

  Exemple :
  ``{"ErrorNormTolerance":1.e-7}``
