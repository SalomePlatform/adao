.. index:: single: APosterioriCorrelations

APosterioriCorrelations
  *Liste de matrices*. Chaque élément est une matrice de corrélations des
  erreurs *a posteriori* de l'état optimal, issue de la matrice
  :math:`\mathbf{A}` des covariances. Pour en disposer, il faut avoir en même
  temps demandé le calcul supplémentaire de ces covariances d'erreurs *a
  posteriori* identifié par le mot-clé "APosterioriCovariance".

  Exemple :
  ``apc = ADD.get("APosterioriCorrelations")[-1]``
