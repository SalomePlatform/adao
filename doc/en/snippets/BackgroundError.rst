.. index:: single: BackgroundError
.. index:: single: ScalarSparseMatrix
.. index:: single: DiagonalSparseMatrix

BackgroundError
  *Matrix*. This indicates the background error covariance matrix, previously
  noted as :math:`\mathbf{B}`. Its value is defined as a "*Matrix*" type
  object, a "*ScalarSparseMatrix*" type object, or a "*DiagonalSparseMatrix*"
  type object, as described in detail in the section
  :ref:`section_ref_covariance_requirements`. Its availability in output is
  conditioned by the boolean "*Stored*" associated with input.
