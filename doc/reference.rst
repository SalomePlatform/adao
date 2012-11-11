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
.. index:: single: String
.. index:: single: Script
.. index:: single: Vector

Each ADAO variable has a pseudo-type to help filling it and validation. The
different pseudo-types are:

**Dict**
    This indicates a variable that has to be filled by a dictionary, usually
    given as a script.

**Function**
    This indicates a variable that has to be filled by a function, usually given
    as a script or a component method.

**Matrix**
    This indicates a variable that has to be filled by a matrix, usually given
    either as a string or as a script.

**String**
    This indicates a string giving a literal representation of a matrix, a
    vector or a vector serie, such as "1 2 ; 3 4" for a square 2x2 matrix.

**Script**
    This indicates a script given as an external file. It can be described by a
    full absolute path name or only by the file name without path.

**Vector**
    This indicates a variable that has to be filled by a vector, usually given
    either as a string or as a script.

**VectorSerie** This indicates a variable that has to be filled by a list of
    vectors, usually given either as a string or as a script.

When a command or keyword can be filled by a script file name, the script has to
contain a variable or a method that has the same name as the one to be filled.
In other words, when importing the script in a YACS Python node, it must create
a variable of the good name in the current namespace.

List of commands and keywords for an ADAO calculation case
----------------------------------------------------------

.. index:: single: ASSIMILATION_STUDY
.. index:: single: Algorithm
.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
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
    algorithms and associated parameters in the following subsection `Options
    for algorithms`_.

**AlgorithmParameters**
    *Optional command*. This command allows to add some optional parameters to
    control the data assimilation or optimization algorithm. It is defined as a
    "*Dict*" type object, that is, given as a script. See below the list of
    algorithms and associated parameters in the following subsection `Options
    for algorithms`_.

**Background**
    *Required command*. This indicates the background or initial vector used,
    previously noted as :math:`\mathbf{x}^b`. It is defined as a "*Vector*" type
    object, that is, given either as a string or as a script.

**BackgroundError**
    *Required command*. This indicates the background error covariance matrix,
    previously noted as :math:`\mathbf{B}`. It is defined as a "*Matrix*" type
    object, that is, given either as a string or as a script.

**Debug**
    *Required command*. This define the level of trace and intermediary debug
    information. The choices are limited between 0 (for False) and 1 (for
    True).

**EvolutionError**
    *Optional command*. This indicates the evolution error covariance matrix,
    usually noted as :math:`\mathbf{Q}`. It is defined as a "*Matrix*" type
    object, that is, given either as a string or as a script.

**EvolutionModel**
    *Optional command*. This indicates the evolution model operator, usually
    noted :math:`M`, which describes a step of evolution. It is defined as a
    "*Function*" type object, that is, given as a script. Different functional
    forms can be used, as described in the following subsection `Requirements
    for functions describing an operator`_.

**InputVariables**
    *Optional command*. This command allows to indicates the name and size of
    physical variables that are bundled together in the control vector. This
    information is dedicated to data processed inside an algorithm.

**Observation**
    *Required command*. This indicates the observation vector used for data
    assimilation or optimization, previously noted as :math:`\mathbf{y}^o`. It
    is defined as a "*Vector*" type object, that is, given either as a string or
    as a script.

**ObservationError**
    *Required command*. This indicates the observation error covariance matrix,
    previously noted as :math:`\mathbf{R}`. It is defined as a "*Matrix*" type
    object, that is, given either as a string or as a script.

**ObservationOperator**
    *Required command*. This indicates the observation operator, previously
    noted :math:`H`, which transforms the input parameters :math:`\mathbf{x}` to
    results :math:`\mathbf{y}` to be compared to observations
    :math:`\mathbf{y}^o`. It is defined as a "*Function*" type object, that is,
    given as a script. Different functional forms can be used, as described in
    the following subsection `Requirements for functions describing an
    operator`_.

**Observers**
    *Optional command*. This command allows to set internal observers, that are
    functions linked with a particular variable, which will be executed each
    time this variable is modified. It is a convenient way to monitor interest
    variables during the data assimilation or optimization process, by printing
    or plotting it, etc.

**OutputVariables**
    *Optional command*. This command allows to indicates the name and size of
    physical variables that are bundled together in the output observation
    vector. This information is dedicated to data processed inside an algorithm.

**Study_name**
    *Required command*. This is an open string to describe the study by a name
    or a sentence.

**Study_repertory**
    *Optional command*. If available, this repertory is used to find all the
    script files that can be used to define some other commands by scripts.

**UserDataInit**
    *Optional command*. This commands allows to initialize some parameters or
    data automatically before data assimilation algorithm processing.

**UserPostAnalysis**
    *Optional command*. This commands allows to process some parameters or data
    automatically after data assimilation algorithm processing. It is defined as
    a script or a string, allowing to put post-processing code directly inside
    the ADAO case.

List of commands and keywords for an ADAO checking case
-------------------------------------------------------

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
    *Required command*. This is a string to indicate the data assimilation or
    optimization algorithm chosen. The choices are limited and available through
    the GUI. There exists for example "3DVAR", "Blue"... See below the list of
    algorithms and associated parameters in the following subsection `Options
    for algorithms`_.

