.. index:: single: DistributionByComponents

DistributionByComponents
  *Liste de noms prédéfinis*. Ce mot-clé n'a besoin d'être défini que lorsque
  l'initialisation de l'essaim de particules pour l'algorithme
  "*ParticleSwarmOptimization*" est fixée à "DistributionByComponents". Dans ce
  cas, il faut indiquer, pour chaque composante de l'état, la distribution
  choisie sous la forme d'un nom prédéfini. Les noms possibles sont "uniform",
  "loguniform", "logarithmic", "['normal',σ]", "['lognormal',σ]" et
  "['logarithmicnormal',σ]". Toutes les distributions "*normal" doivent être
  accompagnées d'une indication d'écart-type σ, sachant qu'elles sont centrées
  dans le domaine de définition. Les valeurs "uniform", "loguniform", "normal",
  "lognormal" n'agissent que sur l'initialisation de la position en appliquant
  la distribution indiquée, les valeurs "logarithmic" et "logarithmicnormal"
  agissent à la fois sur l'initialisation de la position et celle du mouvement.
  Il doit y en avoir le même nombre de valeurs indiquées que la taille d'un
  état individuel. Les distributions se conforment aux bornes indiquées pour
  l'algorithme "*ParticleSwarmOptimization*". Les distributions peuvent être
  différentes pour chaque axe. Lorsque l'on choisi une distribution identique
  pour toutes les composantes, cela équivaut à choisir à la place la valeur
  globale du mot-clé précédent s'il existe.

  Exemple :
  ``{"DistributionByComponents" : ['uniform', 'loguniform', 'logarithmic', ['normal', 1]]}`` pour un espace d'état de dimension 4.
