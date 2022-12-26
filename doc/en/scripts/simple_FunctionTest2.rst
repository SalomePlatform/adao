Second example
..............

This new example describes the test of the correct operation of a given
operator named ``QuadFunction``, available under its functional form. It is
defined by the command "*ObservationOperator*" as
:ref:`section_ref_operator_one`. Using the command "*CheckingPoint*", one add
also a particular state :math:`\mathbf{x}` to test the operator on.

The test is repeated here 15 times, and a final statistic makes it possible to
quickly verify the operator's good behavior. The simplest diagnostic consists
in checking, at the very end of the display, the order of magnitude of the
values indicated as the mean of the differences between the repeated outputs
and their mean, under the part entitled "*Characteristics of the mean of the
differences between the outputs Y and their mean Ym*". For a satisfactory
operator, these values should be close to the numerical zero.
