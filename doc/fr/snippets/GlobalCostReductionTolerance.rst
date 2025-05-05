.. index:: single: GlobalCostReductionTolerance

GlobalCostReductionTolerance
  *Valeur réelle*. Cette clé indique le facteur de réduction limite, conduisant
  à arrêter le processus itératif d'optimisation lorsque la fonction coût
  décroît au moins de cette tolérance sur l'ensemble de la recherche optimale.
  La valeur par défaut est de 1.e-16 (ce qui équivaut à une absence d'effet),
  et il est recommandé de l'adapter aux besoins pour des problèmes réels.

  Exemple :
  ``{"GlobalCostReductionTolerance":1.e-16}``
