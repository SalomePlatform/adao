..
   Copyright (C) 2008-2017 EDF R&D

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

.. _section_methodology:

================================================================================
**[DocT]** Methodology to elaborate a Data Assimilation or Optimization study
================================================================================

This section presents the methodology to build a Data Assimilation or
Optimization study. It describes the conceptual steps to build autonomously such
a study. It is not dependent of any tool, but the ADAO module allows to set up
efficiently such a study, following :ref:`section_using`. Notations are the same
than the ones used in :ref:`section_theory`.

Logical procedure for a study
-----------------------------

For a generic Data Assimilation or Optimization study, the main methodological
steps can be the following:

    - :ref:`section_m_step1`
    - :ref:`section_m_step2`
    - :ref:`section_m_step3`
    - :ref:`section_m_step4`
    - :ref:`section_m_step5`
    - :ref:`section_m_step6`
    - :ref:`section_m_step7`

Each step will be detailed in the next sections.

Detailed procedure for a study
------------------------------

.. _section_m_step1:

STEP 1: Specifying the resolution of the physical problem and the parameters to adjust
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

An essential knowledge, about the physical system to be studied, is the
numerical simulation, often available through calculation case(s) and symbolized
as a **simulation operator** (previously included in :math:`H`). A standard
calculation case gathers model hypothesis, numerical implementation, computing
capacities, etc. in order to represent the behavior of the physical system.
Moreover, a calculation case is characterized by its computing time and memory
requirements, its data and results sizes, etc. The knowledge of all these
elements is of primary importance in the setup of the data assimilation or
optimization study.

To state correctly the study, one have also to state or choose the unknowns of
the simulation. For example, this can be expressed through physical models, of
which the parameters can be adjusted. Moreover, it is always useful to add some
knowledge of sensitivity, for example of the numerical simulation to the
parameters that can be adjusted. More general elements, like stability or
regularity of the simulation with respect to the unknown inputs, are also of
great interest.

Technically, optimization methods can require gradient information of the
simulation with respect to unknowns. In this case, explicit gradient code has to
be given or numerical gradient has to be tuned. Its quality is in relation with
code stability or regularity, and it has to be checked carefully before
establishing optimization calculations.

An **observation operator** is always required, in complement of the simulation
operator. This observation operator, denoted as :math:`H` or included in, has to
convert the numerical simulation outputs into something that is directly
comparable to observations. It is as essential operator as it is the way to
compare simulations and observations. It is usually done by sampling, projection
or integration, of the numerical outputs, but it can be more complicated. Often,
because the observation operator follows the simulation one in simple data
assimilation schemes, 

.. _section_m_step2:

STEP 2: Specifying the criteria for physical results qualification
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Because the studied system are real physical ones, it is of great importance to
express the **physical information that can help to qualify a simulated state**.
There are two main types of such information that leads to criteria allowing
qualification and quantification of future results.

First, coming from numerical or mathematical knowledge, a lot of standard
criteria allow to qualify, relatively or in absolute, the quality of a state.
For example, balance equations or equation closing conditions are good
complementary measures of optimized state quality. Criteria like RMS, RMSE,
field extrema, integrals, etc. are also of great interest to assess optimized
state quality.

Second, coming from physical or experimental knowledge, valuable information can
be obtained on the meaning of optimized states or results. In particular,
physical validity or technical interest can assess of the mathematical results
of the optimization.

In order to get helpful information from these two main types of knowledge, it
is recommended, if possible, to build numerical criteria to ease the assessment
of physical results quality.

.. _section_m_step3:

STEP 3: Identifying and describe the available observations
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

As the second main source of knowledge of the physical system to be studied, the
**observations, or measures,** denoted as :math:`\mathbf{y}^o`, has to be
properly described. The quality of the measures, their intrinsic errors, the
special features is worth to know, in order to introduce these information in
the data assimilation or optimization calculations.

The observations have not only to be available, but also to be easily introduced
in the numerical framework of calculation  or optimization. So the computing
environment  giving access to the observations is of great importance to smooth
the effective use of various measures and sources of measures, and to promote
extensive tests using measures. Computing environment covers availability in
database or not, data formats, computing interfaces...

.. _section_m_step4:

STEP 4: Specifying the AD/Optimization modeling elements (covariance, background...)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Additional Data Assimilation and Optimization modeling elements allows to
improve information about the fine physical representation of the studied
system.

The *a-priori* knowledge of the system state can be modelized using the
**background**, denoted as :math:`\mathbf{x}^b`, and the **background error
covariance matrix**, denoted as :math:`\mathbf{B}`. These information are
extremely important to complete, in particular in order to obtain meaningful
results from Data Assimilation.

On the other hand, information on observation errors can be used to fill the
**observation error covariance matrix** denoted as :math:`\mathbf{R}`. As for
:math:`\mathbf{B}`, it is recommended to use carefully checked data to fill
these covariance matrices.

In case of dynamic simulation, one has to define also an **evolution operator**
and the associated error covariance matrix.

.. _section_m_step5:

STEP 5: Choosing the algorithms and their parameters
++++++++++++++++++++++++++++++++++++++++++++++++++++

Data Assimilation or Optimization requires to solve an optimization problem,
more often modelized as a minimization problem. Depending on the availability of
the gradient of the cost function with respect to the optimization parameters,
recommended class of optimization methods are different. Variational or locally
linearized minimization methods requires this gradient. On the opposite,
derivative free optimization methods doesn't requires this gradient but usually
at a higher computational price.

Inside a class of optimization methods, there is usually a trade-off between the
*"generic capacity of a method"* and the *"particular performance on a specific
problem"*. Generic methods, as for example variational minimization using the
:ref:`section_ref_algorithm_3DVAR`, present remarkable properties of efficiency,
robustness and reliability, that leads to recommend it independently of the
problem. Moreover, it is generally difficult to tune the parameters of an
optimization method, so the most robust one is often the one with the less
parameters. Finally, at least for the beginning, it is recommended to use the
most generic method and to change the less possible the known default
parameters.

.. _section_m_step6:

STEP 6: Conducting the calculations and get the results
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

After setting up the Data Assimilation or Optimization study, the calculation
has to be done in an efficient way.

Because optimizing usually involves a lot of elementary physical simulation of
the system, the calculations are often done in Hight Performance Computing (HPC)
environment to reduce the overall user time. Even if the optimization problem is
small, the simulation time can be long, requiring efficient computing resources.
These requirements have to be taken into account early enough in the study
procedure to be satisfied without needing too much effort.

For the same reason of hight computing requirements, it is important to
carefully prepare the outputs of the optimization procedure. The optimal state
is the main required information, but a lot of other special information can be
obtained during or at the end of the optimization process: error evaluations,
intermediary states, quality indicators... All these information, sometimes
requiring additional processing, has to be asked at the beginning of the
optimization process.

.. _section_m_step7:

STEP 7: Exploiting the results and qualify their physical properties
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Once getting the results, they have to be interpreted in terms of physical and
numerical meaning. Even if the optimization calculation always give a new
optimal state at least as good as the *a priori* one, and hopefully better, this
optimal state has for example to be checked with respect to the quality criteria
identified when :ref:`section_m_step2`. This can lead to physical, statistical
or numerical studies in order to assess the interest of the optimal state to
represent the physical system.

Besides this analysis that has to be done for each Data Assimilation or
Optimization study, it can be worth to exploit the optimization results as part
of a more complete study of the physical system.
