.. _section_examples:

================================================================================
Examples on using the ADAO module
================================================================================

.. |eficas_new| image:: images/eficas_new.png
   :align: middle
.. |eficas_save| image:: images/eficas_save.png
   :align: middle
.. |eficas_yacs| image:: images/eficas_yacs.png
   :align: middle

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
not dependant of the dimension and can be set in dimension 1000... The observed
state is of value 1 in each direction, so:

    ``Yo = [1 1 1]``

The background state, which represent some *a priori* knowledge or a
regularization, is of value of 0 in each direction, which is:

    ``Xb = [0 0 0]``

Data assimilation requires information on errors covariances for observation and
background variables. We choose here to have uncorrelated errors (that is,
diagonal matrices) and to have the same variance of 1 for all variables (that
is, identity matrices. We get:

    ``B = R = [1 0 0 ; 0 1 0 ; 0 0 1]``

Last, we need an observation operator to convert the background value in the
space of observation value. Here, because the space dimensions are the same, we
can choose the identity  as the observation operator:

    ``H = [1 0 0 ; 0 1 0 ; 0 0 1]``

With such choices, the Best Linear Unbiased Estimator (BLUE) will be the
average vector between ``Yo`` and ``Xb``, named the *analysis* and denoted by
``Xa``:

    ``Xa = [0.5 0.5 0.5]``

As en extension of this example, one can change the variances for ``B`` or ``R``
independently, and the analysis will move to ``Yo`` or ``Xb`` in inverse
proportion of the variances in ``B`` and ``R``. It is also equivalent to search
for the analysis thought a BLUE algorithm or a 3DVAR one.

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

  .. _adao_exporttoyacs:
  .. image:: images/adao_exporttoyacs.png
    :align: center
    :scale: 75%
  .. centered::
    **"Export to YACS" submenu to generate the YACS scheme from the ADAO case**

This command will generate the YACS scheme, activate YACS module in SALOME, and
open the new scheme in the GUI of the YACS module [#]. After reordering the
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

Building a simple estimation case with external data definition by functions
----------------------------------------------------------------------------

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

    #-*-coding:iso-8859-1-*-
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
keyword requires a Python dictionary, containing some key/value pairs.

For example, with a 3DVAR algorithm, the possible keys are "*Minimizer*",
"*MaximumNumberOfSteps*", and "*Bounds*":

#.   The "*Minimizer*" key allows to choose the optimisation minimizer, the
     default choice being "LBFGSB", and the possible ones "LBFGSB" (nonlinear
     constrained minimizer, see [Byrd95] and [Zhu97]), "TNC" (nonlinear
     constrained minimizer), "CG" (nonlinear unconstrained minimizer), "BFGS"
     (nonlinear unconstrained minimizer).
#.   The "*MaximumNumberOfSteps*" key indicates the maximum number of iterations
     allowed for iterative optimisation. The default is 15000, which very
     similar of no limit on iterations. It is then recommended to adapt this
     parameter to the needs on real problems.
#.   The "*Bounds*" key allows to define upper and lower bounds for every
     control variable being optimized. Bounds can be given by a list of list of
     pairs of lower/upper bounds for each variable, with possibly ``None`` every
     time there is no bound.

If no bounds at all are required on the control variables, then one can choose
the "BFGS" or "CG" minimisation algorithm for the 3DVAR algorithm.

This dictionary has to be defined, for example, in an external Python script
file, using the mandatory variable name "*AlgorithmParameters*" for the
dictionary. All the keys inside the dictionary are optional, they all have
default values, and can exist without being used. For example::

    #-*-coding:iso-8859-1-*-
    #
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

.. [#] For more information on YACS, see the the *YACS User Guide* available in the main "*Help*" menu of SALOME GUI.
