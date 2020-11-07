.. index:: single: PopulationSize

PopulationSize
  *Valeur entière*. Cette clé permet de définir la taille (approximative) de la
  population à chaque génération. Cette taille est légèrement ajustée pour
  tenir compte du nombre de variables d'état à optimiser. La valeur par défaut
  est 100. Il est conseillé de choisir une population comprise entre 1 et une
  dizaine de fois le nombre de variables d'états, la taille étant d'autant plus
  petite que le nombre de variables augmente.

  Exemple :
  ``{"PopulationSize":100}``
