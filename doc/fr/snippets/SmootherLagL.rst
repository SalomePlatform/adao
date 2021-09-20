.. index:: single: SmootherLagL

SmootherLagL
  *Valeur entière*. Cette clé indique le nombre d'intervalles de temps de
  lissage dans le passé pour l'EnKS. C'est bien un nombre d'intervalles, et non
  pas une durée fixe. La valeur par défaut est 0, qui conduit à une absence de
  lissage.

  Exemple :
  ``{"SmootherLagL":0}``
