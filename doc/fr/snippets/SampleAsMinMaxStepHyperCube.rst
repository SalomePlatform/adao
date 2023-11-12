.. index:: single: SampleAsMinMaxStepHyperCube

SampleAsMinMaxStepHyperCube
  *Liste de triplets de valeurs réelles*. Cette clé décrit les points de calcul
  sous la forme d'un hyper-cube, dont on donne la liste des échantillonnages
  implicites de chaque variable par un triplet *[min,max,step]*. C'est donc une
  liste de la même taille que celle de l'état. Les bornes sont incluses. Par
  nature, les points sont inclus dans le domaine défini par les bornes
  explicites.

  Exemple :
  ``{"SampleAsMinMaxStepHyperCube":[[0.,1.,0.25],[-1,3,1]]}`` pour un espace d'état de dimension 2.
