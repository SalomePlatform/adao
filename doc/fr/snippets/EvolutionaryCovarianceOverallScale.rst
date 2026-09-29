.. index:: single: EvolutionaryCovarianceOverallScale

EvolutionaryCovarianceOverallScale
  *Valeur réelle*. Cette clé indique l'échelle globale d'adaptation de la
  matrice de covariance lors du processus de recherche évolutionnaire CMA-ES.
  Elle est aussi appelée la taille du pas de recherche, ou :math:`\sigma^g`, ou
  :math:`\sigma^0`. C'est une valeur réelle positive. Le défaut est de
  :math:`0.5` et il est important de l'ajuster au cas physique étudié, en
  l'augmentant ou en le réduisant.

  Exemple :
  ``{"EvolutionaryCovarianceOverallScale":0.5}``

