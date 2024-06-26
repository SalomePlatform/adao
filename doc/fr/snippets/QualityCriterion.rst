.. index:: single: QualityCriterion

QualityCriterion
  *Nom prédéfini*. Cette clé indique le critère de qualité, qui est minimisé
  pour trouver l'estimation optimale de l'état. Le défaut est le critère usuel
  de l'assimilation de données nommé "DA", qui est le critère de moindres
  carrés pondérés augmentés. Le critère possible est dans la liste suivante,
  dans laquelle les noms équivalents sont indiqués par un signe "<=>" :
  ["AugmentedWeightedLeastSquares" <=> "AWLS" <=> "DA",
  "WeightedLeastSquares" <=> "WLS",
  "LeastSquares" <=> "LS" <=> "L2",
  "AbsoluteValue" <=> "L1",
  "MaximumError" <=> "ME" <=> "Linf"].
  On pourra se reporter à la section pour :ref:`section_theory_optimization`
  afin de disposer de la définition détaillée de ces critères de qualité.

  Exemple :
  ``{"QualityCriterion":"DA"}``
