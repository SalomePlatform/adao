.. index:: single: AmplitudeOfInitialDirection

AmplitudeOfInitialDirection
  *Valeur réelle*. Cette clé indique la mise à l'échelle de la perturbation
  initiale construite comme un vecteur utilisé pour la dérivée directionnelle
  autour du point nominal de vérification. La valeur par défaut est de 1, ce
  qui signifie qu'il n'y a aucune mise à l'échelle. Il est utile de modifier
  cette valeur, et en particulier de la diminuer dans le cas où les
  perturbations les plus grandes sortent du domaine de définition de la
  fonction.

  Exemple :
  ``{"AmplitudeOfInitialDirection":0.5}``
