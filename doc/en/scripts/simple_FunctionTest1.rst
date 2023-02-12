.. index:: single: FunctionTest (example)

First example
.............

This example describes the test that the given operator works properly, and
that its call proceeds in a way compatible with its common use in the ADAO
algorithms. The required information are minimal, namely here an operator
:math:`F` (described for the test by the command "*ObservationOperator*"), and
a particular state :math:`\mathbf{x}` to test it on (described for the test by
the command "*CheckingPoint*").

The test is repeated a configurable number of times, and a final statistic
makes it possible to quickly verify the operator's good behavior. The simplest
diagnostic consists in checking, at the very end of the display, the order of
magnitude of variations in the values indicated as the mean of the differences
between the repeated outputs and their mean, under the part entitled
"*Characteristics of the mean of the differences between the outputs Y and
their mean Ym*". For a satisfactory operator, these values should be close to
the numerical zero.
