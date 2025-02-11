.. index:: single: SocialAccelerationControl

SocialAccelerationControl
  *Valeur réelle*. Cette clé indique le facteur de changement dans le taux de
  rappel vers le meilleur insecte du voisinage de l'insecte courant, qui est
  par défaut l'essaim complet. C'est une valeur réelle positive dont le défaut
  est 0, c'est-à-dire que, par défaut, il n'y a aucun changement du taux de
  rappel.

  Dans le cas adaptatif ASAPSO [Wang09]_, la valeur de cette clé indique le
  facteur de **croissance linéaire** du taux de rappel avec le nombre de
  générations (rapporté au nombre total demandé de générations), sachant que la
  valeur initiale du taux est indiquée par le facteur associé
  "*SocialAcceleration*". Il n'y a pas de valeur recommandée, mais on peut par
  exemple utiliser la valeur initiale :math:`1.19315` du facteur associé si
  l'on veut doubler le rappel vers la meilleure valeur connue du voisinage à la
  fin des itérations.

  Exemple :
  ``{"SocialAccelerationControl":0.}``
