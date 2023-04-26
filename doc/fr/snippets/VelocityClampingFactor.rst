.. index:: single: VelocityClampingFactor

VelocityClampingFactor
  *Valeur réelle*. Cette clé indique le taux d'atténuation de la vitesse de
  groupe dans la mise à jour pour chaque insecte, utile pour éviter l'explosion
  de l'essaim, c'est-à-dire une croissance incontrôlée de la vitesse des
  insectes. C'est une valeur réelle comprise entre 0+ et 1. Le défaut est de
  0.3.

  Exemple :
  ``{"VelocityClampingFactor":0.3}``

