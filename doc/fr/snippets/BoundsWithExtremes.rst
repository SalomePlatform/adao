.. index:: single: Bounds

Bounds
  *Liste de paires de valeurs réelles*. Cette clé permet de définir des paires
  de bornes supérieure et inférieure pour chaque variable d'état optimisée. Les
  bornes doivent être données par une liste de liste de paires de bornes
  inférieure/supérieure pour chaque variable, avec une valeur extrême chaque
  fois qu'il n'y a pas de borne (``None`` n'est pas une valeur autorisée
  lorsqu'il n'y a pas de borne).

  Exemple :
  ``{"Bounds":[[2.,5.],[1.e-2,10.],[-30.,1.e99],[-1.e99,1.e99]]}``
