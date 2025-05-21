.. index:: single: Dérivation potentiellement requise ou pas

- Les méthodes proposées par cet algorithme **peuvent requérir la dérivation de
  la fonction objectif ou de l'un des opérateurs**. Dans le cas où une
  dérivation est requise, cela nécessite que l'un au moins des opérateurs
  d'observation ou d'évolution soit différentiable voire les deux, et cela
  implique un temps de calcul supplémentaire dans le cas où les dérivées sont
  calculées numériquement par de multiples évaluations.
