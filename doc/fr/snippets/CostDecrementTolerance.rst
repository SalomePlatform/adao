.. index:: single: CostDecrementTolerance

CostDecrementTolerance
  *Valeur réelle*. Cette clé indique une valeur limite, conduisant à arrêter le
  processus itératif d'optimisation lorsque la fonction coût décroît moins que
  cette tolérance au dernier pas. Le défaut est de 1.e-7, et il est recommandé
  de l'adapter aux besoins pour des problèmes réels.

  Exemple :
  ``{"CostDecrementTolerance":1.e-7}``
