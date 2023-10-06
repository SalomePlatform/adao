.. index:: single: KalmanGainAtOptimum

KalmanGainAtOptimum
  *Liste de matrices*. Chaque élément est une matrice de gain de Kalman
  standard, évaluée à l'aide de l'opérateur d'observation linéarisé. Le calcul
  est effectué à l'état optimal.

  Exemple:
  ``kg = ADD.get("KalmanGainAtOptimum")[-1]``
