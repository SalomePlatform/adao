.. index:: single: EvolutionModel

EvolutionModel
  *Operator*. The variable indicates the evolution model operator, usually
  noted :math:`M`, which describes an elementary step of evolution. Its value
  is defined as a "*Function*" type object or a "*Matrix*" type one. In the
  case of "*Function*" type, different functional forms can be used, as
  described in the section :ref:`section_ref_operator_requirements`. If there
  is some control :math:`U` included in the evolution model, the operator has
  to be applied to a pair :math:`(X,U)`.
