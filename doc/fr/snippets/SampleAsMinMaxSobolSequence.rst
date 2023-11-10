.. index:: single: SampleAsMinMaxSobolSequence
.. index:: single: Sobol Sequence
.. index:: single: Séquence de Sobol

SampleAsMinMaxSobolSequence
  *Liste de triplets de paires réelles*. Cette clé décrit le domaine borné dans
  lequel les points de calcul seront placés, sous la forme d'une paire
  *[min,max]* pour chaque composante de l'état. Les bornes inférieures sont
  incluses. Cette liste de paires, en nombre identique à la taille de l'espace
  des états, est complétée par une paire d'entier *[dim,nbr]* comportant la
  dimension de l'espace des états et le nombre minimum souhaité de points
  d'échantillonnage (par construction, le nombre de points générés dans la
  séquence de Sobol sera la puissance de 2 immédiatement supérieure à ce nombre
  minimum). L'échantillonnage est ensuite construit automatiquement selon la
  méthode de séquences de Sobol.

  Exemple :
  ``{"SampleAsMinMaxSobolSequence":[[0.,1.],[-1,3]]+[[2,11]]}`` pour un espace d'état de dimension 2 et au moins 11 points d'échantillonnage (il y aura 16 points en pratique).
