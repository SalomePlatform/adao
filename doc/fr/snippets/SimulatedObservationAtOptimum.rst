.. index:: single: SimulatedObservationAtOptimum
.. index:: single: Forecast

SimulatedObservationAtOptimum
  *Liste de vecteurs*. Chaque élément est un vecteur d'observation obtenu par
  l'opérateur d'observation à partir de la simulation d'analyse ou d'état
  optimal :math:`\mathbf{x}^a`. C'est l'observation de la prévision à partir de
  l'analyse ou de l'état optimal, et elle est parfois appelée "*Forecast*".

  Exemple :
  ``hxa = ADD.get("SimulatedObservationAtOptimum")[-1]``
