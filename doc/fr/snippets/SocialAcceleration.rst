.. index:: single: SocialAcceleration

SocialAcceleration
  *Valeur réelle*. Cette clé indique le taux de rappel vers le meilleur insecte
  du voisinage de l'insecte courant, qui est par défaut l'essaim complet. C'est
  une valeur réelle positive. Le défaut est à peu près de
  :math:`1/2+ln(2)=1.19315` et il est recommandé de l'adapter, plutôt en le
  réduisant, au cas physique qui est en traitement.

  Dans le cas standard (non-adaptatif), ce taux est constant et vaut la valeur
  indiquée. Dans le cas adaptatif ASAPSO [Wang09]_, la valeur de cette clé
  indique le taux initial de rappel qui croît ensuite linéairement selon le
  nombre de générations et le facteur associé "*SocialAccelerationControl*".

  Exemple :
  ``{"SocialAcceleration":1.19315}``
