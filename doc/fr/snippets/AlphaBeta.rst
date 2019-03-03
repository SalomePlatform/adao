.. index:: single: Alpha
.. index:: single: Beta
.. index:: single: Kappa
.. index:: single: Reconditioner

Alpha, Beta, Kappa, Reconditioner
  Ces clés sont des paramètres de mise à l'échelle interne. "Alpha" requiert
  une valeur comprise entre 1.e-4 et 1. "Beta" a une valeur optimale de 2 pour
  une distribution *a priori* gaussienne. "Kappa" requiert une valeur entière,
  dont la bonne valeur par défaut est obtenue en la mettant à 0.
  "Reconditioner" requiert une valeur comprise entre 1.e-3 et 10, son défaut
  étant 1.

  Exemple :
  ``{"Alpha":1,"Beta":2,"Kappa":0,"Reconditioner":1}``
