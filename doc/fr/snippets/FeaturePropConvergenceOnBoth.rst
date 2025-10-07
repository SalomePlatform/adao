.. index:: single: Convergence sur critère(s) de résidu ou de nombre

- Les méthodes proposées par cet algorithme **atteignent leur convergence sur
  un ou plusieurs critères de résidu ou de nombre**. En pratique, il peut y
  avoir plusieurs critères de convergence actifs simultanément.

  Le résidu peut être une mesure standard basée sur un écart ("*écart
  calculs-mesures*" par exemple), ou une valeur remarquable liée à l'algorithme
  ("*nullité d'un gradient*" par exemple).

  Le nombre est fréquemment un élément remarquable lié à l'algorithme, comme un
  nombre d'itérations ou un nombre d'évaluations, mais cela peut aussi être par
  exemple un nombre de générations pour un algorithme évolutionnaire.

  Il convient de régler soigneusement les seuils de convergence, pour limiter
  le coût calcul global de l'algorithme, ou pour assurer une adaptation de la
  convergence au cas physique traité.
