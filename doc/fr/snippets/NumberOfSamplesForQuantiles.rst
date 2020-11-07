.. index:: single: NumberOfSamplesForQuantiles

NumberOfSamplesForQuantiles
  *Valeur entière*. Cette clé indique le nombre de simulations effectuées pour
  estimer les quantiles. Cette option n'est utile que si le calcul
  supplémentaire "SimulationQuantiles" a été choisi. Le défaut est 100, ce qui
  suffit souvent pour une estimation correcte de quantiles courants à 5%, 10%,
  90% ou 95%.

  Exemple :
  ``{"NumberOfSamplesForQuantiles":100}``
