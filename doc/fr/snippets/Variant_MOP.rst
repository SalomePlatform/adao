.. index::
    single: Variant
    pair: Variant ; EIM
    pair: Variant ; DEIM
    pair: Variant ; lcEIM
    pair: Variant ; lcDEIM
    pair: Variant ; PositioningByEIM
    pair: Variant ; PositioningByDEIM
    pair: Variant ; PositioningBylcEIM
    pair: Variant ; PositioningBylcDEIM

Variant
  *Nom prédéfini*. Cette clé permet de choisir l'une des variantes possibles
  pour la recherche du positionnement optimal. La variante par défaut est la
  version contrainte par des positions exclues "lcEIM" ou "PositioningBylcEIM",
  et les choix possibles sont "EIM" ou "PositioningByEIM" (utilisant
  l'algorithme EIM original), "lcEIM" ou "PositioningBylcEIM" (utilisant
  l'algorithme EIM contraint par des positions exclues, nommé "Location
  Constrained EIM"), "DEIM" ou "PositioningByDEIM" (utilisant l'algorithme DEIM
  original), "lcDEIM" ou "PositioningBylcDEIM" (utilisant l'algorithme DEIM
  contraint par des positions exclues, nommé "Location Constrained DEIM"). Il
  est fortement recommandé de conserver la valeur par défaut.

  Exemple :
  ``{"Variant":"lcEIM"}``
