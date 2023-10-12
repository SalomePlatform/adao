Second example
..............

This new example describes the test of the correct operation of a given
operator named ``ControledQuadFunction``, available under its functional form.
It is defined by the command "*ObservationOperator*" as
:ref:`section_ref_operator_funcs` (here, even with this functional form, one
can exceptionally not define the tangent and adjoint forms of the operator
because they are not useful in this test). Using the command "*CheckingPoint*",
one add also a particular state :math:`\mathbf{x}` to test the operator on, and
using the command "*ControlInput*", one add a fixed control :math:`\mathbf{u}`.

The test is arbitrarily repeated here 15 times, and a final statistic makes it
possible to quickly verify the operator's good behavior. The simplest
diagnostic consists in checking, at the very end of the display, the order of
magnitude of variations in the values indicated as the mean of the differences
between the repeated outputs and their mean, under the part entitled
"*Characteristics of the mean of the differences between the outputs Y and
their mean Ym*". For a satisfactory operator, these values should be close to
the numerical zero.
