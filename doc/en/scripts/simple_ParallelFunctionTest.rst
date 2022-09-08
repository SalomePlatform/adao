.. index:: single: FunctionTest (example)

This example describes the test of the correct operation of a given operator,
and that its call proceeds in a way compatible with its common use in parallel
in the ADAO algorithms. The required information are minimal, namely here an
operator :math:`F` (described for the test by the observation command
"*ObservationOperator*"), and a state :math:`\mathbf{x}^b` to test it on
(described for the test by the command "*CheckingPoint*").

The test is repeated a configurable number of times, and a final statistic
makes it possible to quickly verify the operator's good behavior. The simplest
diagnostic consists in checking, at the very end of the display, the order of
magnitude of the values indicated as the mean of the differences between the
repeated outputs and their mean, under the part entitled "*Characteristics of
the mean of the differences between the outputs Y and their mean Ym*". For a
satisfactory operator, these values should be close to the numerical zero.

.. note::

    .. index:: single: EnableMultiProcessingInEvaluation

    It can be useful to make sure that the evaluation of the operator is really
    done in parallel, and for example that there is no forced use of a
    parallelism acceleration, which would avoid a real parallel test. For this
    purpose, it is recommended to systematically use the boolean special
    parameter "*EnableMultiProcessingInEvaluation*", exclusively reserved for
    this purpose, of the operator declaration command. The use of this
    parameter is illustrated in this example. It should not be used in any
    other case.
