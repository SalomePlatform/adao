.. index:: single: SetSeed

SetSeed
  *Valeur entière*. Cette clé permet de donner un nombre entier pour fixer la
  graine du générateur aléatoire utilisé dans l'algorithme. Par défaut, la
  graine est laissée non initialisée, et elle utilise ainsi l'initialisation
  par défaut de l'ordinateur, qui varie donc à chaque étude. Pour assurer la
  reproductibilité de résultats impliquant des tirages aléatoires, il est
  fortement conseillé d'initialiser la graine. Une valeur simple est par
  exemple 123456789. Il est conseillé de mettre un entier à plus de 6 ou 7
  chiffres pour bien initialiser le générateur aléatoire.

  Exemple :
  ``{"SetSeed":123456789}``
