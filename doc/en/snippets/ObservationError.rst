.. index:: single: ObservationError
.. index:: single: ScalarSparseMatrix
.. index:: single: DiagonalSparseMatrix

ObservationError
  *Matrix*. The variable indicates the observation error covariance matrix,
  usually noted as :math:`\mathbf{R}`. It is defined as a "*Matrix*" type
  object, a "*ScalarSparseMatrix*" type object, or a "*DiagonalSparseMatrix*"
  type object, as described in detail in the section
  :ref:`section_ref_covariance_requirements`. Its availability in output is
  conditioned by the boolean "*Stored*" associated with input.
