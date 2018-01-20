.. index:: single: CostFunctionJbAtCurrentOptimum

CostFunctionJbAtCurrentOptimum
  *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
  :math:`J^b`, c'est-à-dire de la partie écart à l'ébauche. A chaque pas, la
  valeur correspond à l'état optimal trouvé depuis le début. Si cette partie
  n'existe pas dans la fonctionnelle, sa valeur est nulle.

  Exemple :
  ``JbACO = ADD.get("CostFunctionJbAtCurrentOptimum")[:]``