**AlgorithmParameters**
    *Optional command*. This command allows to add some optional parameters to
    control the data assimilation or optimization algorithm. It is defined as a
    "*Dict*" type object, that is, given as a script. See below the list of
    algorithms and associated parameters in the following subsection `Options
    for algorithms`_.

**CheckingPoint**
    *Required command*. This indicates the vector used,
    previously noted as :math:`\mathbf{x}^b`. It is defined as a "*Vector*" type
    object, that is, given either as a string or as a script.

**Debug**
    *Required command*. This define the level of trace and intermediary debug
    information. The choices are limited between 0 (for False) and 1 (for
    True).

**ObservationOperator**
    *Required command*. This indicates the observation operator, previously
    noted :math:`H`, which transforms the input parameters :math:`\mathbf{x}` to
    results :math:`\mathbf{y}` to be compared to observations
    :math:`\mathbf{y}^o`. It is defined as a "*Function*" type object, that is,
    given as a script. Different functional forms can be used, as described in
    the following subsection `Requirements for functions describing an
    operator`_.

**Study_name**
    *Required command*. This is an open string to describe the study by a name
    or a sentence.

**Study_repertory**
    *Optional command*. If available, this repertory is used to find all the
    script files that can be used to define some other commands by scripts.

**UserDataInit**
    *Optional command*. This commands allows to initialize some parameters or
    data automatically before data assimilation algorithm processing.

Options for algorithms
----------------------

.. index:: single: 3DVAR
.. index:: single: Blue
.. index:: single: EnsembleBlue
.. index:: single: KalmanFilter
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

Each algorithm can be controlled using some generic or specific options given
through the "*AlgorithmParameters*" optional command, as follows for example::

    AlgorithmParameters = {
        "Minimizer" : "LBFGSB",
        "MaximumNumberOfSteps" : 25,
        "StoreSupplementaryCalculations" : ["APosterioriCovariance","OMA"],
        }

This section describes the available options algorithm by algorithm. If an
option is specified for an algorithm that doesn't support it, the option is
simply left unused. The meaning of the acronyms or particular names can be found
in the :ref:`genindex` or the :ref:`section_glossary`.

**"Blue"**

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations. The default is a void list, none of these variables being
    calculated and stored by default. The possible names are in the following
    list: ["APosterioriCovariance", "BMA", "OMA", "OMB", "Innovation",
    "SigmaBck2", "SigmaObs2", "MahalanobisConsistency"].

**"LinearLeastSquares"**

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations. The default is a void list, none of these variables being
    calculated and stored by default. The possible names are in the following
    list: ["OMA"].

**"3DVAR"**

  Minimizer
    This key allows to choose the optimization minimizer. The default choice
    is "LBFGSB", and the possible ones are "LBFGSB" (nonlinear constrained
    minimizer, see [Byrd95]_ and [Zhu97]_), "TNC" (nonlinear constrained
    minimizer), "CG" (nonlinear unconstrained minimizer), "BFGS" (nonlinear
    unconstrained minimizer), "NCG" (Newton CG minimizer).

  Bounds
    This key allows to define upper and lower bounds for every control
    variable being optimized. Bounds can be given by a list of list of pairs
    of lower/upper bounds for each variable, with possibly ``None`` every time
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
    this tolerance at the last step. The default is 10e-7, and it is
    recommended to adapt it the needs on real problems.

  ProjectedGradientTolerance
    This key indicates a limit value, leading to stop successfully the
    iterative optimization process when all the components of the projected
    gradient are under this limit. It is only used for constrained algorithms.
    The default is -1, that is the internal default of each algorithm, and it
    is not recommended to change it.

  GradientNormTolerance
    This key indicates a limit value, leading to stop successfully the
    iterative optimization process when the norm of the gradient is under this
    limit. It is only used for non-constrained algorithms.  The default is
    10e-5 and it is not recommended to change it.

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

  Minimizer
    This key allows to choose the optimization minimizer. The default choice
    is "LBFGSB", and the possible ones are "LBFGSB" (nonlinear constrained
    minimizer, see [Byrd95]_ and [Zhu97]_), "TNC" (nonlinear constrained
    minimizer), "CG" (nonlinear unconstrained minimizer), "BFGS" (nonlinear
    unconstrained minimizer), "NCG" (Newton CG minimizer).

  Bounds
    This key allows to define upper and lower bounds for every control
    variable being optimized. Bounds can be given by a list of list of pairs
    of lower/upper bounds for each variable, with possibly ``None`` every time
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
    this tolerance at the last step. The default is 10e-7, and it is
    recommended to adapt it the needs on real problems.

  ProjectedGradientTolerance
    This key indicates a limit value, leading to stop successfully the
    iterative optimization process when all the components of the projected
    gradient are under this limit. It is only used for constrained algorithms.
    The default is -1, that is the internal default of each algorithm, and it
    is not recommended to change it.

  GradientNormTolerance
    This key indicates a limit value, leading to stop successfully the
    iterative optimization process when the norm of the gradient is under this
    limit. It is only used for non-constrained algorithms.  The default is
    10e-5 and it is not recommended to change it.

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

  SetSeed
    This key allow to give an integer in order to fix the seed of the random
    generator used to generate the ensemble. A convenient value is for example
    1000. By default, the seed is left uninitialized, and so use the default
    initialization from the computer.

