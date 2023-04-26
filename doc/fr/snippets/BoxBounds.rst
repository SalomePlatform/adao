.. index:: single: BoxBounds

BoxBounds
  *Liste de paires de valeurs réelles*. Cette clé permet de définir des paires
  de bornes supérieure et inférieure pour chaque *incrément* de variable d'état
  optimisée (et non pas chaque variable d'état elle-même, dont les bornes
  peuvent être indiquées par la variable "*Bounds*"). Les bornes d'incréments
  doivent être données par une liste de liste de paires de bornes
  inférieure/supérieure pour chaque incrément de variable, avec une valeur
  ``None`` chaque fois qu'il n'y a pas de borne. Cette clé est requise
  uniquement s'il n'y a pas de bornes de paramètres, et il n'y a pas de valeurs
  par défaut.

  Exemple :
  ``{"BoxBounds":[[-0.5,0.5], [0.01,2.], [0.,None], [None,None]]}``
