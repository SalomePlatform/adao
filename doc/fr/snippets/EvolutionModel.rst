.. index:: single: EvolutionModel

EvolutionModel
  *Opérateur*. La variable désigne l'opérateur d'évolution du modèle,
  usuellement noté :math:`M`, qui décrit un pas élémentaire d'évolution
  dynamique ou itérative. Sa valeur est définie comme un objet de type
  "*Function*" ou de type "*Matrix*". Dans le cas du type "*Function*",
  différentes formes fonctionnelles peuvent être utilisées, comme décrit dans
  la section :ref:`section_ref_operator_requirements`. Si un contrôle :math:`U`
  est inclus dans le modèle d'observation, l'opérateur doit être appliqué à une
  paire :math:`(X,U)`.
