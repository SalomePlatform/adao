.. index:: single: EpsilonMinimumExponent

EpsilonMinimumExponent
  *Valeur entière*. Cette clé indique la valeur de l'exposant minimal du
  coefficient en puissance de 10 qui doit être utilisé pour faire décroître le
  multiplicateur de l'incrément. La valeur par défaut est de -8, et elle doit
  être négative entre 0 et -20. Par exemple, la valeur par défaut conduit à
  calculer le résidu de la formule avec un incrément fixe multiplié par 1.e0
  jusqu'à 1.e-8.

  Exemple :
  ``{"EpsilonMinimumExponent":-12}``
