.. index:: single: SimulationQuantiles

SimulationQuantiles
  *Liste de séries de vecteurs*. Chaque élément est une série de vecteurs
  colonnes d'observation, correspondant, pour un quantile particulier requis
  par l'utilisateur, à l'état observé qui réalise le quantile demandé. Chaque
  vecteur colonne d'observation est restitué dans le même ordre que les valeurs
  de quantiles requis par l'utilisateur.

  Exemple :
  ``sQuantiles = ADD.get("SimulationQuantiles")[:]``
