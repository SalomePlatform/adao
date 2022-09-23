.. index:: single: MaximumNumberOfLocations

MaximumNumberOfLocations
  *Valeur entière*. Cette clé indique le nombre maximum possible de positions
  trouvée dans la recherche optimale. La valeur par défaut est 1. La recherche
  optimale peut éventuellement trouver moins de positions que ce qui est requis
  par cette clé, comme par exemple dans le cas où le résidu associé à
  l'approximation est inférieur au critère et conduit à l'arrêt anticipé de la
  recherche optimale.

  Exemple :
  ``{"MaximumNumberOfLocations":5}``
