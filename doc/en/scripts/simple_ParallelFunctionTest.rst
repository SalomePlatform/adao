.. index:: single: FunctionTest (example)

This example describes the test of the correct operation of an operator and
that its call is compatible with its use in the ADAO algorithms. The necessary
information are minimal, namely here an operator of type observation :math:`H`
and a state :math:`\mathbf{x}^b` on which to test it (named "*CheckingPoint*"
for the test).

The test is repeated a customizable number of times, and a final statistic
allows to quickly check the good behavior of the operator. The simplest
diagnostic consists in checking, at the end, the order of magnitude of the
values indicated as the average of the differences between the repeated outputs
Y and their mean Ym*. For a typical operator, these values should be close to
the numerical zero.
