.. index:: single: ReduceMemoryUse

ReduceMemoryUse
  *Valeur booléenne*. La variable conduit à l'activation, ou pas, du mode de
  réduction de l'empreinte mémoire lors de l'exécution, au prix d'une
  augmentation potentielle du temps de calcul. Les résultats peuvent différer à
  partir d'une certaine précision (1.e-12 à 1.e-14) usuellement proche de la
  précision machine (1.e-16). La valeur par défaut est "False", les choix sont
  "True" ou "False".

  Exemple :
  ``{"ReduceMemoryUse":False}``
