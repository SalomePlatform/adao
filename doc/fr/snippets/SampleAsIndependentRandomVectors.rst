.. index:: single: SampleAsIndependentRandomVectors

SampleAsIndependentRandomVectors
  *Liste de paires [Nom, Paramètres], plus [Dimension, Nombre]*. Cette clé
  décrit les points de calcul sous la forme de distributions particulières
  définies pour chaque dimension, qui permettent d'obtenir des vecteurs
  aléatoires dont chaque composante suit la distribution requise. Contrairement
  à l'échantillonnage décrit par le mot-clé
  "*SampleAsIndependentRandomVariables*" , les points ne sont pas répartis sur
  un hypercube régulier. La distribution sur chaque variable d'axe et spécifiée
  par non nom et ses paramètres, sous la forme d'une liste *[Nom, Paramètres]*
  pour chaque axe. Cette liste de paires, en nombre identique à la taille de
  l'espace des états, est complétée par une paire d'entiers
  *[Dimension, Nombre]* comportant la dimension de l'espace des états et le
  nombre souhaité de points d'échantillonnage. Les noms de distributions
  possibles sont 'normal' de paramètres (mean,std), 'lognormal' de paramètres
  (mean,sigma), 'uniform' de paramètres (low,high), 'loguniform' de paramètres
  (low,high), ou 'weibull' de paramètre (shape). Par nature, les points sont
  inclus dans le domaine non borné ou borné selon les caractéristiques des
  distributions choisies par variable. Les distributions peuvent être
  différentes pour chaque axe.

  Exemple :
  ``{"SampleAsIndependentRandomVectors":[['normal',[0.,1.]], ['uniform',[-2,2]]]}`` pour un espace d'état de dimension 2.
