.. index:: single: AmplitudeOfTangentPerturbation

AmplitudeOfTangentPerturbation
  *Valeur réelle*. Cette clé indique l'amplitude numérique relative de la
  perturbation utilisée pour estimer la valeur tangente de l'opérateur au point
  d'évaluation, i.e. sa dérivée directionnelle. Le défaut conservatif est de
  1.e-2 i.e. 1%, et il est fortement recommandé de l'adapter aux besoins pour
  des problèmes réels, en diminuant sa valeur de plusieurs ordres de grandeur.

  Exemple :
  ``{"AmplitudeOfTangentPerturbation":1.e-2}``
