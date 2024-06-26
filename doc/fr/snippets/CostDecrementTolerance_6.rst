.. index:: single: CostDecrementTolerance

CostDecrementTolerance
  *Valeur réelle*. Cette clé indique une valeur limite, conduisant à arrêter le
  processus itératif d'optimisation lorsque la fonction coût décroît moins que
  cette tolérance au dernier pas. Le défaut est de 1.e-6, et il est recommandé
  de l'adapter aux besoins pour des problèmes réels. On peut se reporter à la
  partie décrivant les manières de
  :ref:`subsection_iterative_convergence_control` pour des recommandations plus
  détaillées.

  Exemple :
  ``{"CostDecrementTolerance":1.e-6}``
