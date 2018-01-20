.. index:: single: APosterioriStandardDeviations

APosterioriStandardDeviations
  *Liste de matrices*. Chaque élément est une matrice diagonale d'écarts-types
  des erreurs *a posteriori* de l'état optimal, issue de la matrice
  :math:`\mathbf{A}` des covariances.

  Exemple :
  ``S = ADD.get("APosterioriStandardDeviations")[-1]``
