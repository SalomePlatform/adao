.. index:: single: EnsembleOfStates

EnsembleOfStates
  *Liste de vecteurs ou matrice*. Chaque élément est une collection ordonnée de
  vecteurs d'état physique ou d'état paramétrique :math:`\mathbf{x}`, avec 1
  état par colonne si c'est une matrice, ou 1 état par élément si c'est une
  liste. Important : la numérotation du support ou des points, sur lequel ou
  auxquels sont fournis une valeur d'état dans chaque vecteur, est
  implicitement celle de l'ordre naturel de numérotation du vecteur d'état, de
  0 à la "taille moins 1" de ce vecteur.

  Exemple :
  ``{"EnsembleOfStates":[x1, x2, x3...]}``
