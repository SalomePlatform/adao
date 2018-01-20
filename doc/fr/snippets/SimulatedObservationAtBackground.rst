.. index:: single: SimulatedObservationAtBackground
.. index:: single: Dry

SimulatedObservationAtBackground
  *Liste de vecteurs*. Chaque élément est un vecteur d'observation simulé par
  l'opérateur d'observation à partir de l'ébauche :math:`\mathbf{x}^b`. C'est
  la prévision à partir de l'ébauche, elle est parfois appellée "*Dry*".

  Exemple :
  ``hxb = ADD.get("SimulatedObservationAtBackground")[-1]``
