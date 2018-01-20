.. index:: single: InitialDirection

InitialDirection
  Cette clé indique la direction vectorielle utilisée pour la dérivée
  directionnelle autour du point nominal de vérification. Cela doit être un
  vecteur. Si elle n'est pas spécifiée, la direction par défaut est une
  perturbation par défaut autour de zéro de la même taille vectorielle que le
  point de vérification.

  Exemple :
  ``{"InitialDirection":[0.1,0.1,100.,3}``
