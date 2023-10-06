.. index:: single: SampledStateForQuantiles

SampledStateForQuantiles
  *Liste de séries de vecteurs*. Chaque élément est une série de vecteurs
  d'état colonnes, généré pour estimer par simulation et/ou observation les
  valeurs de quantiles requis par l'utilisateur. Il y a autant d'états que le
  nombre d'échantillons requis pour cette estimation de quantiles.

  Exemple :
  ``xq = ADD.get("SampledStateForQuantiles")[:]``
