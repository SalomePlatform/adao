.. index:: single: EvolutionaryPopulationSize

EvolutionaryPopulationSize
  *Valeur entière*. Cette clé indique la taille de la population des états
  évalués à chaque étape lors du processus de recherche évolutionnaire CMA-ES.
  C'est une valeur entière. Dans le cas par défaut de valeur nulle, elle est
  automatiquement prise égale au défaut recommandé par la méthode théorique à
  :math:`4+3\log(dimension)`, où :math:`dimension` est celle de l'espace des
  états.

  Exemple :
  ``{"EvolutionaryPopulationSize":15}``

