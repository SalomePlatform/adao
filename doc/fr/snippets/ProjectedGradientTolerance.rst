.. index:: single: ProjectedGradientTolerance

ProjectedGradientTolerance
  *Valeur réelle*. Cette clé indique une valeur limite, conduisant à arrêter le processus
  itératif d'optimisation lorsque toutes les composantes du gradient projeté
  sont en-dessous de cette limite. C'est utilisé uniquement par les
  optimiseurs sous contraintes. Le défaut est -1, qui désigne le défaut
  interne de chaque optimiseur (usuellement 1.e-5), et il n'est pas recommandé
  de le changer.

  Exemple :
  ``{"ProjectedGradientTolerance":-1}``
