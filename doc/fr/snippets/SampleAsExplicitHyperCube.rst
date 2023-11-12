.. index:: single: SampleAsExplicitHyperCube

SampleAsExplicitHyperCube
  *Liste de liste de valeurs réelles*. Cette clé décrit les points de calcul
  sous la forme d'un hyper-cube, dont on donne la liste des échantillonnages
  explicites de chaque variable comme une liste. C'est donc une liste de
  listes, chacune étant de taille potentiellement différente. Par nature, les
  points sont inclus dans le domaine défini par les bornes des listes
  explicites de chaque variable.

  Exemple : ``{"SampleAsExplicitHyperCube":[[0.,0.25,0.5,0.75,1.], [-2,2,1]]}`` pour un espace d'état de dimension 2.
