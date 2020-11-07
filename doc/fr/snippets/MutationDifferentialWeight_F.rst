.. index:: single: MutationDifferentialWeight_F

MutationDifferentialWeight_F
  *Paire de valeurs réelles*. Cette clé permet de définir le poids différentiel
  dans l'étape de mutation. Cette variable est usuellement notée ``F`` dans la
  littérature. Il peut être constant s'il est sous la forme d'une valeur
  unique, ou variable de manière aléatoire dans les deux bornes données dans la
  paire. La valeur par défaut est (0.5, 1).

  Exemple :
  ``{"MutationDifferentialWeight_F":(0.5, 1)}``
