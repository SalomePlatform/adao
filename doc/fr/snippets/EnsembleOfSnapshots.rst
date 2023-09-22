.. index:: single: EnsembleOfSnapshots

EnsembleOfSnapshots
  *Liste de vecteurs ou matrice*. Cette clé contient une collection ordonnée de
  vecteurs d'état physique :math:`\mathbf{y}` (nommés "*snapshots*" en
  terminologie de bases réduites), avec un état complet par colonne si c'est
  une matrice, ou un état complet par élément si c'est une liste. Important :
  la numérotation du support ou des points, sur lequel ou auxquels sont fournis
  une valeur d'état dans chaque vecteur, est implicitement celle de l'ordre
  naturel de numérotation du vecteur d'état, de 0 à la "taille moins 1" de ce
  vecteur.

  Exemple :
  ``{"EnsembleOfSnapshots":[y1, y2, y3...]}``
