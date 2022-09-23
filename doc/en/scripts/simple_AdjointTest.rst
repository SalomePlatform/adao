.. index:: single: AdjointTest (example)

This example describes the test of the quality of the adjoint of some operator,
whose direct formulation is given and whose adjoint formulation is here
approximated by default. The required information is minimal, namely here an
operator :math:`F` (described for the test by the observation command
"*ObservationOperator*"), and a state :math:`\mathbf{x}^b` to test it on
(described for the test by the command "*CheckingPoint*"). An observation
:math:`\mathbf{y}^o` can be given as here (described for the test by the
command "*Observation*"). The output has been set to determine the printout,
for example to make more easy automatic comparison.

The actual check is to observe whether the residue is consistently equal to
zero at the accuracy of the calculation.
