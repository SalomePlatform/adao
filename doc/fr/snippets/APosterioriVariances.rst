.. index:: single: APosterioriVariances

APosterioriVariances
  *Liste de matrices*. Chaque élément est une matrice diagonale de variances
  des erreurs *a posteriori* de l'état optimal, issue de la matrice
  :math:`\mathbf{A}` des covariances.

  Exemple :
  ``V = ADD.get("APosterioriVariances")[-1]``
