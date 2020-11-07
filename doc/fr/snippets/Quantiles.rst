.. index:: single: Quantiles

Quantiles
  *Liste de valeurs réelles*. Cette liste indique les valeurs de quantile,
  entre 0 et 1, à estimer par simulation autour de l'état optimal.
  L'échantillonnage utilise des tirages aléatoires gaussiens multivariés,
  dirigés par la matrice de covariance a posteriori. Cette option n'est utile
  que si le calcul supplémentaire "SimulationQuantiles" a été choisi. La valeur
  par défaut est une liste vide.

  Exemple :
  ``{"Quantiles":[0.1,0.9]}``
