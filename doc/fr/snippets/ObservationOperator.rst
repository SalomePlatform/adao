.. index:: single: ObservationOperator

ObservationOperator
  *Opérateur*. La variable désigne l'opérateur d'observation, usuellement noté
  :math:`H`, qui transforme les paramètres d'entrée :math:`\mathbf{x}` en
  résultats :math:`\mathbf{y}` qui sont à comparer aux observations
  :math:`\mathbf{y}^o`. Sa valeur est définie comme un objet de type
  "*Function*" ou de type "*Matrix*". Dans le cas du type "*Function*",
  différentes formes fonctionnelles peuvent être utilisées, comme décrit dans
  la section :ref:`section_ref_operator_requirements`. Si un contrôle :math:`U`
  est inclus dans le modèle d'observation, l'opérateur doit être appliqué à une
  paire :math:`(X,U)`.
