.. index:: single: SampleAsMinMaxLatinHyperCube
.. index:: single: Latin hypercube
.. index:: single: Hypercube Latin

SampleAsMinMaxLatinHyperCube
  *Liste de paires réelles [Min, Max], plus [Dimension, Nombre]*. Cette clé
  décrit le domaine borné dans lequel les points de calcul seront placés, sous
  la forme d'une paire *[Min, Max]* pour chaque composante de l'état. Les
  bornes inférieures sont incluses. Cette liste de paires, en nombre identique
  à la taille de l'espace des états, est complétée par une paire d'entiers
  *[Dimension, Nombre]* comportant la dimension de l'espace des états et le
  nombre souhaité de points d'échantillonnage. L'échantillonnage est ensuite
  construit automatiquement selon la méthode de l'hypercube Latin (LHS). Par
  nature, les points sont inclus dans le domaine défini par les bornes
  explicites.

  Exemple :
  ``{"SampleAsMinMaxLatinHyperCube":[[0.,1.],[-1,3]]+[[2,11]]}`` pour un espace d'état de dimension 2 et pour 11 points d'échantillonnage.
