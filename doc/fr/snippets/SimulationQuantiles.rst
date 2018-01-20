.. index:: single: SimulationQuantiles

SimulationQuantiles
  *Liste de vecteurs*. Chaque élément est un vecteur correspondant à l'état
  observé qui réalise le quantile demandé, dans le même ordre que les valeurs
  de quantiles requis par l'utilisateur.

  Exemple :
  ``sQuantiles = ADD.get("SimulationQuantiles")[:]``
