.. index:: single: EvolutionError

EvolutionError
  *Matrice*. La variable désigne la matrice de covariance des erreurs *a
  priori* d'évolution, usuellement notée :math:`\mathbf{Q}`. Sa valeur est
  définie comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou
  de type "*DiagonalSparseMatrix*", comme décrit en détail dans la section
  :ref:`section_ref_covariance_requirements`. Sa disponibilité en sortie est
  conditionnée par le booléen "*Stored*" associé en entrée.
