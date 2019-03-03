.. index:: single: JacobianMatrixAtOptimum

JacobianMatrixAtOptimum
  *Liste de matrices*. Chaque élément est une matrice jacobienne de dérivées
  partielles de la sortie de l'opérateur d'observation par rapport aux
  paramètres d'entrée, une colonne de dérivées par paramètre. Le calcul est
  effectué à l'état optimal.

  Exemple:
  ``GradH = ADD.get("JacobianMatrixAtOptimum")[-1]``
