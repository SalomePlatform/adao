.. index:: single: APosterioriCorrelations

APosterioriCorrelations
  *Liste de matrices*. Chaque élément est une matrice de corrélations des
  erreurs *a posteriori* de l'état optimal, issue de la matrice
  :math:`\mathbf{A}` des covariances.

  Exemple :
  ``C = ADD.get("APosterioriCorrelations")[-1]``
