.. index:: single: ObservationOperator

ObservationOperator
  *Operator*. The variable indicates the observation operator, usually noted as
  :math:`H`, which transforms the input parameters :math:`\mathbf{x}` to
  results :math:`\mathbf{y}` to be compared to observations
  :math:`\mathbf{y}^o`. Its value is defined as a "*Function*" type object or a
  "*Matrix*" type one. In the case of "*Function*" type, different functional
  forms can be used, as described in the section
  :ref:`section_ref_operator_requirements`. If there is some control :math:`U`
  included in the observation, the operator has to be applied to a pair
  :math:`(X,U)`.
