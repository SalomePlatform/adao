.. index:: single: CurrentStepNumber

CurrentStepNumber
  *Liste d'entiers*. Chaque élément est l'index du pas courant au cours du
  déroulement itératif, piloté par la série des observations, de l'algorithme
  utilisé. Remarque : ce n'est pas l'index d'itération courant d'algorithme
  même si cela coïncide pour des algorithmes non itératifs.

  Exemple :
  ``i = ADD.get("CurrentStepNumber")[-1]``
