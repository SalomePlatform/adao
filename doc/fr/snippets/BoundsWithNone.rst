.. index:: single: Bounds

Bounds
  *Liste de paires de valeurs réelles*. Cette clé permet de définir des paires
  de bornes supérieure et inférieure pour chaque variable d'état optimisée. Les
  bornes doivent être données par une liste de liste de paires de bornes
  inférieure/supérieure pour chaque variable, avec une valeur ``None`` chaque
  fois qu'il n'y a pas de borne. Les bornes peuvent toujours être spécifiées,
  mais seuls les optimiseurs sous contraintes les prennent en compte. Si la
  liste est vide, cela équivaut à une absence de bornes.

  Exemple :
  ``{"Bounds":[[2.,5.],[1.e-2,10.],[-30.,None],[None,None]]}``
