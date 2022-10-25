.. index::
    single: Variant
    pair: Variant ; PositioningByEIM
    pair: Variant ; PositioningBylcEIM

Variant
  *Nom prédéfini*. Cette clé permet de choisir l'une des variantes possibles
  pour la recherche du positionnement optimal. La variante par défaut est la
  version contrainte par des positions exclues "PositioningBylcEIM", et les
  choix possibles sont
  "PositioningByEIM" (utilisant l'algorithme EIM original),
  "PositioningBylcEIM" (utilisant l'algorithme EIM contraint par des positions exclues, nommé "Location Constrained EIM").
  Il est fortement recommandé de conserver la valeur par défaut.

  Exemple :
  ``{"Variant":"PositioningBylcEIM"}``
