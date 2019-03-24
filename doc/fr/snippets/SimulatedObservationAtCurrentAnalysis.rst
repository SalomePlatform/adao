.. index:: single: SimulatedObservationAtCurrentAnalysis

SimulatedObservationAtCurrentAnalysis
  *Liste de vecteurs*. Chaque élément est un vecteur d'observation simulé par
  l'opérateur d'observation à partir de l'état courant, c'est-à-dire dans
  l'espace des observations. Cette quantité est identique au vecteur
  d'observation simulé à l'état courant dans le cas d'une assimilation
  mono-état.

  Exemple :
  ``hxs = ADD.get("SimulatedObservationAtCurrentAnalysis")[-1]``
