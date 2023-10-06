.. index:: single: SocialAcceleration

SocialAcceleration
  *Valeur réelle*. Cette clé indique le taux de rappel vers le meilleur insecte
  du voisinage de l'insecte courant, qui est par défaut l'essaim complet. C'est
  une valeur réelle positive. Le défaut est à peu près de
  :math:`1/2+ln(2)=1.19315` et il est recommandé de l'adapter, plutôt en le
  réduisant, au cas physique qui est en traitement.

  Exemple :
  ``{"SocialAcceleration":1.19315}``
