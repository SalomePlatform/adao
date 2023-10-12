..
   Copyright (C) 2008-2023 EDF R&D

   This file is part of SALOME ADAO module.

   This library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 2.1 of the License, or (at your option) any later version.

   This library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public
   License along with this library; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA

   See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com

   Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

.. _section_ref_operator_requirements:

Requirements for functions describing an operator
-------------------------------------------------

.. index:: single: setObservationOperator
.. index:: single: setEvolutionModel
.. index:: single: setControlModel

The availability of the operators of observation, and sometimes of evolution,
are required to implement the data assimilation or optimization procedures. As
the evolution operator is considered in its incremental form, which represents
the transition between two successive states, it is then formally similar to
the observation operator and the way to describe them is unique.

These operators include the **physical simulation by numerical calculations**.
But they also include **filtering, projection or restriction** of simulated
quantities, which are necessary to compare the simulation to the observation.

Schematically, an operator :math:`O` has to give a output simulation or
solution for specified input parameters. Part of the input parameters can be
modified during the optimization procedure. So the mathematical representation
of such a process is a function. It was briefly described in the section
:ref:`section_theory`. It is generalized here by the relation:

.. math:: \mathbf{y} = O( \mathbf{x} )

between the pseudo-observations outputs :math:`\mathbf{y}` and the input
parameters :math:`\mathbf{x}` using the observation or evolution :math:`O`
operator. The same functional representation can be used for the linear tangent
model :math:`\mathbf{O}` of :math:`O` and its adjoint :math:`\mathbf{O}^*`,
also required by some data assimilation or optimization algorithms.

On input and output of these operators, the :math:`\mathbf{x}` and
:math:`\mathbf{y}` variables, or their increments, are mathematically vectors,
and they can be given by the user as non-oriented vectors (of type list or
Numpy array) or oriented ones (of type Numpy matrix).

Then, **to fully describe an operator, the user has only to provide a function
that completely and only realize the functional operation**.

This function is usually given as a **Python function or script**, that can be
in particular executed as an independent Python function or in a YACS node.
These function or script can, with no differences, launch external codes or use
internal Python or SALOME calls and methods. If the algorithm requires the 3
aspects of the operator (direct form, tangent form and adjoint form), the user
has to give the 3 functions or to approximate them using ADAO.

There are for the user 3 practical methods to provide an operator functional
representation, which are different depending on the chosen argument:

- :ref:`section_ref_operator_one`
- :ref:`section_ref_operator_funcs`
- :ref:`section_ref_operator_switch`

In case of ADAO scripted interface (TUI), only the first two are necessary
because the third is included in the second. In case of ADAO graphical
interface EFICAS, these methods are chosen in the "*FROM*"  field of each
operator having a "*Function*" value as "*INPUT_TYPE*", as shown by the
following figure:

  .. eficas_operator_function:
  .. image:: images/eficas_operator_function.png
    :align: center
    :width: 100%
  .. centered::
    **Choosing graphically an operator functional representation**

In ADAO textual interface (TUI), in the specific case illustrated above, the
same approach is taken by writing :
::

    ...
    case.set( 'ObservationOperator',
        OneFunction = True,
        Script = 'scripts_for_JDC.py'
        )
    ...

.. _section_ref_operator_one:

First functional form: one direct operator only
+++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: OneFunction
.. index:: single: ScriptWithOneFunction
.. index:: single: DirectOperator
.. index:: single: DifferentialIncrement
.. index:: single: CenteredFiniteDifference

The first one consist in providing only one function, potentially non-linear,
and to approximate the associated tangent and adjoint operators.

This is done in ADAO by using, in the ADAO graphical interface EFICAS, the
keyword "*ScriptWithOneFunction*" for the description by a script. In the
textual interface, it is the keyword "*OneFunction*", possibly combined with
"*Script*" keyword depending on whether it is a function or a script. If it is
by external script, the user must provide a file containing a function that has
the mandatory name "*DirectOperator*". For example, an external script can
follow the generic template::

    def DirectOperator( X ):
        """ Direct non-linear simulation operator """
        ...
        ...
        ...
        # Result: Y = O(X)
        return "a vector similar to Y"

In this case, the user has also provide a value for the differential increment
(or keep the default value), using through the graphical interface (GUI) or
textual one (TUI) the keyword "*DifferentialIncrement*" as parameter, which has
a default value of 1%. This coefficient will be used in the finite differences
approximation to build the tangent and adjoint operators. The finite
differences approximation order can also be chosen through the GUI, using the
keyword "*CenteredFiniteDifference*", with ``False`` or 0 for an uncentered
schema of first order (which is the default value), and with ``True`` or 1 for
a centered schema of second order (and of twice the first order computational
cost). If necessary and if possible, :ref:`subsection_ref_parallel_df` can be
used. In all cases, an internal cache mechanism is used to restrict the number
of operator evaluations at the minimum possible in a sequential or parallel
execution scheme for numerical approximations of the tangent and adjoint
operators, to avoid redundant calculations. One can refer to the section
dealing with :ref:`subsection_iterative_convergence_control` to discover the
interaction with the convergence parameters.

