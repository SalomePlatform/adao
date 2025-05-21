.. index::
    single: Variant
    pair: Variant ; GeneralizedSimulatedAnnealing
    pair: Variant ; DualAnnealing

Variant
  *Nom prédéfini*. Cette clé permet de choisir l'une des variantes possibles
  pour l'algorithme principal. La variante par défaut est la formulation
  "DualAnnealing" d'origine, et les choix possibles sont
  "GeneralizedSimulatedAnnealing" (Generalized Simulated Annealing ou GSA),
  "DualAnnealing" (Dual Annealing).

  Il est conseillé d'essayer la variante "DualAnnealing" avec un très faible
  nombre d'itérations et un nombre limité d'évaluations de la fonction de
  simulation.

  Exemple :
  ``{"Variant":"DualAnnealing"}``
