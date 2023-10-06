.. index:: single: CurrentOptimum

CurrentOptimum
  *Liste de vecteurs*. Chaque élément est le vecteur d'état optimal au pas de
  temps courant au cours du déroulement itératif de l'algorithme d'optimisation
  utilisé. Ce n'est pas nécessairement le dernier état.

  Exemple :
  ``xo = ADD.get("CurrentOptimum")[:]``
