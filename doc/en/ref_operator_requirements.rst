..
   Copyright (C) 2008-2015 EDF R&D

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
and they are given as non-oriented vectors (of type list or Numpy array) or
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
(or keep the default value), using through the GUI the keyword
"*DifferentialIncrement*", which has a default value of 1%. This coefficient
will be used in the finite differences approximation to build the tangent and
adjoint operators. The finite differences approximation order can also be chosen
through the GUI, using the keyword "*CenteredFiniteDifference*", with 0 for an
uncentered schema of first order (which is the default value), and with 1 for a
centered schema of second order (of twice the first order computational cost).

This first operator definition form allows easily to test the functional form
before its use in an ADAO case, greatly reducing the complexity of
operator implementation.

**Important warning:** the name "*DirectOperator*" is mandatory, and the type of
the ``X`` argument can be either a list, a numpy array or a numpy 1D-matrix. The
user function has to accept and treat all these cases.

Second functional form: using "*ScriptWithFunctions*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithFunctions
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

**In general, it is recommended to use the first functional form rather than
the second one. A small performance improvement is not a good reason to use a
detailed implementation as this second functional form.**

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
respectively the ``dX`` or the ``Y`` arguments are ``None``, the user has to
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

Special case of controlled evolution or observation operator
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

In some cases, the evolution or the observation operator is required to be
controlled by an external input control, given *a priori*. In this case, the
generic form of the incremental model is slightly modified as follows:

.. math:: \mathbf{y} = O( \mathbf{x}, \mathbf{u})

where :math:`\mathbf{u}` is the control over one state increment. In fact, the
direct operator has to be applied to a pair of variables :math:`(X,U)`.
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
