.. index:: single: BoxBounds

BoxBounds
  *Liste de paires de valeurs réelles*. Cette clé permet de définir des bornes
  supérieure et inférieure pour chaque incrément de  variable d'état optimisée
  (et non pas chaque variable d'état elle-même). Les bornes doivent être
  données par une liste de liste de paires de bornes inférieure/supérieure pour
  chaque incrément de variable, avec une valeur extrême chaque fois qu'il n'y a
  pas de borne (``None`` n'est pas une valeur autorisée lorsqu'il n'y a pas de
  borne). Cette clé est requise et il n'y a pas de valeurs par défaut.

  Exemple :
  ``{"BoxBounds":[[-0.5,0.5], [0.01,2.], [0.,1.e99], [-1.e99,1.e99]]}``
