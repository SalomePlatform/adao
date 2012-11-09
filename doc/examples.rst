.. _section_examples:

================================================================================
Tutorials on using the ADAO module
================================================================================

.. |eficas_new| image:: images/eficas_new.png
   :align: middle
   :scale: 50%
.. |eficas_save| image:: images/eficas_save.png
   :align: middle
   :scale: 50%
.. |eficas_yacs| image:: images/eficas_yacs.png
   :align: middle
   :scale: 50%

This section presents some examples on using the ADAO module in SALOME. The
first one shows how to build a simple data assimilation case defining
explicitly all the required data through the GUI. The second one shows, on the
same case, how to define data using external sources through scripts.

Building a simple estimation case with explicit data definition
---------------------------------------------------------------

This simple example is a demonstration one, and describes how to set a BLUE
estimation framework in order to get *weighted least square estimated state* of
a system from an observation of the state and from an *a priori* knowledge (or
background) of this state. In other words, we look for the weighted middle
between the observation and the background vectors. All the numerical values of
this example are arbitrary.

Experimental set up
+++++++++++++++++++

We choose to operate in a 3-dimensional space. 3D is chosen in order to restrict
the size of numerical object to explicitly enter by the user, but the problem is
not dependant of the dimension and can be set in dimension 1000... The
observation :math:`\mathbf{y}^o` is of value 1 in each direction, so:

    ``Yo = [1 1 1]``

The background state :math:`\mathbf{x}^b`, which represent some *a priori*
knowledge or a regularization, is of value of 0 in each direction, which is:

    ``Xb = [0 0 0]``

Data assimilation requires information on errors covariances :math:`\mathbf{R}`
and :math:`\mathbf{B}` respectively for observation and background variables. We
choose here to have uncorrelated errors (that is, diagonal matrices) and to have
the same variance of 1 for all variables (that is, identity matrices). We get:

    ``B = R = [1 0 0 ; 0 1 0 ; 0 0 1]``

Last, we need an observation operator :math:`\mathbf{H}` to convert the
background value in the space of observation value. Here, because the space
dimensions are the same, we can choose the identity  as the observation
operator:

    ``H = [1 0 0 ; 0 1 0 ; 0 0 1]``

With such choices, the Best Linear Unbiased Estimator (BLUE) will be the average
vector between :math:`\mathbf{y}^o` and :math:`\mathbf{x}^b`, named the
*analysis* and denoted by :math:`\mathbf{x}^a`:

    ``Xa = [0.5 0.5 0.5]``

As en extension of this example, one can change the variances for
:math:`\mathbf{B}` or :math:`\mathbf{R}` independently, and the analysis will
move to :math:`\mathbf{y}^o` or to :math:`\mathbf{x}^b` in inverse proportion of
the variances in :math:`\mathbf{B}` and :math:`\mathbf{R}`. It is also
equivalent to search for the analysis thought a BLUE algorithm or a 3DVAR one.

Using the GUI to build the ADAO case
++++++++++++++++++++++++++++++++++++

First, you have to activate the ADAO module by choosing the appropriate module
button or menu of SALOME, and you will see:

  .. _adao_activate2:
  .. image:: images/adao_activate.png
    :align: center
    :width: 100%
  .. centered::
    **Activating the module ADAO in SALOME**

Choose the "*New*" button in this window. You will directly get the EFICAS
interface for variables definition, along with the "*Object browser*". You can
then click on the "*New*" button |eficas_new| to create a new ADAO case, and you
will see:

  .. _adao_viewer:
  .. image:: images/adao_viewer.png
    :align: center
    :width: 100%
  .. centered::
    **The EFICAS viewer for cases definition in module ADAO**

Then fill in the variables to build the ADAO case by using the experimental set
up described above. All the technical information given above will be directly
inserted in the ADAO case definition, by using the *String* type for all the
variables. When the case definition is ready, save it to a "*JDC (\*.comm)*"
native file somewhere in your path. Remember that other files will be also
created near this first one, so it is better to make a specific directory for
your case, and to save the file inside. The name of the file will appear in the
"*Object browser*" window, under the "*ADAO*" menu. The final case definition
looks like this:

  .. _adao_jdcexample01:
  .. image:: images/adao_jdcexample01.png
    :align: center
    :width: 100%
  .. centered::
    **Definition of the experimental set up chosen for the ADAO case**

