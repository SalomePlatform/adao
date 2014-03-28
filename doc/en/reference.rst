.. _section_reference:

================================================================================
Reference description of the ADAO commands and keywords
================================================================================

This section presents the reference description of the ADAO commands and
keywords available through the GUI or through scripts.

Each command or keyword to be defined through the ADAO GUI has some properties.
The first property is to be *required*, *optional* or only factual, describing a
type of input. The second property is to be an "open" variable with a fixed type
but with any value allowed by the type, or a "restricted" variable, limited to
some specified values. The EFICAS editor GUI having build-in validating
capacities, the properties of the commands or keywords given through this GUI
are automatically correct. 

The mathematical notations used afterward are explained in the section
:ref:`section_theory`.

Examples of using these commands are available in the section
:ref:`section_examples` and in example files installed with ADAO module.

List of possible input types
----------------------------

.. index:: single: Dict
.. index:: single: Function
.. index:: single: Matrix
.. index:: single: ScalarSparseMatrix
.. index:: single: DiagonalSparseMatrix
.. index:: single: String
.. index:: single: Script
.. index:: single: Vector

Each ADAO variable has a pseudo-type to help filling it and validation. The
different pseudo-types are:

**Dict**
    This indicates a variable that has to be filled by a Python dictionary
    ``{"key":"value...}``, usually given either as a string or as a script file.

**Function**
    This indicates a variable that has to be filled by a Python function,
    usually given as a script file or a component method.

**Matrix**
    This indicates a variable that has to be filled by a matrix, usually given
    either as a string or as a script file.

**ScalarSparseMatrix**
    This indicates a variable that has to be filled by a unique number (which
    will be used to multiply an identity matrix), usually given either as a
    string or as a script file.

**DiagonalSparseMatrix**
    This indicates a variable that has to be filled by a vector (which will be
    used to replace the diagonal of an identity matrix), usually given either as
    a string or as a script file.

**Script**
    This indicates a script given as an external file. It can be described by a
    full absolute path name or only by the file name without path. If the file
    is given only by a file name without path, and if a study directory is also
    indicated, the file is searched in the given directory.

**String**
    This indicates a string giving a literal representation of a matrix, a
    vector or a vector serie, such as "1 2 ; 3 4" or "[[1,2],[3,4]]" for a
    square 2x2 matrix.

**Vector**
    This indicates a variable that has to be filled by a vector, usually given
    either as a string or as a script file.

**VectorSerie**
    This indicates a variable that has to be filled by a list of
    vectors, usually given either as a string or as a script file.

When a command or keyword can be filled by a script file name, the script has to
contain a variable or a method that has the same name as the one to be filled.
In other words, when importing the script in a YACS Python node, it must create
a variable of the good name in the current namespace of the node.

Reference description for ADAO calculation cases
------------------------------------------------

List of commands and keywords for an ADAO calculation case
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ASSIMILATION_STUDY
.. index:: single: Algorithm
.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: ControlInput
.. index:: single: Debug
.. index:: single: EvolutionError
.. index:: single: EvolutionModel
.. index:: single: InputVariables
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: Observers
.. index:: single: OutputVariables
.. index:: single: Study_name
.. index:: single: Study_repertory
.. index:: single: UserDataInit
.. index:: single: UserPostAnalysis

The first set of commands is related to the description of a calculation case,
that is a *Data Assimilation* procedure or an *Optimization* procedure. The
terms are ordered in alphabetical order, except the first, which describes
choice between calculation or checking. The different commands are the
following:

**ASSIMILATION_STUDY**
    *Required command*. This is the general command describing the data
    assimilation or optimization case. It hierarchically contains all the other
    commands.

**Algorithm**
    *Required command*. This is a string to indicate the data assimilation or
    optimization algorithm chosen. The choices are limited and available through
    the GUI. There exists for example "3DVAR", "Blue"... See below the list of
    algorithms and associated parameters in the following subsection `Optional
    and required commands for calculation algorithms`_.

**AlgorithmParameters**
    *Optional command*. This command allows to add some optional parameters to
    control the data assimilation or optimization algorithm. Its value is
    defined as a "*Dict*" type object. See below the list of algorithms and
    associated parameters in the following subsection `Optional and required
    commands for calculation algorithms`_.

**Background**
    *Required command*. This indicates the background or initial vector used,
    previously noted as :math:`\mathbf{x}^b`. Its value is defined as a
    "*Vector*" type object.

**BackgroundError**
    *Required command*. This indicates the background error covariance matrix,
    previously noted as :math:`\mathbf{B}`. Its value is defined as a "*Matrix*"
    type object, a "*ScalarSparseMatrix*" type object, or a
    "*DiagonalSparseMatrix*" type object.

**ControlInput**
    *Optional command*. This indicates the control vector used to force the
    evolution model at each step, usually noted as :math:`\mathbf{U}`. Its value
    is defined as a "*Vector*" or a *VectorSerie* type object. When there is no
    control, it has to be a void string ''.

**Debug**
    *Optional command*. This define the level of trace and intermediary debug
    information. The choices are limited between 0 (for False) and 1 (for
    True).

**EvolutionError**
    *Optional command*. This indicates the evolution error covariance matrix,
    usually noted as :math:`\mathbf{Q}`. It is defined as a "*Matrix*" type
    object, a "*ScalarSparseMatrix*" type object, or a "*DiagonalSparseMatrix*"
    type object.

**EvolutionModel**
    *Optional command*. This indicates the evolution model operator, usually
    noted :math:`M`, which describes an elementary step of evolution. Its value
    is defined as a "*Function*" type object. Different functional forms can be
    used, as described in the following subsection `Requirements for functions
    describing an operator`_. If there is some control :math:`U` included in the
    evolution model, the operator has to be applied to a pair :math:`(X,U)`.

**InputVariables**
    *Optional command*. This command allows to indicates the name and size of
    physical variables that are bundled together in the state vector. This
    information is dedicated to data processed inside an algorithm.

**Observation**
    *Required command*. This indicates the observation vector used for data
    assimilation or optimization, previously noted as :math:`\mathbf{y}^o`. It
    is defined as a "*Vector*" or a *VectorSerie* type object.

**ObservationError**
    *Required command*. This indicates the observation error covariance matrix,
    previously noted as :math:`\mathbf{R}`. It is defined as a "*Matrix*" type
    object, a "*ScalarSparseMatrix*" type object, or a "*DiagonalSparseMatrix*"
    type object.

**ObservationOperator**
    *Required command*. This indicates the observation operator, previously
    noted :math:`H`, which transforms the input parameters :math:`\mathbf{x}` to
    results :math:`\mathbf{y}` to be compared to observations
    :math:`\mathbf{y}^o`. Its value is defined as a "*Function*" type object.
    Different functional forms can be used, as described in the following
    subsection `Requirements for functions describing an operator`_. If there is
    some control :math:`U` included in the observation, the operator has to be
    applied to a pair :math:`(X,U)`.

**Observers**
    *Optional command*. This command allows to set internal observers, that are
    functions linked with a particular variable, which will be executed each
    time this variable is modified. It is a convenient way to monitor variables
    of interest during the data assimilation or optimization process, by
    printing or plotting it, etc. Common templates are provided to help the user
    to start or to quickly make his case.

**OutputVariables**
    *Optional command*. This command allows to indicates the name and size of
    physical variables that are bundled together in the output observation
    vector. This information is dedicated to data processed inside an algorithm.

**Study_name**
    *Required command*. This is an open string to describe the ADAO study by a
    name or a sentence.

**Study_repertory**
    *Optional command*. If available, this directory is used as base name for
    calculation, and used to find all the script files, given by name without
    path, that can be used to define some other commands by scripts.

**UserDataInit**
    *Optional command*. This commands allows to initialize some parameters or
    data automatically before data assimilation or optimisation algorithm input
    processing. It indicates a script file name to be executed before entering
    in initialization phase of chosen variables.

**UserPostAnalysis**
    *Optional command*. This commands allows to process some parameters or data
    automatically after data assimilation or optimization algorithm processing.
    Its value is defined as a script file or a string, allowing to put
    post-processing code directly inside the ADAO case. Common templates are
    provided to help the user to start or to quickly make his case.

Optional and required commands for calculation algorithms
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: 3DVAR
.. index:: single: Blue
.. index:: single: ExtendedBlue
.. index:: single: EnsembleBlue
.. index:: single: KalmanFilter
.. index:: single: ExtendedKalmanFilter
.. index:: single: UnscentedKalmanFilter
.. index:: single: LinearLeastSquares
.. index:: single: NonLinearLeastSquares
.. index:: single: ParticleSwarmOptimization
.. index:: single: QuantileRegression

.. index:: single: AlgorithmParameters
.. index:: single: Bounds
.. index:: single: CostDecrementTolerance
.. index:: single: GradientNormTolerance
.. index:: single: GroupRecallRate
.. index:: single: MaximumNumberOfSteps
.. index:: single: Minimizer
.. index:: single: NumberOfInsects
.. index:: single: ProjectedGradientTolerance
.. index:: single: QualityCriterion
.. index:: single: Quantile
.. index:: single: SetSeed
.. index:: single: StoreInternalVariables
.. index:: single: StoreSupplementaryCalculations
.. index:: single: SwarmVelocity

Each algorithm can be controlled using some generic or specific options, given
through the "*AlgorithmParameters*" optional command in a script file or a
sring, as follows for example in a file::

    AlgorithmParameters = {
        "Minimizer" : "LBFGSB",
        "MaximumNumberOfSteps" : 25,
        "StoreSupplementaryCalculations" : ["APosterioriCovariance","OMA"],
        }

To give the "*AlgorithmParameters*" values by string, one must enclose a
standard dictionnary definition between simple quotes, as for example::

    '{"Minimizer":"LBFGSB","MaximumNumberOfSteps":25}'

This section describes the available options algorithm by algorithm. In
addition, for each algorithm, the required commands/keywords are given, being
described in `List of commands and keywords for an ADAO calculation case`_. If
an option is specified by the user for an algorithm that doesn't support it, the
option is simply left unused and don't stop the treatment. The meaning of the
acronyms or particular names can be found in the :ref:`genindex` or the
:ref:`section_glossary`.

**"Blue"**

  *Required commands*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  StoreInternalVariables
    This boolean key allows to store default internal variables, mainly the
    current state during iterative optimization process. Be careful, this can be
    a numerically costly choice in certain calculation cases. The default is
    "False".

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations. The default is a void list, none of these variables being
    calculated and stored by default. The possible names are in the following
    list: ["APosterioriCovariance", "BMA", "OMA", "OMB", "Innovation",
    "SigmaBck2", "SigmaObs2", "MahalanobisConsistency"].

**"ExtendedBlue"**

  *Required commands*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  StoreInternalVariables
    This boolean key allows to store default internal variables, mainly the
    current state during iterative optimization process. Be careful, this can be
    a numerically costly choice in certain calculation cases. The default is
    "False".

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations. The default is a void list, none of these variables being
    calculated and stored by default. The possible names are in the following
    list: ["APosterioriCovariance", "BMA", "OMA", "OMB", "Innovation",
    "SigmaBck2", "SigmaObs2", "MahalanobisConsistency"].

**"LinearLeastSquares"**

  *Required commands*
    *"Observation", "ObservationError",
    "ObservationOperator"*

  StoreInternalVariables
    This boolean key allows to store default internal variables, mainly the
    current state during iterative optimization process. Be careful, this can be
    a numerically costly choice in certain calculation cases. The default is
    "False".

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations. The default is a void list, none of these variables being
    calculated and stored by default. The possible names are in the following
    list: ["OMA"].

**"3DVAR"**

  *Required commands*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  Minimizer
    This key allows to choose the optimization minimizer. The default choice is
    "LBFGSB", and the possible ones are "LBFGSB" (nonlinear constrained
    minimizer, see [Byrd95]_, [Morales11]_ and [Zhu97]_), "TNC" (nonlinear
    constrained minimizer), "CG" (nonlinear unconstrained minimizer), "BFGS"
    (nonlinear unconstrained minimizer), "NCG" (Newton CG minimizer). It is
    recommended to stay with the default.

  Bounds
    This key allows to define upper and lower bounds for every state variable
    being optimized. Bounds can be given by a list of list of pairs of
    lower/upper bounds for each variable, with possibly ``None`` every time
    there is no bound. The bounds can always be specified, but they are taken
    into account only by the constrained minimizers.

  MaximumNumberOfSteps
    This key indicates the maximum number of iterations allowed for iterative
    optimization. The default is 15000, which is very similar to no limit on
    iterations. It is then recommended to adapt this parameter to the needs on
    real problems. For some minimizers, the effective stopping step can be
    slightly different of the limit due to algorithm internal control
    requirements.

  CostDecrementTolerance
    This key indicates a limit value, leading to stop successfully the
    iterative optimization process when the cost function decreases less than
    this tolerance at the last step. The default is 1.e-7, and it is
    recommended to adapt it to the needs on real problems.

  ProjectedGradientTolerance
    This key indicates a limit value, leading to stop successfully the iterative
    optimization process when all the components of the projected gradient are
    under this limit. It is only used for constrained minimizers. The default is
    -1, that is the internal default of each minimizer (generally 1.e-5), and it
    is not recommended to change it.

  GradientNormTolerance
    This key indicates a limit value, leading to stop successfully the
    iterative optimization process when the norm of the gradient is under this
    limit. It is only used for non-constrained minimizers.  The default is
    1.e-5 and it is not recommended to change it.

  StoreInternalVariables
    This boolean key allows to store default internal variables, mainly the
    current state during iterative optimization process. Be careful, this can be
    a numerically costly choice in certain calculation cases. The default is
    "False".

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations. The default is a void list, none of these variables being
    calculated and stored by default. The possible names are in the following
    list: ["APosterioriCovariance", "BMA", "OMA", "OMB", "Innovation",
    "SigmaObs2", "MahalanobisConsistency"].

**"NonLinearLeastSquares"**

  *Required commands*
    *"Background",
    "Observation", "ObservationError",
    "ObservationOperator"*

  Minimizer
    This key allows to choose the optimization minimizer. The default choice is
    "LBFGSB", and the possible ones are "LBFGSB" (nonlinear constrained
    minimizer, see [Byrd95]_, [Morales11]_ and [Zhu97]_), "TNC" (nonlinear
    constrained minimizer), "CG" (nonlinear unconstrained minimizer), "BFGS"
    (nonlinear unconstrained minimizer), "NCG" (Newton CG minimizer). It is
    recommended to stay with the default.

  Bounds
    This key allows to define upper and lower bounds for every state variable
    being optimized. Bounds can be given by a list of list of pairs of
    lower/upper bounds for each variable, with possibly ``None`` every time
    there is no bound. The bounds can always be specified, but they are taken
    into account only by the constrained minimizers.

  MaximumNumberOfSteps
    This key indicates the maximum number of iterations allowed for iterative
    optimization. The default is 15000, which is very similar to no limit on
    iterations. It is then recommended to adapt this parameter to the needs on
    real problems. For some minimizers, the effective stopping step can be
    slightly different due to algorithm internal control requirements.

  CostDecrementTolerance
    This key indicates a limit value, leading to stop successfully the
    iterative optimization process when the cost function decreases less than
    this tolerance at the last step. The default is 1.e-7, and it is
    recommended to adapt it to the needs on real problems.

  ProjectedGradientTolerance
    This key indicates a limit value, leading to stop successfully the iterative
    optimization process when all the components of the projected gradient are
    under this limit. It is only used for constrained minimizers. The default is
    -1, that is the internal default of each minimizer (generally 1.e-5), and it
    is not recommended to change it.

  GradientNormTolerance
    This key indicates a limit value, leading to stop successfully the
    iterative optimization process when the norm of the gradient is under this
    limit. It is only used for non-constrained minimizers.  The default is
    1.e-5 and it is not recommended to change it.

  StoreInternalVariables
    This boolean key allows to store default internal variables, mainly the
    current state during iterative optimization process. Be careful, this can be
    a numerically costly choice in certain calculation cases. The default is
    "False".

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations. The default is a void list, none of these variables being
    calculated and stored by default. The possible names are in the following
    list: ["BMA", "OMA", "OMB", "Innovation"].

**"EnsembleBlue"**

  *Required commands*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  SetSeed
    This key allow to give an integer in order to fix the seed of the random
    generator used to generate the ensemble. A convenient value is for example
    1000. By default, the seed is left uninitialized, and so use the default
    initialization from the computer.

**"KalmanFilter"**

  *Required commands*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  EstimationOf
    This key allows to choose the type of estimation to be performed. It can be
    either state-estimation, with a value of "State", or parameter-estimation,
    with a value of "Parameters". The default choice is "State".

  StoreInternalVariables
    This boolean key allows to store default internal variables, mainly the
    current state during iterative optimization process. Be careful, this can be
    a numerically costly choice in certain calculation cases. The default is
    "False".

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations. The default is a void list, none of these variables being
    calculated and stored by default. The possible names are in the following
    list: ["APosterioriCovariance", "BMA", "Innovation"].

**"ExtendedKalmanFilter"**

  *Required commands*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  Bounds
    This key allows to define upper and lower bounds for every state variable
    being optimized. Bounds can be given by a list of list of pairs of
    lower/upper bounds for each variable, with extreme values every time there
    is no bound. The bounds can always be specified, but they are taken into
    account only by the constrained minimizers.

  ConstrainedBy
    This key allows to define the method to take bounds into account. The
    possible methods are in the following list: ["EstimateProjection"].

  EstimationOf
    This key allows to choose the type of estimation to be performed. It can be
    either state-estimation, with a value of "State", or parameter-estimation,
    with a value of "Parameters". The default choice is "State".

  StoreInternalVariables
    This boolean key allows to store default internal variables, mainly the
    current state during iterative optimization process. Be careful, this can be
    a numerically costly choice in certain calculation cases. The default is
    "False".

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations. The default is a void list, none of these variables being
    calculated and stored by default. The possible names are in the following
    list: ["APosterioriCovariance", "BMA", "Innovation"].

**"UnscentedKalmanFilter"**

  *Required commands*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  Bounds
    This key allows to define upper and lower bounds for every state variable
    being optimized. Bounds can be given by a list of list of pairs of
    lower/upper bounds for each variable, with extreme values every time there
    is no bound. The bounds can always be specified, but they are taken into
    account only by the constrained minimizers.

  ConstrainedBy
    This key allows to define the method to take bounds into account. The
    possible methods are in the following list: ["EstimateProjection"].

  EstimationOf
    This key allows to choose the type of estimation to be performed. It can be
    either state-estimation, with a value of "State", or parameter-estimation,
    with a value of "Parameters". The default choice is "State".
  
  Alpha, Beta, Kappa, Reconditioner
    These keys are internal scaling parameters. "Alpha" requires a value between
    1.e-4 and 1. "Beta" has an optimal value of 2 for gaussian *a priori*
    distribution. "Kappa" requires an integer value, and the right default is
    obtained by setting it to 0. "Reconditioner" requires a value between 1.e-3
    and 10, it defaults to 1.

  StoreInternalVariables
    This boolean key allows to store default internal variables, mainly the
    current state during iterative optimization process. Be careful, this can be
    a numerically costly choice in certain calculation cases. The default is
    "False".

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations. The default is a void list, none of these variables being
    calculated and stored by default. The possible names are in the following
    list: ["APosterioriCovariance", "BMA", "Innovation"].

**"ParticleSwarmOptimization"**

  *Required commands*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  MaximumNumberOfSteps
    This key indicates the maximum number of iterations allowed for iterative
    optimization. The default is 50, which is an arbitrary limit. It is then
    recommended to adapt this parameter to the needs on real problems.

  NumberOfInsects
    This key indicates the number of insects or particles in the swarm. The
    default is 100, which is a usual default for this algorithm.

  SwarmVelocity
    This key indicates the part of the insect velocity which is imposed by the 
    swarm. It is a positive floating point value. The default value is 1.

  GroupRecallRate
    This key indicates the recall rate at the best swarm insect. It is a
    floating point value between 0 and 1. The default value is 0.5.

  QualityCriterion
    This key indicates the quality criterion, minimized to find the optimal
    state estimate. The default is the usual data assimilation criterion named
    "DA", the augmented ponderated least squares. The possible criteria has to
    be in the following list, where the equivalent names are indicated by "=":
    ["AugmentedPonderatedLeastSquares"="APLS"="DA",
    "PonderatedLeastSquares"="PLS", "LeastSquares"="LS"="L2",
    "AbsoluteValue"="L1", "MaximumError"="ME"]

  SetSeed
    This key allow to give an integer in order to fix the seed of the random
    generator used to generate the ensemble. A convenient value is for example
    1000. By default, the seed is left uninitialized, and so use the default
    initialization from the computer.

  StoreInternalVariables
    This boolean key allows to store default internal variables, mainly the
    current state during iterative optimization process. Be careful, this can be
    a numerically costly choice in certain calculation cases. The default is
    "False".

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations. The default is a void list, none of these variables being
    calculated and stored by default. The possible names are in the following
    list: ["BMA", "OMA", "OMB", "Innovation"].

**"QuantileRegression"**

  *Required commands*
    *"Background",
    "Observation",
    "ObservationOperator"*

  Quantile
    This key allows to define the real value of the desired quantile, between
    0 and 1. The default is 0.5, corresponding to the median.

  Minimizer
    This key allows to choose the optimization minimizer. The default choice
    and only available choice is "MMQR" (Majorize-Minimize for Quantile
    Regression).

  MaximumNumberOfSteps
    This key indicates the maximum number of iterations allowed for iterative
    optimization. The default is 15000, which is very similar to no limit on
    iterations. It is then recommended to adapt this parameter to the needs on
    real problems.

  CostDecrementTolerance
    This key indicates a limit value, leading to stop successfully the
    iterative optimization process when the cost function or the surrogate
    decreases less than this tolerance at the last step. The default is 1.e-6,
    and it is recommended to adapt it to the needs on real problems.

  StoreInternalVariables
    This boolean key allows to store default internal variables, mainly the
    current state during iterative optimization process. Be careful, this can be
    a numerically costly choice in certain calculation cases. The default is
    "False".

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations. The default is a void list, none of these variables being
    calculated and stored by default. The possible names are in the following
    list: ["BMA", "OMA", "OMB", "Innovation"].

Reference description for ADAO checking cases
---------------------------------------------

List of commands and keywords for an ADAO checking case
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: CHECKING_STUDY
.. index:: single: Algorithm
.. index:: single: AlgorithmParameters
.. index:: single: CheckingPoint
.. index:: single: Debug
.. index:: single: ObservationOperator
.. index:: single: Study_name
.. index:: single: Study_repertory
.. index:: single: UserDataInit

The second set of commands is related to the description of a checking case,
that is a procedure to check required properties on information somewhere else
by a calculation case. The terms are ordered in alphabetical order, except the
first, which describes choice between calculation or checking. The different
commands are the following:

**CHECKING_STUDY**
    *Required command*. This is the general command describing the checking
    case. It hierarchically contains all the other commands.

**Algorithm**
    *Required command*. This is a string to indicate the test algorithm chosen.
    The choices are limited and available through the GUI. There exists for
    example "FunctionTest", "AdjointTest"... See below the list of algorithms
    and associated parameters in the following subsection `Optional and required
    commands for checking algorithms`_.

**AlgorithmParameters** *Optional command*. This command allows to add some
    optional parameters to control the data assimilation or optimization
    algorithm. It is defined as a "*Dict*" type object, that is, given as a
    script. See below the list of algorithms and associated parameters in the
    following subsection `Optional and required commands for checking
    algorithms`_.

**CheckingPoint**
    *Required command*. This indicates the vector used, previously noted as
    :math:`\mathbf{x}^b`. It is defined as a "*Vector*" type object.

**Debug**
    *Optional command*. This define the level of trace and intermediary debug
    information. The choices are limited between 0 (for False) and 1 (for
    True).

**ObservationOperator**
    *Required command*. This indicates the observation operator, previously
    noted :math:`H`, which transforms the input parameters :math:`\mathbf{x}` to
    results :math:`\mathbf{y}` to be compared to observations
    :math:`\mathbf{y}^o`. It is defined as a "*Function*" type object. Different
    functional forms can be used, as described in the following subsection
    `Requirements for functions describing an operator`_. If there is some
    control :math:`U` included in the observation, the operator has to be
    applied to a pair :math:`(X,U)`.

**Study_name**
    *Required command*. This is an open string to describe the study by a name
    or a sentence.

**Study_repertory**
    *Optional command*. If available, this directory is used as base name for
    calculation, and used to find all the script files, given by name without
    path, that can be used to define some other commands by scripts.

**UserDataInit**
    *Optional command*. This commands allows to initialize some parameters or
    data automatically before data assimilation algorithm processing.

Optional and required commands for checking algorithms
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: AdjointTest
.. index:: single: FunctionTest
.. index:: single: GradientTest
.. index:: single: LinearityTest

.. index:: single: AlgorithmParameters
.. index:: single: AmplitudeOfInitialDirection
.. index:: single: EpsilonMinimumExponent
.. index:: single: InitialDirection
.. index:: single: ResiduFormula
.. index:: single: SetSeed

We recall that each algorithm can be controlled using some generic or specific
options, given through the "*AlgorithmParameters*" optional command, as follows
for example::

    AlgorithmParameters = {
        "AmplitudeOfInitialDirection" : 1,
        "EpsilonMinimumExponent" : -8,
        }

If an option is specified by the user for an algorithm that doesn't support it,
the option is simply left unused and don't stop the treatment. The meaning of
the acronyms or particular names can be found in the :ref:`genindex` or the
:ref:`section_glossary`. In addition, for each algorithm, the required
commands/keywords are given, being described in `List of commands and keywords
for an ADAO checking case`_.

**"AdjointTest"**

  *Required commands*
    *"CheckingPoint",
    "ObservationOperator"*

  AmplitudeOfInitialDirection
    This key indicates the scaling of the initial perturbation build as a vector
    used for the directional derivative around the nominal checking point. The
    default is 1, that means no scaling.

  EpsilonMinimumExponent
    This key indicates the minimal exponent value of the power of 10 coefficient
    to be used to decrease the increment multiplier. The default is -8, and it
    has to be between 0 and -20. For example, its default value leads to
    calculate the residue of the formula with a fixed increment multiplied from
    1.e0 to 1.e-8.

  InitialDirection
    This key indicates the vector direction used for the directional derivative
    around the nominal checking point. It has to be a vector. If not specified,
    this direction defaults to a random perturbation around zero of the same
    vector size than the checking point.

  SetSeed
    This key allow to give an integer in order to fix the seed of the random
    generator used to generate the ensemble. A convenient value is for example
    1000. By default, the seed is left uninitialized, and so use the default
    initialization from the computer.

**"FunctionTest"**

  *Required commands*
    *"CheckingPoint",
    "ObservationOperator"*

  NumberOfPrintedDigits
    This key indicates the number of digits of precision for floating point
    printed output. The default is 5, with a minimum of 0.

  NumberOfRepetition
    This key indicates the number of time to repeat the function evaluation. The
    default is 1.
  
  SetDebug
    This key requires the activation, or not, of the debug mode during the
    function evaluation. The default is "True", the choices are "True" or
    "False".

**"GradientTest"**

  *Required commands*
    *"CheckingPoint",
    "ObservationOperator"*

  AmplitudeOfInitialDirection
    This key indicates the scaling of the initial perturbation build as a vector
    used for the directional derivative around the nominal checking point. The
    default is 1, that means no scaling.

  EpsilonMinimumExponent
    This key indicates the minimal exponent value of the power of 10 coefficient
    to be used to decrease the increment multiplier. The default is -8, and it
    has to be between 0 and -20. For example, its default value leads to
    calculate the residue of the scalar product formula with a fixed increment
    multiplied from 1.e0 to 1.e-8.

  InitialDirection
    This key indicates the vector direction used for the directional derivative
    around the nominal checking point. It has to be a vector. If not specified,
    this direction defaults to a random perturbation around zero of the same
    vector size than the checking point.

  ResiduFormula
    This key indicates the residue formula that has to be used for the test. The
    default choice is "Taylor", and the possible ones are "Taylor" (residue of
    the Taylor development of the operator, which has to decrease with the
    square power of the perturbation) and "Norm" (residue obtained by taking the
    norm of the Taylor development at zero order approximation, which
    approximate the gradient, and which has to remain constant).
  
  SetSeed
    This key allow to give an integer in order to fix the seed of the random
    generator used to generate the ensemble. A convenient value is for example
    1000. By default, the seed is left uninitialized, and so use the default
    initialization from the computer.

**"LinearityTest"**

  *Required commands*
    *"CheckingPoint",
    "ObservationOperator"*

  AmplitudeOfInitialDirection
    This key indicates the scaling of the initial perturbation build as a vector
    used for the directional derivative around the nominal checking point. The
    default is 1, that means no scaling.

  EpsilonMinimumExponent
    This key indicates the minimal exponent value of the power of 10 coefficient
    to be used to decrease the increment multiplier. The default is -8, and it
    has to be between 0 and -20. For example, its default value leads to
    calculate the residue of the scalar product formula with a fixed increment
    multiplied from 1.e0 to 1.e-8.

  InitialDirection
    This key indicates the vector direction used for the directional derivative
    around the nominal checking point. It has to be a vector. If not specified,
    this direction defaults to a random perturbation around zero of the same
    vector size than the checking point.

  ResiduFormula
    This key indicates the residue formula that has to be used for the test. The
    default choice is "CenteredDL", and the possible ones are "CenteredDL"
    (residue of the difference between the function at nominal point and the
    values with positive and negative increments, which has to stay very small),
    "Taylor" (residue of the Taylor development of the operator normalized by
    the nominal value, which has to stay very small), "NominalTaylor" (residue
    of the order 1 approximations of the operator, normalized to the nominal
    point, which has to stay close to 1), and "NominalTaylorRMS" (residue of the
    order 1 approximations of the operator, normalized by RMS to the nominal
    point, which has to stay close to 0).
  
  SetSeed
    This key allow to give an integer in order to fix the seed of the random
    generator used to generate the ensemble. A convenient value is for example
    1000. By default, the seed is left uninitialized, and so use the default
    initialization from the computer.

Requirements for functions describing an operator
-------------------------------------------------

The operators for observation and evolution are required to implement the data
assimilation or optimization procedures. They include the physical simulation by
numerical calculations, but also the filtering and restriction to compare the
simulation to observation. The evolution operator is considered here in its
incremental form, representing the transition between two successive states, and
is then similar to the observation operator.

Schematically, an operator has to give a output solution given the input
parameters. Part of the input parameters can be modified during the optimization
procedure. So the mathematical representation of such a process is a function.
It was briefly described in the section :ref:`section_theory` and is generalized
here by the relation:

.. math:: \mathbf{y} = O( \mathbf{x} )

between the pseudo-observations :math:`\mathbf{y}` and the parameters
:math:`\mathbf{x}` using the observation or evolution operator :math:`O`. The
same functional representation can be used for the linear tangent model
:math:`\mathbf{O}` of :math:`O` and its adjoint :math:`\mathbf{O}^*`, also
required by some data assimilation or optimization algorithms.

On input and output of these operators, the :math:`\mathbf{x}` and
:math:`\mathbf{y}` variables or their increments are mathematically vectors,
and they are given as non-orented vectors (of type list or Numpy array) or
oriented ones (of type Numpy matrix).

Then, **to describe completely an operator, the user has only to provide a
function that fully and only realize the functional operation**.

This function is usually given as a script that can be executed in a YACS node.
This script can without difference launch external codes or use internal SALOME
calls and methods. If the algorithm requires the 3 aspects of the operator
(direct form, tangent form and adjoint form), the user has to give the 3
functions or to approximate them.

There are 3 practical methods for the user to provide an operator functional
representation. These methods are chosen in the "*FROM*"  field of each operator
having a "*Function*" value as "*INPUT_TYPE*", as shown by the following figure:

  .. eficas_operator_function:
  .. image:: images/eficas_operator_function.png
    :align: center
    :width: 100%
  .. centered::
    **Choosing an operator functional representation**

First functional form: using "*ScriptWithOneFunction*"
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithOneFunction
.. index:: single: DirectOperator
.. index:: single: DifferentialIncrement
.. index:: single: CenteredFiniteDifference

The first one consist in providing only one potentially non-linear function, and
to approximate the tangent and the adjoint operators. This is done by using the
keyword "*ScriptWithOneFunction*" for the description of the chosen operator in
the ADAO GUI. The user have to provide the function in a script, with a
mandatory name "*DirectOperator*". For example, the script can follow the
template::

    def DirectOperator( X ):
        """ Direct non-linear simulation operator """
        ...
        ...
        ...
        return Y=O(X)

In this case, the user has also provide a value for the differential increment
(or keep the devault value), using through the GUI the keyword
"*DifferentialIncrement*", which has a default value of 1%. This coefficient
will be used in the finite difference approximation to build the tangent and
adjoint operators. The finite difference approximation order can also be chosen
through the GUI, using the keyword "*CenteredFiniteDifference*", with 0 for an
uncentered schema of first order (which is the default value), and with 1 for a
centered schema of second order (of twice the first order computational cost).

This first operator definition form allows easily to test the functional form
before its use in an ADAO case, greatly reducing the complexity of
operator implementation.

**Important warning:** the name "*DirectOperator*" is mandatory, and the type of
the ``X`` argument can be either a list, a numpy array or a numpy 1D-matrix. The
user has to treat these cases in his function.

Second functional form: using "*ScriptWithFunctions*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithFunctions
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

**In general, it is recommended to use the first functionnal form rather than
the second one. A small performance improvement is not a good reason to use a
detailled implementation as this second functional form.**

The second one consist in providing directly the three associated operators
:math:`O`, :math:`\mathbf{O}` and :math:`\mathbf{O}^*`. This is done by using
the keyword "*ScriptWithFunctions*" for the description of the chosen operator
in the ADAO GUI. The user have to provide three functions in one script, with
three mandatory names "*DirectOperator*", "*TangentOperator*" and
"*AdjointOperator*". For example, the script can follow the template::

    def DirectOperator( X ):
        """ Direct non-linear simulation operator """
        ...
        ...
        ...
        return something like Y

    def TangentOperator( (X, dX) ):
        """ Tangent linear operator, around X, applied to dX """
        ...
        ...
        ...
        return something like Y

    def AdjointOperator( (X, Y) ):
        """ Adjoint operator, around X, applied to Y """
        ...
        ...
        ...
        return something like X

Another time, this second operator definition allow easily to test the
functional forms before their use in an ADAO case, reducing the complexity of
operator implementation.

For some algorithms, it is required that the tangent and adjoint functions can
return the matrix equivalent to the linear operator. In this case, when
respectivly the ``dX`` or the ``Y`` arguments are ``None``, the user has to
return the associated matrix.

**Important warning:** the names "*DirectOperator*", "*TangentOperator*" and
"*AdjointOperator*" are mandatory, and the type of the ``X``, Y``, ``dX``
arguments can be either a python list, a numpy array or a numpy 1D-matrix. The
user has to treat these cases in his script.

Third functional form: using "*ScriptWithSwitch*"
+++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithSwitch
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

**It is recommended not to use this third functional form without a solid
numerical or physical reason. A performance improvement is not a good reason to
use the implementation complexity of this third functional form. Only an
inability to use the first or second forms justifies the use of the third.**

This third form give more possibilities to control the execution of the three
functions representing the operator, allowing advanced usage and control over
each execution of the simulation code. This is done by using the keyword
"*ScriptWithSwitch*" for the description of the chosen operator in the ADAO GUI.
The user have to provide a switch in one script to control the execution of the 
direct, tangent and adjoint forms of its simulation code. The user can then, for
example, use other approximations for the tangent and adjoint codes, or
introduce more complexity in the argument treatment of the functions. But it
will be far more complicated to implement and debug.

If, however, you want to use this third form, we recommend using the following
template for the switch. It requires an external script or code named here
"*Physical_simulation_functions.py*", containing three functions named
"*DirectOperator*", "*TangentOperator*" and "*AdjointOperator*" as previously.
Here is the switch template::

    import Physical_simulation_functions
    import numpy, logging
    #
    method = ""
    for param in computation["specificParameters"]:
        if param["name"] == "method":
            method = param["value"]
    if method not in ["Direct", "Tangent", "Adjoint"]:
        raise ValueError("No valid computation method is given")
    logging.info("Found method is \'%s\'"%method)
    #
    logging.info("Loading operator functions")
    Function = Physical_simulation_functions.DirectOperator
    Tangent  = Physical_simulation_functions.TangentOperator
    Adjoint  = Physical_simulation_functions.AdjointOperator
    #
    logging.info("Executing the possible computations")
    data = []
    if method == "Direct":
        logging.info("Direct computation")
        Xcurrent = computation["inputValues"][0][0][0]
        data = Function(numpy.matrix( Xcurrent ).T)
    if method == "Tangent":
        logging.info("Tangent computation")
        Xcurrent  = computation["inputValues"][0][0][0]
        dXcurrent = computation["inputValues"][0][0][1]
        data = Tangent(numpy.matrix(Xcurrent).T, numpy.matrix(dXcurrent).T)
    if method == "Adjoint":
        logging.info("Adjoint computation")
        Xcurrent = computation["inputValues"][0][0][0]
        Ycurrent = computation["inputValues"][0][0][1]
        data = Adjoint((numpy.matrix(Xcurrent).T, numpy.matrix(Ycurrent).T))
    #
    logging.info("Formatting the output")
    it = numpy.ravel(data)
    outputValues = [[[[]]]]
    for val in it:
      outputValues[0][0][0].append(val)
    #
    result = {}
    result["outputValues"]        = outputValues
    result["specificOutputInfos"] = []
    result["returnCode"]          = 0
    result["errorMessage"]        = ""

All various modifications could be done from this template hypothesis.

Special case of controled evolution or observation operator
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

In some cases, the evolution or the observation operator is required to be
controled by an external input control, given *a priori*. In this case, the
generic form of the incremental model is slightly modified as follows:

.. math:: \mathbf{y} = O( \mathbf{x}, \mathbf{u})

where :math:`\mathbf{u}` is the control over one state increment. In this case,
the direct operator has to be applied to a pair of variables :math:`(X,U)`.
Schematically, the operator has to be set as::

    def DirectOperator( (X, U) ):
        """ Direct non-linear simulation operator """
        ...
        ...
        ...
        return something like X(n+1) (evolution) or Y(n+1) (observation)

The tangent and adjoint operators have the same signature as previously, noting
that the derivatives has to be done only partially against :math:`\mathbf{x}`.
In such a case with explicit control, only the second functional form (using
"*ScriptWithFunctions*") and third functional form (using "*ScriptWithSwitch*")
can be used.

Requirements to describe covariance matrices
--------------------------------------------

Multiple covariance matrices are required to implement the data assimilation or
optimization procedures. The main ones are the background error covariance
matrix, noted as :math:`\mathbf{B}`, and the observation error covariance matrix,
noted as :math:`\mathbf{R}`. Such a matrix is required to be a squared symetric
semi-definite positive matrix.

There are 3 practical methods for the user to provide a covariance matrix. These
methods are chosen by the "*INPUT_TYPE*" keyword of each defined covariance
matrix, as shown by the following figure:

  .. eficas_covariance_matrix:
  .. image:: images/eficas_covariance_matrix.png
    :align: center
    :width: 100%
  .. centered::
    **Choosing covariance matrix representation**

First matrix form: using "*Matrix*" representation
++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Matrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

This first form is the default and more general one. The covariance matrix
:math:`\mathbf{M}` has to be fully specified. Even if the matrix is symetric by
nature, the entire :math:`\mathbf{M}` matrix has to be given.

.. math:: \mathbf{M} =  \begin{pmatrix}
    m_{11} & m_{12} & \cdots   & m_{1n} \\
    m_{21} & m_{22} & \cdots   & m_{2n} \\
    \vdots & \vdots & \vdots   & \vdots \\
    m_{n1} & \cdots & m_{nn-1} & m_{nn}
    \end{pmatrix}

It can be either a Python Numpy array or a matrix, or a list of lists of values
(that is, a list of rows). For example, a simple diagonal unitary background
error covariance matrix :math:`\mathbf{B}` can be described in a Python script
file as::

    BackgroundError = [[1, 0 ... 0], [0, 1 ... 0] ... [0, 0 ... 1]]

or::

    BackgroundError = numpy.eye(...)

Second matrix form: using "*ScalarSparseMatrix*" representation
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScalarSparseMatrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

On the opposite, this second form is a very simplified method to provide a
matrix. The covariance matrix :math:`\mathbf{M}` is supposed to be a positive
multiple of the identity matrix. This matrix can then be specified in a unique
way by the multiplier :math:`m`:

.. math:: \mathbf{M} =  m \times \begin{pmatrix}
    1       & 0      & \cdots   & 0      \\
    0       & 1      & \cdots   & 0      \\
    \vdots  & \vdots & \vdots   & \vdots \\
    0       & \cdots & 0        & 1
    \end{pmatrix}

The multiplier :math:`m` has to be a floating point or integer positive value
(if it is negative, which is impossible for a positive covariance matrix, it is
converted to positive value). For example, a simple diagonal unitary background
error covariance matrix :math:`\mathbf{B}` can be described in a python script
file as::

    BackgroundError = 1.

or, better, by a "*String*" directly in the ADAO case.

Third matrix form: using "*DiagonalSparseMatrix*" representation
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: DiagonalSparseMatrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

This third form is also a simplified method to provide a matrix, but a little
more powerful than the second one. The covariance matrix :math:`\mathbf{M}` is
already supposed to be diagonal, but the user has to specify all the positive
diagonal values. The matrix can then be specified only by a vector
:math:`\mathbf{V}` which will be set on a diagonal matrix:

.. math:: \mathbf{M} =  \begin{pmatrix}
    v_{1}  & 0      & \cdots   & 0      \\
    0      & v_{2}  & \cdots   & 0      \\
    \vdots & \vdots & \vdots   & \vdots \\
    0      & \cdots & 0        & v_{n}
    \end{pmatrix}

It can be either a Python Numpy array or a matrix, or a list or a list of list
of positive values (in all cases, if some are negative, which is impossible,
they are converted to positive values). For example, a simple diagonal unitary
background error covariance matrix :math:`\mathbf{B}` can be described in a
python script file as::

    BackgroundError = [1, 1 ... 1]

or::

    BackgroundError = numpy.ones(...)
