.. index:: single: ForecastCovariance

ForecastCovariance
  *Liste de matrices*. Chaque élément est une matrice de covariance d'erreur
  sur l'état prévu par le modèle au cours du déroulement itératif temporel de
  l'algorithme utilisé.

  Exemple :
  ``pf = ADD.get("ForecastCovariance")[-1]``
