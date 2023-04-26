.. index:: single: CognitiveAcceleration

CognitiveAcceleration
  *Valeur réelle*. Cette clé indique le taux de rappel vers la meilleure valeur
  connue précédemment de l'insecte courant. C'est une valeur réelle positive.
  Le défaut est à peu près de :math:`1/2+ln(2)` et il est recommandé de
  l'adapter, plutôt en le réduisant, au cas physique qui est en traitement.

  Exemple :
  ``{"CognitiveAcceleration":1.19315}``

