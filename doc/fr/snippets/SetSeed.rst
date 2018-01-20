.. index:: single: SetSeed

SetSeed
  Cette clé permet de donner un nombre entier pour fixer la graine du
  générateur aléatoire utilisé dans l'algorithme. Une valeur simple est par
  exemple 1000. Par défaut, la graine est laissée non initialisée, et elle
  utilise ainsi l'initialisation par défaut de l'ordinateur, qui varie donc à
  chaque étude. Pour assurer la reproductibilité de résultats impliquant des
  tirages aléatoires, il est fortement conseiller d'initialiser la graine.

  Exemple :
  ``{"SetSeed":1000}``
