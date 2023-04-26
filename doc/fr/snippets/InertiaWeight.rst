.. index:: single: InertiaWeight

InertiaWeight
  *Valeur réelle*. Cette clé indique la part de la vitesse de l'essaim qui est
  imposée à l'insecte, dite "poids de l'inertie". C'est une valeur réelle
  comprise entre 0 et 1. Le défaut est de à peu près :math:`1/(2*ln(2))` et il
  est recommandé de l'adapter au cas physique qui est en traitement.

  Exemple :
  ``{"InertiaWeight":0.72135}``
