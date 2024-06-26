.. index:: single: InitializationPoint

InitializationPoint
  *Vecteur*. La variable désigne un vecteur à utiliser comme l'état initial
  autour duquel démarre un algorithme itératif. Par défaut, cet état initial
  n'a pas besoin d'être fourni et il est égal à l'ébauche :math:`\mathbf{x}^b`.
  Sa valeur doit permettre de construire un vecteur de taille identique à
  l'ébauche. Dans le cas où il est fourni, il ne remplace l'ébauche que pour
  l'initialisation.

  Exemple :
  ``{"InitializationPoint":[1, 2, 3, 4, 5]}``
