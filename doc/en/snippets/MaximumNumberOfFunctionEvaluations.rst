.. index:: single: MaximumNumberOfFunctionEvaluations

MaximumNumberOfFunctionEvaluations
  This key indicates the maximum number of evaluation of the cost function to
  be optimized. The default is 15000, which is an arbitrary limit. It is then
  recommended to adapt this parameter to the needs on real problems. For some
  optimizers, the effective number of function evaluations can be slightly
  different of the limit due to algorithm internal control requirements.

  Example:
  ``{"MaximumNumberOfFunctionEvaluations":50}``