To go further, we need now to generate the YACS scheme from the ADAO case
definition. In order to do that, right click on the name of the file case in the
"*Object browser*" window, and choose the "*Export to YACS*" sub-menu (or the
"*Export to YACS*" button |eficas_yacs|) as below:

  .. _adao_exporttoyacs00:
  .. image:: images/adao_exporttoyacs.png
    :align: center
    :scale: 75%
  .. centered::
    **"Export to YACS" sub-menu to generate the YACS scheme from the ADAO case**

This command will generate the YACS scheme, activate YACS module in SALOME, and
open the new scheme in the GUI of the YACS module [#]_. After reordering the
nodes by using the "*arrange local node*" sub-menu of the YACS graphical view of
the scheme, you get the following representation of the generated ADAO scheme:

  .. _yacs_generatedscheme:
  .. image:: images/yacs_generatedscheme.png
    :align: center
    :width: 100%
  .. centered::
    **YACS generated scheme from the ADAO case**

After that point, all the modifications, executions and post-processing of the
data assimilation scheme will be done in YACS. In order to check the result in a
simple way, we create here a new YACS node by using the "*in-line script node*"
sub-menu of the YACS graphical view, and we name it "*PostProcessing*".

This script will retrieve the data assimilation analysis from the
"*algoResults*" output port of the computation bloc (which gives access to a
SALOME Python Object), and will print it on the standard output. 

To obtain this, the in-line script node need to have an input port of type
"*pyobj*" named "*results*" for example, that have to be linked graphically to
the "*algoResults*" output port of the computation bloc. Then the code to fill
in the script node is::

    Xa = results.ADD.get("Analysis").valueserie(-1)

    print
    print "Analysis =",Xa
    print

The augmented YACS scheme can be saved (overwriting the generated scheme if the
simple "*Save*" command or button are used, or with a new name). Then,
classically in YACS, it have to be prepared for run, and then executed. After
completion, the printing on standard output is available in the "*YACS Container
Log*", obtained through the right click menu of the "*proc*" window in the YACS
scheme as shown below:

  .. _yacs_containerlog:
  .. image:: images/yacs_containerlog.png
    :align: center
    :width: 100%
  .. centered::
    **YACS menu for Container Log, and dialog window showing the log**

We verify that the result is correct by checking that the log dialog window
contains the following line::

    Analysis = [0.5, 0.5, 0.5]

as shown in the image above.

As a simple extension of this example, one can notice that the same problem
solved with a 3DVAR algorithm gives the same result. This algorithm can be
chosen at the ADAO case building step, before entering in YACS step. The
ADAO 3DVAR case will look completely similar to the BLUE algorithmic case, as
shown by the following figure:

  .. _adao_jdcexample02:
  .. image:: images/adao_jdcexample02.png
    :align: center
    :width: 100%
  .. centered::
    **Defining an ADAO 3DVAR case looks completely similar to a BLUE case**

There is only one command changing, with "*3DVAR*" value instead of "*Blue*".

Building a simple estimation case with external data definition by scripts
--------------------------------------------------------------------------

It is useful to get parts or all of the data from external definition, using
Python script files to provide access to the data. As an example, we build here
an ADAO case representing the same experimental set up as in the above example
`Building a simple estimation case with explicit data definition`_, but using
data form a single one external Python script file.

First, we write the following script file, using conventional names for the
desired variables. Here, all the input variables are defined in the script, but
the user can choose to split the file in several ones, or to mix explicit data
definition in the ADAO GUI and implicit data definition by external files. The
present script looks like::

    import numpy
    #
    # Definition of the Background as a vector
    # ----------------------------------------
    Background = [0, 0, 0]
    #
    # Definition of the Observation as a vector
    # -----------------------------------------
    Observation = "1 1 1"
    #
    # Definition of the Background Error covariance as a matrix
    # ---------------------------------------------------------
    BackgroundError = numpy.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
    #
    # Definition of the Observation Error covariance as a matrix
    # ----------------------------------------------------------
    ObservationError = numpy.matrix("1 0 0 ; 0 1 0 ; 0 0 1")
    #
    # Definition of the Observation Operator as a matrix
    # --------------------------------------------------
    ObservationOperator = numpy.identity(3)

The names of the Python variables above are mandatory, in order to define the
right variables, but the Python script can be bigger and define classes,
functions, etc. with other names. It shows different ways to define arrays and
matrices, using list, string (as in Numpy or Octave), Numpy array type or Numpy
matrix type, and Numpy special functions. All of these syntaxes are valid.

After saving this script somewhere in your path (named here "*script.py*" for
the example), we use the GUI to build the ADAO case. The procedure to fill in
the case is similar except that, instead of selecting the "*String*" option for
the "*FROM*" keyword, we select the "*Script*" one. This leads to a
"*SCRIPT_DATA/SCRIPT_FILE*" entry in the tree, allowing to choose a file as:

  .. _adao_scriptentry01:
  .. image:: images/adao_scriptentry01.png
    :align: center
    :width: 100%
  .. centered::
    **Defining an input value using an external script file**

Other steps and results are exactly the same as in the `Building a simple
estimation case with explicit data definition`_ previous example.

In fact, this script methodology allows to retrieve data from in-line or previous
calculations, from static files, from database or from stream, all of them
outside of SALOME. It allows also to modify easily some input data, for example
for debug purpose or for repetitive execution process, and it is the most
versatile method in order to parametrize the input data. **But be careful,
script methodology is not a "safe" procedure, in the sense that erroneous
data, or errors in calculations, can be directly injected into the YACS scheme
execution.**

Adding parameters to control the data assimilation algorithm
------------------------------------------------------------

One can add some optional parameters to control the data assimilation algorithm
calculation. This is done by using the "*AlgorithmParameters*" keyword in the
definition of the ADAO case, which is an keyword of the ASSIMILATION_STUDY. This
keyword requires a Python dictionary, containing some key/value pairs. The list
of possible optional parameters are given in the subsection
:ref:`subsection_algo_options`.

If no bounds at all are required on the control variables, then one can choose
the "BFGS" or "CG" minimisation algorithm for the 3DVAR algorithm. For
constrained optimization, the minimizer "LBFGSB" is often more robust, but the
"TNC" is sometimes more performant.

This dictionary has to be defined, for example, in an external Python script
file, using the mandatory variable name "*AlgorithmParameters*" for the
dictionary. All the keys inside the dictionary are optional, they all have
default values, and can exist without being used. For example::

    AlgorithmParameters = {
        "Minimizer" : "CG", # Possible choice : "LBFGSB", "TNC", "CG", "BFGS"
        "MaximumNumberOfSteps" : 10,
        }

Then the script can be added to the ADAO case, in a file entry describing the
"*AlgorithmParameters*" keyword, as follows:

  .. _adao_scriptentry02:
  .. image:: images/adao_scriptentry02.png
    :align: center
    :width: 100%
  .. centered::
    **Adding parameters to control the algorithm**

Other steps and results are exactly the same as in the `Building a simple
estimation case with explicit data definition`_ previous example. The dictionary
can also be directly given in the input field associated with the keyword.

Building a complex case with external data definition by scripts
----------------------------------------------------------------

This more complex and complete example has to been considered as a framework for
user inputs, that need to be tailored for each real application. Nevertheless,
the file skeletons are sufficiently general to have been used for various
applications in neutronic, fluid mechanics... Here, we will not focus on the
results, but more on the user control of inputs and outputs in an ADAO case. As
previously, all the numerical values of this example are arbitrary.

The objective is to set up the input and output definitions of a physical case
by external python scripts, using a general non-linear operator, adding control
on parameters and so on... The complete framework scripts can be found in the
ADAO skeletons examples directory under the name
"*External_data_definition_by_scripts*".

Experimental set up
+++++++++++++++++++

We continue to operate in a 3-dimensional space, in order to restrict
the size of numerical object shown in the scripts, but the problem is
not dependant of the dimension. 

We choose a twin experiment context, using a known true state
:math:`\mathbf{x}^t` of arbitrary values:

    ``Xt = [1 2 3]``

The background state :math:`\mathbf{x}^b`, which represent some *a priori*
knowledge of the true state, is build as a normal random perturbation of 20% the
true state :math:`\mathbf{x}^t` for each component, which is:

    ``Xb = Xt + normal(0, 20%*Xt)``

To describe the background error covariances matrix :math:`\mathbf{B}`, we make
as previously the hypothesis of uncorrelated errors (that is, a diagonal matrix,
of size 3x3 because :math:`\mathbf{x}^b` is of lenght 3) and to have the same
variance of 0.1 for all variables. We get:

    ``B = 0.1 * diagonal( lenght(Xb) )``

We suppose that there exist an observation operator :math:`\mathbf{H}`, which
can be non linear. In real calibration procedure or inverse problems, the
physical simulation codes are embedded in the observation operator. We need also
to know its gradient with respect to each calibrated variable, which is a rarely
known information with industrial codes. But we will see later how to obtain an
approximated gradient in this case.

Being in twin experiments, the observation :math:`\mathbf{y}^o` and its error
covariances matrix :math:`\mathbf{R}` are generated by using the true state
:math:`\mathbf{x}^t` and the observation operator :math:`\mathbf{H}`:

    ``Yo = H( Xt )``

and, with an arbitrary standard deviation of 1% on each error component:

    ``R = 0.0001 * diagonal( lenght(Yo) )``

All the required data assimilation informations are then defined.

Skeletons of the scripts describing the setup
+++++++++++++++++++++++++++++++++++++++++++++

We give here the essential parts of each script used afterwards to build the ADAO
case. Remember that using these scripts in real Python files requires to
correctly define the path to imported modules or codes (even if the module is in
the same directory that the importing Python file ; we indicate the path
adjustment using the mention ``"# INSERT PHYSICAL SCRIPT PATH"``), the encoding
if necessary, etc. The indicated file names for the following scripts are
arbitrary. Examples of complete file scripts are available in the ADAO examples
standard directory.

We first define the true state :math:`\mathbf{x}^t` and some convenient matrix
building function, in a Python script file named
``Physical_data_and_covariance_matrices.py``::

    import numpy
    #
    def True_state():
        """
        Arbitrary values and names, as a tuple of two series of same length
        """
        return (numpy.array([1, 2, 3]), ['Para1', 'Para2', 'Para3'])
    #
    def Simple_Matrix( size, diagonal=None ):
        """
        Diagonal matrix, with either 1 or a given vector on the diagonal
        """
        if diagonal is not None:
            S = numpy.diag( diagonal )
        else:
            S = numpy.matrix(numpy.identity(int(size)))
        return S

We can then define the background state :math:`\mathbf{x}^b` as a random
perturbation of the true state, adding at the end of the script the definition
of a *required ADAO variable* in order to export the defined value. It is done
in a Python script file named ``Script_Background_xb.py``::

    from Physical_data_and_covariance_matrices import True_state
    import numpy
    #
    xt, names = True_state()
    #
    Standard_deviation = 0.2*xt # 20% for each variable
    #
    xb = xt + abs(numpy.random.normal(0.,Standard_deviation,size=(len(xt),)))
    #
    # Creating the required ADAO variable
    # -----------------------------------
    Background = list(xb)

In the same way, we define the background error covariance matrix
:math:`\mathbf{B}` as a diagonal matrix of the same diagonal length as the
background of the true state, using the convenient function already defined. It
is done in a Python script file named ``Script_BackgroundError_B.py``::

    from Physical_data_and_covariance_matrices import True_state, Simple_Matrix
    #
    xt, names = True_state()
    #
    B = 0.1 * Simple_Matrix( size = len(xt) )
    #
    # Creating the required ADAO variable
    # -----------------------------------
    BackgroundError = B

To continue, we need the observation operator :math:`\mathbf{H}` as a function
of the state. It is here defined in an external file named
``"Physical_simulation_functions.py"``, which should contain functions
conveniently named here ``"FunctionH"`` and ``"AdjointH"``. These functions are
user ones, representing as programming functions the :math:`\mathbf{H}` operator
and its adjoint. We suppose these functions are given by the user. A simple
skeleton is given in the Python script file ``Physical_simulation_functions.py``
of the ADAO examples standard directory. It can be used in the case only the
non-linear direct physical simulation exists. The script is partly reproduced
here for convenience::

    def FunctionH( XX ):
        """ Direct non-linear simulation operator """
        #
        # --------------------------------------> EXAMPLE TO BE REMOVED
        if type(XX) is type(numpy.matrix([])):  # EXAMPLE TO BE REMOVED
            HX = XX.A1.tolist()                 # EXAMPLE TO BE REMOVED
        elif type(XX) is type(numpy.array([])): # EXAMPLE TO BE REMOVED
            HX = numpy.matrix(XX).A1.tolist()   # EXAMPLE TO BE REMOVED
        else:                                   # EXAMPLE TO BE REMOVED
            HX = XX                             # EXAMPLE TO BE REMOVED
        # --------------------------------------> EXAMPLE TO BE REMOVED
        #
        return numpy.array( HX )
    #
    def TangentHMatrix( X, increment = 0.01, centeredDF = False ):
        """ Tangent operator (Jacobian) calculated by finite differences """
        #
        dX  = increment * X.A1
        #
        if centeredDF:
            # 
            Jacobian  = []
            for i in range( len(dX) ):
                X_plus_dXi     = numpy.array( X.A1 )
                X_plus_dXi[i]  = X[i] + dX[i]
                X_moins_dXi    = numpy.array( X.A1 )
                X_moins_dXi[i] = X[i] - dX[i]
                #
                HX_plus_dXi  = FunctionH( X_plus_dXi )
                HX_moins_dXi = FunctionH( X_moins_dXi )
                #
                HX_Diff = ( HX_plus_dXi - HX_moins_dXi ) / (2.*dX[i])
                #
                Jacobian.append( HX_Diff )
            #
        else:
            #
            HX_plus_dX = []
            for i in range( len(dX) ):
                X_plus_dXi    = numpy.array( X.A1 )
                X_plus_dXi[i] = X[i] + dX[i]
                #
                HX_plus_dXi = FunctionH( X_plus_dXi )
                #
                HX_plus_dX.append( HX_plus_dXi )
            #
            HX = FunctionH( X )
            #
            Jacobian = []
            for i in range( len(dX) ):
                Jacobian.append( ( HX_plus_dX[i] - HX ) / dX[i] )
        #
        Jacobian = numpy.matrix( Jacobian )
        #
        return Jacobian
    #
    def TangentH( X ):
        """ Tangent operator """
        _X = numpy.asmatrix(X).flatten().T
        HtX = self.TangentHMatrix( _X ) * _X
        return HtX.A1
    #
    def AdjointH( (X, Y) ):
        """ Ajoint operator """
        #
        Jacobian = TangentHMatrix( X, centeredDF = False )
        #
        Y = numpy.asmatrix(Y).flatten().T
        HaY = numpy.dot(Jacobian, Y)
        #
        return HaY.A1

We insist on the fact that these non-linear operator ``"FunctionH"``, tangent
operator ``"TangentH"`` and adjoint operator ``"AdjointH"`` come from the
physical knowledge, include the reference physical simulation code and its
eventual adjoint, and have to be carefully set up by the data assimilation user.
The errors in or missuses of the operators can not be detected or corrected by
the data assimilation framework alone.

To operates in the module ADAO, it is required to define for ADAO these
different types of operators: the (potentially non-linear) standard observation
operator, named ``"Direct"``, its linearised approximation, named ``"Tangent"``,
and the adjoint operator named ``"Adjoint"``. The Python script have to retrieve
an input parameter, found under the key "value", in a variable named
``"specificParameters"`` of the SALOME input data and parameters
``"computation"`` dictionary variable. If the operator is already linear, the
``"Direct"`` and ``"Tangent"`` functions are the same, as it can be supposed
here. The following example Python script file named
``Script_ObservationOperator_H.py``, illustrates the case::

    import Physical_simulation_functions
    import numpy, logging
    #
    # -----------------------------------------------------------------------
    # SALOME input data and parameters: all information are the required input
    # variable "computation", containing for example:
    #      {'inputValues': [[[[0.0, 0.0, 0.0]]]],
    #       'inputVarList': ['adao_default'],
    #       'outputVarList': ['adao_default'],
    #       'specificParameters': [{'name': 'method', 'value': 'Direct'}]}
    # -----------------------------------------------------------------------
    #
    # Recovering the type of computation: "Direct", "Tangent" or "Adjoint"
    # --------------------------------------------------------------------
    method = ""
    for param in computation["specificParameters"]:
        if param["name"] == "method":
            method = param["value"]
    logging.info("ComputationFunctionNode: Found method is \'%s\'"%method)
    #
    # Loading the H operator functions from external definitions
    # ----------------------------------------------------------
    logging.info("ComputationFunctionNode: Loading operator functions")
    FunctionH = Physical_simulation_functions.FunctionH
    TangentH  = Physical_simulation_functions.TangentH
    AdjointH  = Physical_simulation_functions.AdjointH
    #
    # Executing the possible computations
    # -----------------------------------
    if method == "Direct":
        logging.info("ComputationFunctionNode: Direct computation")
        Xcurrent = computation["inputValues"][0][0][0]
        data = FunctionH(numpy.matrix( Xcurrent ).T)
    #
    if method == "Tangent":
        logging.info("ComputationFunctionNode: Tangent computation")
        Xcurrent = computation["inputValues"][0][0][0]
        data = TangentH(numpy.matrix( Xcurrent ).T)
    #
    if method == "Adjoint":
        logging.info("ComputationFunctionNode: Adjoint computation")
        Xcurrent = computation["inputValues"][0][0][0]
        Ycurrent = computation["inputValues"][0][0][1]
        data = AdjointH((numpy.matrix( Xcurrent ).T, numpy.matrix( Ycurrent ).T))
    #
    # Formatting the output
    # ---------------------
    logging.info("ComputationFunctionNode: Formatting the output")
    it = data.flat
    outputValues = [[[[]]]]
    for val in it:
      outputValues[0][0][0].append(val)
    #
    # Creating the required ADAO variable
    # -----------------------------------
    result = {}
    result["outputValues"]        = outputValues
    result["specificOutputInfos"] = []
    result["returnCode"]          = 0
    result["errorMessage"]        = ""

As output, this script has to define a nested list variable, as shown above with
the ``"outputValues"`` variable, where the nested levels describe the different
variables included in the state, then the different possible states at the same
time, then the different time steps. In this case, because there is only one
time step and one state, and all the variables are stored together, we only set
the most inner level of the lists.

In this twin experiments framework, the observation :math:`\mathbf{y}^o` and its
error covariances matrix :math:`\mathbf{R}` can be generated. It is done in two
Python script files, the first one being named ``Script_Observation_yo.py``::

    from Physical_data_and_covariance_matrices import True_state
    from Physical_simulation_functions import FunctionH
    #
    xt, noms = True_state()
    #
    yo = FunctionH( xt )
    #
    # Creating the required ADAO variable
    # -----------------------------------
    Observation = list(yo)

and the second one named ``Script_ObservationError_R.py``::

    from Physical_data_and_covariance_matrices import True_state, Simple_Matrix
    from Physical_simulation_functions import FunctionH
    #
    xt, names = True_state()
    #
    yo = FunctionH( xt )
    #
    R  = 0.0001 * Simple_Matrix( size = len(yo) )
    #
    # Creating the required ADAO variable
    # -----------------------------------
    ObservationError = R

As in previous examples, it can be useful to define some parameters for the data
assimilation algorithm. For example, if we use the standard 3DVAR algorithm, the
following parameters can be defined in a Python script file named
``Script_AlgorithmParameters.py``::

    # Creating the required ADAO variable
    # -----------------------------------
    AlgorithmParameters = {
        "Minimizer" : "TNC",         # Possible : "LBFGSB", "TNC", "CG", "BFGS"
        "MaximumNumberOfSteps" : 15, # Number of global iterative steps
        "Bounds" : [
            [ None, None ],          # Bound on the first parameter
            [ 0., 4. ],              # Bound on the second parameter
            [ 0., None ],            # Bound on the third parameter
            ],
    }

Finally, it is common to post-process the results, retrieving them after the
data assimilation phase in order to analyse, print or show them. It requires to
use a intermediary Python script file in order to extract these results. The
following example Python script file named ``Script_UserPostAnalysis.py``,
illustrates the fact::

    from Physical_data_and_covariance_matrices import True_state
    import numpy
    #
    xt, names   = True_state()
    xa          = ADD.get("Analysis").valueserie(-1)
    x_series    = ADD.get("CurrentState").valueserie()
    J           = ADD.get("CostFunctionJ").valueserie()
    #
    # Verifying the results by printing
    # ---------------------------------
    print
    print "xt = %s"%xt
    print "xa = %s"%numpy.array(xa)
    print
    for i in range( len(x_series) ):
        print "Step %2i : J = %.5e  et  X = %s"%(i, J[i], x_series[i])
    print

At the end, we get a description of the whole case setup through a set of files
listed here:

#.      ``Physical_data_and_covariance_matrices.py``
#.      ``Physical_simulation_functions.py``
#.      ``Script_AlgorithmParameters.py``
#.      ``Script_BackgroundError_B.py``
#.      ``Script_Background_xb.py``
#.      ``Script_ObservationError_R.py``
#.      ``Script_ObservationOperator_H.py``
#.      ``Script_Observation_yo.py``
#.      ``Script_UserPostAnalysis.py``

We insist here that all these scripts are written by the user and can not be
automatically tested. So the user is required to verify the scripts (and in
particular their input/output) in order to limit the difficulty of debug. We
recall: **script methodology is not a "safe" procedure, in the sense that
erroneous data, or errors in calculations, can be directly injected into the
YACS scheme execution.**

Building the case with external data definition by scripts
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

All these scripts can then be used to define the ADAO case with external data
definition by Python script files. It is entirely similar to the method
described in the `Building a simple estimation case with external data
definition by scripts`_ previous section. For each variable to be defined, we
select the "*Script*" option of the "*FROM*" keyword, which leads to a
"*SCRIPT_DATA/SCRIPT_FILE*" entry in the tree.

The other steps to build the ADAO case are exactly the same as in the `Building
a simple estimation case with explicit data definition`_ previous section.

Using the simple linear operator :math:`\mathbf{H}` from the Python script file
``Physical_simulation_functions.py`` in the ADAO examples standard directory,
the results will look like::

    xt = [1 2 3]
    xa = [ 1.000014    2.000458  3.000390]

    Step  0 : J = 1.81750e+03  et  X = [1.014011, 2.459175, 3.390462]
    Step  1 : J = 1.81750e+03  et  X = [1.014011, 2.459175, 3.390462]
    Step  2 : J = 1.79734e+01  et  X = [1.010771, 2.040342, 2.961378]
    Step  3 : J = 1.79734e+01  et  X = [1.010771, 2.040342, 2.961378]
    Step  4 : J = 1.81909e+00  et  X = [1.000826, 2.000352, 3.000487]
    Step  5 : J = 1.81909e+00  et  X = [1.000826, 2.000352, 3.000487]
    Step  6 : J = 1.81641e+00  et  X = [1.000247, 2.000651, 3.000156]
    Step  7 : J = 1.81641e+00  et  X = [1.000247, 2.000651, 3.000156]
    Step  8 : J = 1.81569e+00  et  X = [1.000015, 2.000432, 3.000364]
    Step  9 : J = 1.81569e+00  et  X = [1.000015, 2.000432, 3.000364]
    Step 10 : J = 1.81568e+00  et  X = [1.000013, 2.000458, 3.000390]
    ...

The state at the first step is the randomly generated background state
:math:`\mathbf{x}^b`. After completion, these printing on standard output is
available in the "*YACS Container Log*", obtained through the right click menu
of the "*proc*" window in the YACS scheme.

.. [#] For more information on YACS, see the the *YACS module User's Guide* available in the main "*Help*" menu of SALOME GUI.
