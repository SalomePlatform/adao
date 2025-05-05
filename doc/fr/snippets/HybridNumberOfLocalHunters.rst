.. index:: single: HybridNumberOfLocalHunters

HybridNumberOfLocalHunters
  *Valeur entière*. Cette clé indique le nombre d'insectes sur lesquels la
  recherche locale va être conduite. Les insectes sont choisis comme les
  meilleurs de l'itération courante de la recherche globale. Avec une valeur
  par défaut de 1, la recherche locale est effectuée uniquement sur le
  meilleur. Il est ainsi recommandé d'adapter ce paramètre aux besoins pour des
  problèmes réels.

  Exemple :
  ``{"HybridNumberOfLocalHunters":1}``