This first operator definition form allows easily to test the functional form
before its use in an ADAO case, greatly reducing the complexity of operator
implementation. One can then use the "*FunctionTest*" ADAO checking algorithm
(see the section on the :ref:`section_ref_algorithm_FunctionTest`) specifically
designed for this test.

**Important:** the name "*DirectOperator*" is mandatory when using an
independant Python script. The type of the input ``X`` argument can be either a
list of float values, a Numpy array or a Numpy matrix, and the user function
has to accept and treat all these cases. The type of the output argument ``Y``
must also be equivalent to a list of real values.

Various forms of operators are available in several scripts included in the
:ref:`section_docu_examples`.

.. _section_ref_operator_funcs:

Second functional form: three operators direct, tangent and adjoint
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ThreeFunctions
.. index:: single: ScriptWithFunctions
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

.. warning::

  In general, it is recommended to use the first functional form rather than
  the second one. A small performance improvement is not a good reason to use a
  detailed implementation as this second functional form.

The second one consist in providing directly the three associated operators
:math:`O`, :math:`\mathbf{O}` and :math:`\mathbf{O}^*`. This is done by using
the keyword "*ScriptWithFunctions*" for the description of the chosen operator
in the ADAO graphical interface EFICAS. In the textual interface, it is the
keyword "*ThreeFunctions*", possibly combined with "*Script*" keyword depending
on whether it is a function or a script. The user have to provide in one script
three functions, with the three mandatory names "*DirectOperator*",
"*TangentOperator*" and "*AdjointOperator*". For example, the external script
can follow the template::

    def DirectOperator( X ):
        """ Direct non-linear simulation operator """
        ...
        ...
        ...
        return "a vector similar to Y"

    def TangentOperator( pair = (X, dX) ):
        """ Tangent linear operator, around X, applied to dX """
        X, dX = pair
        ...
        ...
        ...
        return "a vector similar to Y"

    def AdjointOperator( pair = (X, Y) ):
        """ Adjoint operator, around X, applied to Y """
        X, Y = pair
        ...
        ...
        ...
        return "a vector similar to X"

Another time, this second operator definition allow easily to test the
functional forms before their use in an ADAO case, reducing the complexity of
operator implementation.

For some algorithms (in particular filters without ensemble), it is required
that the tangent and adjoint functions can return the matrix equivalent to the
linear operator. In this case, when respectively the ``dX`` or the ``Y``
arguments are ``None``, the user script has to return the associated matrix.
The templates of the "*TangentOperator*" and "*AddOperator*" functions then
become the following::

    def TangentOperator( pair = (X, dX) ):
        """ Tangent linear operator, around X, applied to dX """
        X, dX = pair
        ...
        ...
        ...
        if dX is None or len(dX) == 0:
            return "the matrix of the tangent linear operator"
        else:
            return "a vector similar to Y"

    def AdjointOperator( pair = (X, Y) ):
        """ Adjoint operator, around X, applied to Y """
        X, Y = pair
        ...
        ...
        ...
        if Y is None or len(Y) == 0:
            return "the adjoint linear operator matrix"
        else:
            return "a vector similar to X"

**Important:** the names "*DirectOperator*", "*TangentOperator*" and
"*AdjointOperator*" are mandatory when using an independent Python script. The
type of the ``X``, Y``, ``dX`` input or output arguments can be either a list
of float values, a Numpy array or a Numpy matrix. The user function has to
treat these cases in his script.

.. _section_ref_operator_switch:

Third functional form: three operators with a switch
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithSwitch
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

**It is recommended not to use this third functional form without a strong
numerical or physical reason. A performance improvement is not a good reason to
use the implementation complexity of this third functional form. Only an
inability to use the first or second forms justifies the use of the third.**

This third form give more possibilities to control the execution of the three
functions representing the operator, allowing advanced usage and control over
each execution of the simulation code. This is done by using the keyword
"*ScriptWithSwitch*" for the description of the chosen operator in the ADAO
graphical interface EFICAS. In the textual interface, you only have to use the
keyword "*ThreeFunctions*" above to also define this case, with the right
functions. The user have to provide a switch in one script to control the
execution of the direct, tangent and adjoint forms of its simulation code. The
user can then, for example, use other approximations for the tangent and
adjoint codes, or introduce more complexity in the argument treatment of the
functions. But it will be far more complicated to implement and debug.

