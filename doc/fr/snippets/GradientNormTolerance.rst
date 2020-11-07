.. index:: single: GradientNormTolerance

GradientNormTolerance
  *Valeur réelle*. Cette clé indique une valeur limite, conduisant à arrêter le
  processus itératif d'optimisation lorsque la norme du gradient est en dessous
  de cette limite. C'est utilisé uniquement par les optimiseurs sans
  contraintes. Le défaut est 1.e-5 et il n'est pas recommandé de le changer.

  Exemple :
  ``{"GradientNormTolerance":1.e-5}``
