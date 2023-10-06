.. index:: single: APosterioriVariances

APosterioriVariances
  *Liste de matrices*. Chaque élément est une matrice diagonale de variances
  des erreurs *a posteriori* de l'état optimal, issue de la matrice
  :math:`\mathbf{A}` des covariances. Pour en disposer, il faut avoir en même
  temps demandé le calcul de ces covariances d'erreurs *a posteriori*.

  Exemple :
  ``apv = ADD.get("APosterioriVariances")[-1]``
