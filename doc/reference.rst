.. _section_reference:

================================================================================
Reference description of the ADAO commands and keywords
================================================================================


This section presents the reference description of the commands and keywords
available through the GUI or through scripts.

Each command or keyword to be defined through the ADAO GUI has some properties.
The first property is to be a required command, an optional command or a keyword
describing a type of input. The second property is to be an "open" variable with
a fixed type but with any value allowed by the type, or a "restricted" variable,
limited to some specified values. The mathematical notations used afterwards are
explained in the section :ref:`section_theory`.

List of possible input types
++++++++++++++++++++++++++++

.. index:: single: Dict
.. index:: single: Function
.. index:: single: Matrix
.. index:: single: String
.. index:: single: Script
.. index:: single: Vector

The different type-style commands are:

:Dict:
    *Type of an input*. This indicates a variable that has to be filled by a
    dictionary, usually given as a script.

:Function:
    *Type of an input*. This indicates a variable that has to be filled by a
    function, usually given as a script.

:Matrix:
    *Type of an input*. This indicates a variable that has to be filled by a
    matrix, usually given either as a string or as a script.

:String:
    *Type of an input*. This indicates a string, such as a name or a literal
    representation of a matrix or vector, such as "1 2 ; 3 4".

:Script:
    *Type of an input*. This indicates a script given as an external file.

:Vector:
    *Type of an input*. This indicates a variable that has to be filled by a
    vector, usually given either as a string or as a script.
    
List of commands
++++++++++++++++

.. index:: single: ASSIMILATION_STUDY
.. index:: single: Algorithm
.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Debug
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

The different commands are the following:

:ASSIMILATION_STUDY:
    *Required command*. This is the general command describing an ADAO case. It
    hierarchicaly contains all the other commands.

:Algorithm:
    *Required command*. This is a string to indicates the data assimilation
    algorithm chosen. The choices are limited and available through the GUI.
    There exists for example: "3DVAR", "Blue"... See below the list of
    algorithms and associated parameters.

:AlgorithmParameters:
    *Optional command*. This command allows to add some optional parameters to
    control the data assimilation algorithm calculation. It is defined as a
    "*Dict*" type object.  See below the list of algorithms and associated
    parameters.

:Background:
    *Required command*. This indicates the backgroud vector used for data
    assimilation, previously noted as :math:`\mathbf{x}^b`. It is defined as a
    "*Vector*" type object, that is, given either as a string or as a script.

:BackgroundError:
    *Required command*. This indicates the backgroud error covariance matrix,
    previously noted as :math:`\mathbf{B}`.It is defined as a "*Matrix*" type
    object, that is, given either as a string or as a script.

:Debug:
    *Required command*. This let choose the level of trace and intermediary
    debug informations. The choices are limited between 0 (for False) and 1 (for
    True) and available through the GUI.

:InputVariables:
    *Optional command*. This command allows to indicates the name and size of
    physical variables that are bundled together in the control vector. This
    information is dedicated to data processed inside of data assimilation
    algorithm.

:Observation:
    *Required command*. This indicates the observation vector used for data
    assimilation, previously noted as :math:`\mathbf{y}^o`. It is defined as a
    "*Vector*" type object, that is, given either as a string or as a script.

:ObservationError:
    *Required command*. This indicates the observation error covariance matrix,
    previously noted as :math:`\mathbf{R}`.It is defined as a "*Matrix*" type
    object, that is, given either as a string or as a script.

:ObservationOperator:
    *Required command*. This indicates the observation operator, previously
    noted :math:`H`, which transforms the input parameters :math:`\mathbf{x}`
    to results :math:`\mathbf{y}` to be compared to observations
    :math:`\mathbf{y}^o`.

:Observers:
    *Optional command*. This command allows to set internal observers, that are
    functions linked with a particular variable, which will be executed each
    time this variable is modified. It is a convenient way to monitor interest
    variables during the data assimilation process, by printing or plotting it,
    etc.

:OutputVariables:
    *Optional command*. This command allows to indicates the name and size of
    physical variables that are bundled together in the output observation
    vector. This information is dedicated to data processed inside of data
    assimilation algorithm.

:Study_name:
    *Required command*. This is an open string to describe the study by a name
    or a sentence.

:Study_repertory:
    *Optional command*. If available, this repertory is used to find all the
    script files that can be used to define some other commands by scripts.

:UserDataInit:
    *Optional command*. This commands allows to initialise some parameters or
    data automatically before data assimilation algorithm processing.

:UserPostAnalysis:
    *Optional command*. This commands allows to process some parameters or data
    automatically after data assimilation algorithm processing. It is defined as
    a script or a string, allowing to put simple code directly inside the ADAO
    case.

.. _subsection_algo_options:

List of possible options for the algorithms
+++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Blue
.. index:: single: LinearLeastSquares
.. index:: single: 3DVAR
.. index:: single: NonLinearLeastSquares
.. index:: single: EnsembleBlue
.. index:: single: QuantileRegression

.. index:: single: AlgorithmParameters
.. index:: single: Minimizer
.. index:: single: Bounds
.. index:: single: MaximumNumberOfSteps
.. index:: single: CalculateAPosterioriCovariance
.. index:: single: CostDecrementTolerance
.. index:: single: ProjectedGradientTolerance
.. index:: single: GradientNormTolerance
.. index:: single: SetSeed
.. index:: single: Quantile

Each algorithm can be controled using some generic or specific options given
throught the "*AlgorithmParameters*" optional command, as follows::

    AlgorithmParameters = {
        "Minimizer" : "CG",
        "MaximumNumberOfSteps" : 10,
        }

