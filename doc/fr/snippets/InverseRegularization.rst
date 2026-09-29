.. index:: single: InverseRegularization

InverseRegularization
  *Valeur réelle*. Cette clé indique le type de régularisation dans le calcul
  inverse des coordonnées réduites lors d'une approximation base réduite.
  Lorsqu'elle est strictement négative (et c'est la valeur par défaut), on
  utilise le pseudo-inverse. Lorsqu'elle est strictement positive, on utilise
  une régularisation avec comme coefficient additionnel la valeur contenue dans
  la clé. Lorsqu'elle est nulle, on utilise une inversion directe. Les trois
  méthodes sont équivalentes en théorie et dans les cas de dimension courantes.
  Le défaut est la plus précise. Il est fortement recommandé de conserver la
  valeur par défaut.

  Exemple :
  ``{"InverseRegularization":-1}``
