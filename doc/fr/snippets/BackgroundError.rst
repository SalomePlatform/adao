.. index:: single: BackgroundError
.. index:: single: ScalarSparseMatrix
.. index:: single: DiagonalSparseMatrix

BackgroundError
  *Matrice*. La variable désigne la matrice de covariance des erreurs
  d'ébauche, usuellement notée :math:`\mathbf{B}`. Sa valeur est définie comme
  un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de type
  "*DiagonalSparseMatrix*", comme décrit en détail dans la section
  :ref:`section_ref_covariance_requirements`. Sa disponibilité en sortie est
  conditionnée par le booléen "*Stored*" associé en entrée.
