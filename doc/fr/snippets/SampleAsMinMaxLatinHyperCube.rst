.. index:: single: SampleAsMinMaxLatinHyperCube

SampleAsMinMaxLatinHyperCube
  *Liste de triplets de paires réelles*. Cette clé décrit le domaine borné dans
  lequel les points de calcul seront placés, sous la forme d'une paire
  *[min,max]* pour chaque composante de l'état. Les bornes inférieures sont
  incluses. Cette liste de paires, en nombre identique à la taille de l'espace
  des états, est complétée par une paire d'entier *[dim,nb]* comportant la
  dimension de l'espace des états et le nombre souhaité de points
  d'échantillonnage. L'échantillonnage est ensuite construit automatiquement
  selon la méthode de l'hypercube Latin (LHS).

  Exemple :
  ``{"SampleAsMinMaxLatinHyperCube":[[0.,1.],[-1,3]]+[[2,11]]}`` pour un espace d'état de dimension 2 et 11 points d'échantillonnage.
