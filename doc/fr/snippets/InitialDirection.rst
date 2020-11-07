.. index:: single: InitialDirection

InitialDirection
  *Vecteur*. Cette clé indique la direction vectorielle utilisée pour la
  dérivée directionnelle autour du point nominal de vérification. Cela doit
  être un vecteur de la même taille que celle du point de vérification. Si elle
  n'est pas spécifiée, la direction par défaut est une perturbation vectorielle
  autour de zéro de la même taille que le point de vérification.

  Exemple :
  ``{"InitialDirection":[0.1,0.1,100.,3}`` pour un espace d'état de dimension 4
