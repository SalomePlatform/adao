.. index:: single: SampleAsIndependentRandomVariables

SampleAsIndependentRandomVariables
  *Liste de triplets [Nom, Paramètres, Nombre]*. Cette clé décrit les points de
  calcul sous la forme d'un hyper-cube, dont les points sur chaque axe
  proviennent de l'échantillonnage aléatoire indépendant de la variable d'axe,
  selon la spécification de la distribution, de ses paramètres et du nombre de
  points de l'échantillon, sous la forme d'une liste *[Nom, Paramètres,
  Nombre]* pour chaque axe. Contrairement à l'échantillonnage décrit par le
  mot-clé "*SampleAsIndependentRandomVectors*" , les points sont explicitement
  répartis sur un hypercube régulier. Les noms de distributions possibles sont
  'normal' de paramètres (mean,std), 'lognormal' de paramètres (mean,sigma),
  'uniform' de paramètres (low,high), 'loguniform' de paramètres (low,high), ou
  'weibull' de paramètre (shape). C'est donc une liste de la même taille que
  celle de l'état. Par nature, les points sont inclus dans le domaine non borné
  ou borné selon les caractéristiques des distributions choisies par variable.
  Les distributions peuvent être différentes pour chaque axe.

  Exemple :
  ``{"SampleAsIndependentRandomVariables":[['normal',[0.,1.],3], ['uniform',[-2,2],4]]}`` pour un espace d'état de dimension 2.
