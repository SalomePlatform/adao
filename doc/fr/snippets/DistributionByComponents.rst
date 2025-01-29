.. index:: single: DistributionByComponents

SwarmInitialization
  *Liste de noms prédéfinis*. Ce mot-clé n'a besoin d'être défini que lorsque
  l'initialisation de l'essaim de particules pour l'algorithme
  "*ParticleSwarmOptimization*" est fixée à "DistributionByComponents". Dans ce
  cas, il faut indiquer, pour chaque composante de l'état, la distribution
  choisie sous la forme d'un nom prédéfini. Les noms possibles sont 'uniform'
  et 'loguniform' et les distributions utilisent les bornes indiquées pour
  l'algorithme "*ParticleSwarmOptimization*". Les distributions peuvent être
  différentes pour chaque axe.

  Exemple :
  ``{"DistributionByComponents":['loguniform', 'uniform', 'loguniform']}`` pour un espace d'état de dimension 3.
