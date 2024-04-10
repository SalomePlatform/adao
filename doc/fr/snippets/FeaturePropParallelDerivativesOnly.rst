.. index:: single: Parallélisme de dérivation

- Les méthodes proposées par cet algorithme **ne présentent pas de parallélisme
  interne, mais utilisent la dérivation numérique d'opérateur(s) qui est, elle,
  parallélisable**. L'interaction potentielle, entre le parallélisme de la
  dérivation numérique, et le parallélisme éventuellement présent dans les
  opérateurs d'observation ou d'évolution de l'utilisateur, doit donc être
  soigneusement réglée.
