.. index:: single: CostFunctionJoAtCurrentOptimum

CostFunctionJoAtCurrentOptimum
  *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
  :math:`J^o`, c'est-à-dire de la partie écart à l'observation. A chaque pas,
  la valeur correspond à l'état optimal trouvé depuis le début.

  Exemple :
  ``JoACO = ADD.get("CostFunctionJoAtCurrentOptimum")[:]``