If, however, you want to use this third form, we recommend using the following
template for the switch. It requires an external script or code named here
"*Physical_simulation_functions.py*", containing three functions named
"*DirectOperator*", "*TangentOperator*" and "*AdjointOperator*" as previously.
Here is the switch template::

    import Physical_simulation_functions
    import numpy, logging, codecs, pickle
    def loads( data ):
        return pickle.loads(codecs.decode(data.encode(), "base64"))
    #
    method = ""
    for param in computation["specificParameters"]:
        if param["name"] == "method":
            method = loads(param["value"])
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

.. _section_ref_operator_control:

Special case of controlled evolution or observation operator
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

In some cases, the evolution or the observation operator is required to be
controlled by an external input control, given *a priori*. In this case, the
generic form of the incremental model :math:`O` is slightly modified as
follows:

.. math:: \mathbf{y} = O( \mathbf{x}, \mathbf{u})

where :math:`\mathbf{u}` is the control over one state increment. In fact, the
direct operator has to be applied to a pair of variables :math:`(X,U)`.
Schematically, the operator :math:`O` has to be set up as a function applicable
on a pair :math:`\mathbf{(X, U)}` as follows::

    def DirectOperator( pair = (X, U) ):
        """ Direct non-linear simulation operator """
        X, U = pair
        ...
        ...
        ...
        return something like X(n+1) (evolution) or Y(n+1) (observation)

The tangent and adjoint operators have the same signature as previously, noting
that the derivatives has to be done only partially against :math:`\mathbf{x}`.
In such a case with explicit control, only the second functional form (using
"*ScriptWithFunctions*") and third functional form (using "*ScriptWithSwitch*")
can be used.

.. _section_ref_operator_dimensionless:

Additional notes on dimensionless transformation of operators
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Nondimensionalization
.. index:: single: Dimensionless

It is common that physical quantities, in input or output of the operators,
have significant differences in magnitude or rate of change. One way to avoid
numerical difficulties is to use, or to set, a dimensionless version of
calculations carried out in operators [WikipediaND]_. In principle, since
physical simulation should be as dimensionless as possible, it is at first
recommended to use the existing dimensionless capacity of the calculation code.

However, in the common case where we can not dispose of it, it is often useful
to surround the calculation to remove dimension for input or output. A simple
way to do this is to convert the input parameters :math:`\mathbf{x}` which are
arguments of a function like "*DirectOperator*". One mostly use the default
values :math:`\mathbf{x}^b` (background, or nominal value). Provided that each
component of :math:`\mathbf{x}^b` is non zero, one can indeed use a
multiplicative correction. For this, one can for example state:

.. math:: \mathbf{x} = \mathbf{\alpha}\mathbf{x}^b

and then optimize the multiplicative parameter :math:`\mathbf{\alpha}`.  This
parameter has as default value (or as background) a vector of 1. In the same
way, one can use additive correction if it is more interesting from a physical
point of view. In this case, one can state:

.. math:: \mathbf{x} =\mathbf{x}^b + \mathbf{\alpha}

and then optimize the additive parameter :math:`\mathbf{\alpha}`. In this case,
the parameter has for background value a vector of 0.

Be careful, applying a dimensionless transformation also requires changing the
associated error covariances in an ADAO formulation of the optimization
problem.

Such a process is rarely enough to avoid all the numerical problems, but it
often improves a lot the numeric conditioning of the optimization.

.. index:: single: InputFunctionAsMulti

Dealing explicitly with "multiple" functions
++++++++++++++++++++++++++++++++++++++++++++

.. warning::

  It is strongly recommended not to use this explicit "multiple" functions
  definition without a very strong computing justification. This treatment is
  already done by default in ADAO to increase performances. Only the very
  experienced user, seeking to manage particularly difficult cases, can be
  interested in this extension. Despite its simplicity, there is an explicit
  risk of significantly worsening performance, or getting weird runtime errors.

It is possible, when defining operator's functions, to set them as functions
that treat not only one argument, but a series of arguments, to give back on
output the corresponding value series. Writing it as pseudo-code, the
"multiple" function, here named ``MultiFunctionO``, representing the classical
operator :math:`O` named "*DirectOperator*", does::

    def MultiFunctionO( Inputs ):
        """ Multiple ! """
        Outputs = []
        for X in Inputs:
            Y = DirectOperator( X )
            Outputs.append( Y )
        return Outputs

The length of the output (that is, the number of calculated values) is equal to
the length of the input (that is, the number of states for which one want to
calculate the value by the operator).

This possibility is only available in the TUI textual interface for ADAO. For
this, when defining an operator's function, in the same time one usually define
the function or the external script, it can be set using an additional boolean
parameter "*InputFunctionAsMulti*" that the definition is one of a "multiple"
function. For example, if it is the observation operator that is defined in
this way, one should write (knowing that all other optional commands remain
unchanged):
::

    case.set( 'ObservationOperator',
        OneFunction          = MultiFunctionO,
        ...
        InputFunctionAsMulti = True,
        )