This section describes the available options by algorithm. If an option is
specified for an algorithm that doesn't support it, the option is simply left
unused.

:"Blue":

    :CalculateAPosterioriCovariance:
      This boolean key allows to enable the calculation and the storage of the
      covariance matrix of a posteriori anlysis errors. Be careful, this is a
      numericaly costly step. The default is "False".

:"LinearLeastSquares":
    no option

:"3DVAR":

    :Minimizer:
      This key allows to choose the optimization minimizer. The default choice
      is "LBFGSB", and the possible ones are "LBFGSB" (nonlinear constrained
      minimizer, see [Byrd95]_ and [Zhu97]_), "TNC" (nonlinear constrained
      minimizer), "CG" (nonlinear unconstrained minimizer), "BFGS" (nonlinear
      unconstrained minimizer), "NCG" (Newton CG minimizer).

    :Bounds:
      This key allows to define upper and lower bounds for every control
      variable being optimized. Bounds can be given by a list of list of pairs
      of lower/upper bounds for each variable, with possibly ``None`` every time
      there is no bound. The bounds can always be specified, but they are taken
      into account only by the constrained minimizers.

    :MaximumNumberOfSteps:
      This key indicates the maximum number of iterations allowed for iterative
      optimization. The default is 15000, which very similar to no limit on
      iterations. It is then recommended to adapt this parameter to the needs on
      real problems. For some minimizers, the effective stopping step can be
      slightly different due to algorihtm internal control requirements.

    :CalculateAPosterioriCovariance:
      This boolean key allows to enable the calculation and the storage of the
      covariance matrix of a posteriori anlysis errors. Be careful, this is a
      numericaly costly step. The default is "False".

    :CostDecrementTolerance:
      This key indicates a limit value, leading to stop successfully the
      iterative optimization process when the cost function decreases less than
      this tolerance at the last step. The default is 10e-7, and it is
      recommended to adapt it the needs on real problems.

    :ProjectedGradientTolerance:
      This key indicates a limit value, leading to stop successfully the
      iterative optimization process when all the components of the projected
      gradient are under this limit. It is only used for constrained algorithms.
      The default is -1, that is the internal default of each algorithm, and it
      is not recommended to change it.

    :GradientNormTolerance:
      This key indicates a limit value, leading to stop successfully the
      iterative optimization process when the norm of the gradient is under this
      limit. It is only used for non-constrained algorithms.  The default is
      10e-5 and it is not recommended to change it.

:"NonLinearLeastSquares":

    :Minimizer:
      This key allows to choose the optimization minimizer. The default choice
      is "LBFGSB", and the possible ones are "LBFGSB" (nonlinear constrained
      minimizer, see [Byrd95]_ and [Zhu97]_), "TNC" (nonlinear constrained
      minimizer), "CG" (nonlinear unconstrained minimizer), "BFGS" (nonlinear
      unconstrained minimizer), "NCG" (Newton CG minimizer).

    :Bounds:
      This key allows to define upper and lower bounds for every control
      variable being optimized. Bounds can be given by a list of list of pairs
      of lower/upper bounds for each variable, with possibly ``None`` every time
      there is no bound. The bounds can always be specified, but they are taken
      into account only by the constrained minimizers.

    :MaximumNumberOfSteps:
      This key indicates the maximum number of iterations allowed for iterative
      optimization. The default is 15000, which very similar to no limit on
      iterations. It is then recommended to adapt this parameter to the needs on
      real problems. For some minimizers, the effective stopping step can be
      slightly different due to algorihtm internal control requirements.

    :CostDecrementTolerance:
      This key indicates a limit value, leading to stop successfully the
      iterative optimization process when the cost function decreases less than
      this tolerance at the last step. The default is 10e-7, and it is
      recommended to adapt it the needs on real problems.

    :ProjectedGradientTolerance:
      This key indicates a limit value, leading to stop successfully the
      iterative optimization process when all the components of the projected
      gradient are under this limit. It is only used for constrained algorithms.
      The default is -1, that is the internal default of each algorithm, and it
      is not recommended to change it.

    :GradientNormTolerance:
      This key indicates a limit value, leading to stop successfully the
      iterative optimization process when the norm of the gradient is under this
      limit. It is only used for non-constrained algorithms.  The default is
      10e-5 and it is not recommended to change it.

:"EnsembleBlue":

    :SetSeed:
      This key allow to give an integer in order to fix the seed of the random
      generator used to generate the ensemble. A convenient value is for example
      1000. By default, the seed is left uninitialized, and so use the default
      initialization from the computer.

:"QuantileRegression":

    :Quantile:
      This key allows to define the real value of the desired quantile, between
      0 and 1. The default is 0.5, corresponding to the median.

    :Minimizer:
      This key allows to choose the optimization minimizer. The default choice
      and only available choice is "MMQR" (Majorize-Minimize for Quantile
      Regression).

    :MaximumNumberOfSteps:
      This key indicates the maximum number of iterations allowed for iterative
      optimization. The default is 15000, which very similar to no limit on
      iterations. It is then recommended to adapt this parameter to the needs on
      real problems.

    :CostDecrementTolerance:
      This key indicates a limit value, leading to stop successfully the
      iterative optimization process when the cost function or the surrogate
      decreases less than this tolerance at the last step. The default is 10e-6,
      and it is recommended to adapt it the needs on real problems.

Examples of using these commands are available in the section
:ref:`section_examples` and in example files installed with ADAO module.
