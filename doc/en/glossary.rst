.. _section_glossary:

Glossary
========

.. glossary::
   :sorted:

   case
      One case is defined by a set of data and of choices, packed together
      through the user interface of the module. The data are physical
      measurements that have to be available before or during the case
      execution. The simulation code(s) and the assimilation methods and
      parameters has to be chosen, they define the execution properties of the
      case.

   iteration
      One iteration occurs when using iterative optimizers (e.g. 3DVAR), and it
      is entirely hidden in the main YACS OptimizerLoop Node named
      "compute_bloc". Nevertheless, the user can watch the iterative process
      through the *YACS Container Log* window, which is updated during the
      process, and using *Observers* attached to calculation variables.

   APosterioriCovariance
      Keyword to indicate the covariance matrix of *a posteriori* analysis
      errors.

   BMA (Background minus Analysis)
      Difference between the simulation based on the background state and the
      one base on the optimal state estimation, noted as :math:`\mathbf{x}^b -
      \mathbf{x}^a`.

   OMA (Observation minus Analysis)
      Difference between the observations and the result of the simulation based
      on the optimal state estimation, the analysis, filtered to be compatible
      with the observation, noted as :math:`\mathbf{y}^o -
      \mathbf{H}\mathbf{x}^a`.

   OMB (Observation minus Background)
      Difference between the observations and the result of the simulation based
      on the background state, filtered to be compatible with the observation,
      noted as :math:`\mathbf{y}^o - \mathbf{H}\mathbf{x}^b`.

   SigmaBck2
      Keyword to indicate the Desroziers-Ivanov parameter measuring the
      background part consistency of the data assimilation optimal state
      estimation. It can be compared to 1.

   SigmaObs2
      Keyword to indicate the Desroziers-Ivanov parameter measuring the
      observation part consistency of the data assimilation optimal state
      estimation. It can be compared to 1.

   MahalanobisConsistency
      Keyword to indicate the Mahalanobis parameter measuring the consistency of
      the data assimilation optimal state estimation. It can be compared to 1.

   analysis
      The optimal state estimation through a data assimilation or optimization
      procedure.

   innovation
      Difference between the observations and the result of the simulation based
      on the background state, filtered to be compatible with the observation.
      It is similar with OMB in static cases.

   CostFunctionJ
      Keyword to indicate the minimization function, noted as :math:`J`.

   CostFunctionJo
      Keyword to indicate the observation part of the minimization function,
      noted as :math:`J^o`.

   CostFunctionJb
      Keyword to indicate the background part of the minimization function,
      noted as :math:`J^b`.
