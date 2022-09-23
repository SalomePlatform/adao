.. index:: single: ExcludeLocations

ExcludeLocations
  *Liste d'entiers*. Cette clé indique la liste des points du vecteur d'état
  exclus de la recherche optimale. La valeur par défaut est une liste vide.
  Important : la numérotation de ces points exclus doit être identique à celle
  qui est adoptée implicitement dans les états fournis par la clé
  "*EnsembleOfSnapshots*".

  Exemple :
  ``{"ExcludeLocations":[3, 125, 286]}``
