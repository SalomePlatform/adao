.. index:: single: SimulatedObservationAtOptimum
.. index:: single: Forecast

SimulatedObservationAtOptimum
  *Liste de vecteurs*. Chaque élément est un vecteur d'observation simulé par
  l'opérateur d'observation à partir de l'analyse ou de l'état optimal
  :math:`\mathbf{x}^a`. C'est la prévision à partir de l'analyse ou de l'état
  optimal, et elle est parfois appellée "*Forecast*".

  Exemple :
  ``hxa = ADD.get("SimulatedObservationAtOptimum")[-1]``