**"KalmanFilter"**

  StoreSupplementaryCalculations
     This list indicates the names of the supplementary variables that can be
     available at the end of the algorithm. It involves potentially costly
     calculations. The default is a void list, none of these variables being
     calculated and stored by default. The possible names are in the following
     list: ["APosterioriCovariance", "Innovation"].

**"ParticleSwarmOptimization"**

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
    decreases less than this tolerance at the last step. The default is 10e-6,
    and it is recommended to adapt it the needs on real problems.

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

Requirements for functions describing an operator
-------------------------------------------------

The operators for observation and evolution are required to implement the data
assimilation or optimization procedures. They include the physical simulation
numerical simulations, but also the filtering and restriction to compare the
simulation to observation.

Schematically, an operator has to give a output solution given the input
parameters. Part of the input parameters can be modified during the optimization
procedure. So the mathematical representation of such a process is a function.
It was briefly described in the section :ref:`section_theory` and is generalized
here by the relation:

.. math:: \mathbf{y} = H( \mathbf{x} )

between the pseudo-observations :math:`\mathbf{y}` and the parameters
:math:`\mathbf{x}` using the observation operator :math:`H`. The same functional
representation can be used for the linear tangent model :math:`\mathbf{H}` of
:math:`H` and its adjoint :math:`\mathbf{H}^*`, also required by some data
assimilation or optimization algorithms.

Then, **to describe completely an operator, the user has only to provide a
function that fully and only realize the functional operation**.

This function is usually given as a script that can be executed in a YACS node.
This script can without difference launch external codes or use internal SALOME
calls and methods. If the algorithm requires the 3 aspects of the operator
(direct form, tangent form and adjoint form), the user has to give the 3
functions or to approximate them.

There are 3 practical methods for the user to provide the operator functional
representation.

First functional form: using "*ScriptWithOneFunction*"
++++++++++++++++++++++++++++++++++++++++++++++++++++++

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
        return Y=H(X)

In this case, the user can also provide a value for the differential increment,
using through the GUI the keyword "*DifferentialIncrement*", which has a default
value of 1%. This coefficient will be used in the finite difference
approximation to build the tangent and adjoint operators.

This first operator definition allow easily to test the functional form before
its use in an ADAO case, reducing the complexity of implementation.

Second functional form: using "*ScriptWithFunctions*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++

The second one consist in providing directly the three associated operators
:math:`H`, :math:`\mathbf{H}` and :math:`\mathbf{H}^*`. This is done by using the
keyword "*ScriptWithFunctions*" for the description of the chosen operator in
the ADAO GUI. The user have to provide three functions in one script, with three
mandatory names "*DirectOperator*", "*TangentOperator*" and "*AdjointOperator*".
For example, the script can follow the template::

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

Another time, this second perator definition allow easily to test the functional
forms before their use in an ADAO case, greatly reducing the complexity of
implementation.

Third functional form: using "*ScriptWithSwitch*"
+++++++++++++++++++++++++++++++++++++++++++++++++

This third form give more possibilities to control the execution of the three
functions representing the operator, allowing advanced usage and control over
each execution of the simulation code. This is done by using the keyword
"*ScriptWithSwitch*" for the description of the chosen operator in the ADAO GUI.
The user have to provide a switch in one script to control the execution of the 
direct, tangent and adjoint forms of its simulation code. The user can then, for
example, use other approximations for the tangent and adjoint codes, or
introduce more complexity in the argument treatment of the functions. But it
will be far more complicated to implement and debug.

**It is recommended not to use this third functional form without a solid
numerical or physical reason.**

If, however, you want to use this third form, we recommend using the following
template for the switch. It requires an external script or code named
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
    FunctionH = Physical_simulation_functions.DirectOperator
    TangentH  = Physical_simulation_functions.TangentOperator
    AdjointH  = Physical_simulation_functions.AdjointOperator
    #
    logging.info("Executing the possible computations")
    data = []
    if method == "Direct":
        logging.info("Direct computation")
        Xcurrent = computation["inputValues"][0][0][0]
        data = FunctionH(numpy.matrix( Xcurrent ).T)
    if method == "Tangent":
        logging.info("Tangent computation")
        Xcurrent  = computation["inputValues"][0][0][0]
        dXcurrent = computation["inputValues"][0][0][1]
        data = TangentH(numpy.matrix(Xcurrent).T, numpy.matrix(dXcurrent).T)
    if method == "Adjoint":
        logging.info("Adjoint computation")
        Xcurrent = computation["inputValues"][0][0][0]
        Ycurrent = computation["inputValues"][0][0][1]
        data = AdjointH((numpy.matrix(Xcurrent).T, numpy.matrix(Ycurrent).T))
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
