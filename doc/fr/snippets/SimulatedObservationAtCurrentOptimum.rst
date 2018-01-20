.. index:: single: SimulatedObservationAtCurrentOptimum

SimulatedObservationAtCurrentOptimum
  *Liste de vecteurs*. Chaque élément est un vecteur d'observation simulé par
  l'opérateur d'observation à partir de l'état optimal au pas de temps courant
  au cours du déroulement de l'algorithme d'optimisation, c'est-à-dire dans
  l'espace des observations.

  Exemple :
  ``hxo = ADD.get("SimulatedObservationAtCurrentOptimum")[-1]``
