.. index:: single: Convergence sur critère(s) de résidu

- Les méthodes proposées par cet algorithme **atteignent leur convergence sur
  un ou plusieurs critères de résidu**. En pratique, il peut y avoir plusieurs
  critères de convergence actifs simultanément.

  Le résidu peut être une mesure standard basée sur un écart ("*écart
  calculs-mesures*" par exemple), ou être une valeur remarquable lié à
  l'algorithme ("*nullité d'un gradient*" par exemple).

  Il convient de régler soigneusement les seuils de convergence, pour limiter
  le coût calcul global de l'algorithme, ou pour assurer une adaptation de la
  convergence au cas physique traité.
