.. index:: single: StateBoundsForQuantiles

StateBoundsForQuantiles
  *Liste de paires de valeurs réelles*. Cette clé permet de définir des paires
  de bornes supérieure et inférieure pour chaque variable d'état utilisée dans
  la simulation des quantiles. Les bornes doivent être données par une liste de
  liste de paires de bornes inférieure/supérieure pour chaque variable, avec
  une valeur ``None`` chaque fois qu'il n'y a pas de borne.

  En l'absence de définition de ces bornes pour la simulation des quantiles et
  si des bornes d'optimisation sont définies, ce sont ces dernières qui sont
  utilisées pour la simulation des quantiles. Si ces bornes pour la simulation
  des quantiles sont définies, elles sont utilisées quelles que soient les
  bornes d'optimisation définies. Si cette variable est définie à ``None``,
  alors aucune borne n'est utilisée pour les états utilisés dans la simulation
  des quantiles quelles que soient les bornes d'optimisation définies.

  Exemple :
  ``{"StateBoundsForQuantiles":[[2.,5.],[1.e-2,10.],[-30.,None],[None,None]]}``
