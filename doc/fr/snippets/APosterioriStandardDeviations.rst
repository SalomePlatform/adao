.. index:: single: APosterioriStandardDeviations

APosterioriStandardDeviations
  *Liste de matrices*. Chaque élément est une matrice diagonale d'écarts-types
  des erreurs *a posteriori* de l'état optimal, issue de la matrice
  :math:`\mathbf{A}` des covariances. Pour en disposer, il faut avoir en même
  temps demandé le calcul de ces covariances d'erreurs *a posteriori*.

  Exemple :
  ``aps = ADD.get("APosterioriStandardDeviations")[-1]``
