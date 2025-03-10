.. index:: single: EnsembleOfStates

EnsembleOfStates
  *Liste de vecteurs ou matrice*. Chaque élément est une collection ordonnée de
  vecteurs d'état physique ou d'état paramétrique :math:`\mathbf{x}`. Ce sont
  des **entrées** d'opérateur :math:`H`, c'est-à-dire des états courants avant
  observation. A chaque index de pas, il y a 1 état par colonne si cette liste
  est sous forme matricielle, ou 1 état par élément si c'est effectivement une
  liste. Important : la numérotation du support ou des points, sur lequel ou
  auxquels sont fournis une valeur d'état dans chaque vecteur, est
  implicitement celle de l'ordre naturel de numérotation du vecteur d'état, de
  0 à la "taille moins 1" de ce vecteur.

  Exemple :
  ``{"EnsembleOfStates":[x1, x2, x3...]}``
