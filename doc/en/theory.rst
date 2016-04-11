..
   Copyright (C) 2008-2016 EDF R&D

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

.. _section_theory:

=================================================================================
**[DocT]** A brief introduction to Data Assimilation and Optimization
=================================================================================

.. index:: single: Data Assimilation
.. index:: single: true state
.. index:: single: observation
.. index:: single: a priori

**Data Assimilation** is a general framework for computing the optimal estimate
of the true state of a system, over time if necessary. It uses values obtained
by combining both observations and *a priori* models, including information
about their errors.

In other words, data assimilation merges measurement data of a system, that are
the observations, with *a priori* system physical and mathematical knowledge,
embedded in numerical models, to obtain the best possible estimate of the system
real state and of its stochastic properties. Note that this real state (or
"*true state*") can not be reached, but can only be estimated. Moreover, despite
the fact that the used information are stochastic by nature, data assimilation
provides deterministic techniques in order to perform very efficiently the
estimation.

Because data assimilation look for the **best possible** estimate, its
underlying procedure always integrates optimization in order to find this
estimate: particular optimization methods are always embedded in data
assimilation algorithms. Optimization methods can be seen in ADAO as a way to
extend data assimilation applications. They will be introduced this way in the
section `Going further in the state estimation by optimization methods`_, but
they are far more general and can be used without data assimilation concepts.

Two main types of applications exist in data assimilation, being covered by the
same formalism: **parameters identification** and **fields reconstruction**.
Before introducing the `Simple description of the data assimilation
methodological framework`_ in a next section, we describe briefly these two
types. At the end, some references allow `Going further in the data assimilation
framework`_.

Fields reconstruction or measures interpolation
-----------------------------------------------

.. index:: single: fields reconstruction
.. index:: single: measures interpolation
.. index:: single: fields interpolation

**Fields reconstruction (or interpolation)** consists in finding, from a
restricted set of real measures, the physical field which is the most
*consistent* with these measures.

This *consistency* is to understand in terms of interpolation, that is to say
that the field we want to reconstruct, using data assimilation on measures, has
to fit at best the measures, while remaining constrained by the overall field
calculation. The calculation is thus an *a priori* estimation of the field that
we seek to identify.

If the system evolves in time, the reconstruction has to be established on every
time step, of the field as a whole. The interpolation process in this case is
more complicated since it is temporal, and not only in terms of instantaneous
values of the field.

A simple example of fields reconstruction comes from meteorology, in which one
look for value of variables such as temperature or pressure in all points of the
spatial domain. One have instantaneous measurements of these quantities at
certain points, but also a history set of these measures. Moreover, these
variables are constrained by evolution equations for the state of the
atmosphere, which indicates for example that the pressure at a point can not
take any value independently of the value at this same point in previous time.
One must therefore make the reconstruction of a field at any point in space, in
a "consistent" manner with the evolution equations and with the measures of the
previous time steps.

Parameters identification, models adjustment, calibration
---------------------------------------------------------

.. index:: single: parameters identification
.. index:: single: parameters adjustment
.. index:: single: models adjustment
.. index:: single: calibration
.. index:: single: background
.. index:: single: regularization
.. index:: single: inverse problems

The **identification (or adjustment) of parameters** by data assimilation is a
form of state calibration which uses both the physical measurement and an *a
priori* parameters estimation (called the "*background*") of the state that one
seeks to identify, as well as a characterization of their errors. From this
point of view, it uses all available information on the physical system, with
restrictive yet realistic assumptions about errors, to find the "*optimal
estimation*" from the true state. We note, in terms of optimization, that the
background realizes a "*regularization*", in the mathematical meaning of
Tikhonov [[Tikhonov77]_ [WikipediaTI]_, of the main problem of parameters
identification. One can also use the term "*inverse problem*" to refer to this
process.

In practice, the two observed gaps "*calculation-measures*" and
"*calculation-background*" are combined to build the calibration correction of
parameters or initial conditions. The addition of these two gaps requires a
relative weight, which is chosen to reflect the trust we give to each piece of
information. This confidence is depicted by the covariance of the errors on the
background and on the observations. Thus the stochastic aspect of information is
essential for building the calibration error function.

A simple example of parameters identification comes from any kind of physical
simulation process involving a parametrized model. For example, a static
mechanical simulation of a beam constrained by some forces is described by beam
parameters, such as a Young coefficient, or by the intensity of the force. The
parameters estimation problem consists in finding for example the right Young
coefficient value in order that the simulation of the beam corresponds to
measurements, including the knowledge of errors.

Simple description of the data assimilation methodological framework
--------------------------------------------------------------------

.. index:: single: background
.. index:: single: background error covariances
.. index:: single: observation error covariances
.. index:: single: covariances
.. index:: single: 3DVAR
.. index:: single: Blue

We can write these features in a simple manner. By default, all variables are
vectors, as there are several parameters to readjust, or a discrete field to
reconstruct.

According to standard notations in data assimilation, we note
:math:`\mathbf{x}^a` the optimal parameters that is to be determined by
calibration, :math:`\mathbf{y}^o` the observations (or experimental
measurements) that we must compare to the simulation outputs,
:math:`\mathbf{x}^b` the background (*a priori* values, or regularization
values) of searched parameters, :math:`\mathbf{x}^t` the unknown ideals
parameters that would give exactly the observations (assuming that the errors
are zero and the model is exact) as output.

In the simplest case, which is static, the steps of simulation and of
observation can be combined into a single observation operator noted :math:`H`
(linear or nonlinear). It transforms the input parameters :math:`\mathbf{x}` to
results :math:`\mathbf{y}`, to be directly compared to observations
:math:`\mathbf{y}^o`:

.. math:: \mathbf{y} = H(\mathbf{x})

Moreover, we use the linearized operator :math:`\mathbf{H}` to represent the
effect of the full operator :math:`H` around a linearization point (and we omit
thereafter to mention :math:`H` even if it is possible to keep it). In reality,
we have already indicated that the stochastic nature of variables is essential,
coming from the fact that model, background and observations are all incorrect.
We therefore introduce errors of observations additively, in the form of a
random vector :math:`\mathbf{\epsilon}^o` such that:

.. math:: \mathbf{y}^o = \mathbf{H} \mathbf{x}^t + \mathbf{\epsilon}^o

The errors represented here are not only those from observation, but also from
the simulation. We can always consider that these errors are of zero mean.
Noting :math:`E[.]` the classical mathematical expectation, we can then define a
matrix :math:`\mathbf{R}` of the observation error covariances by the
expression:

.. math:: \mathbf{R} = E[\mathbf{\epsilon}^o.{\mathbf{\epsilon}^o}^T]

The background can also be written formally as a function of the true value, by
introducing the errors vector :math:`\mathbf{\epsilon}^b` such that:

.. math:: \mathbf{x}^b = \mathbf{x}^t + \mathbf{\epsilon}^b

The errors :math:`\mathbf{\epsilon}^b` are also assumed of zero mean, in the
same manner as for observations. We define the :math:`\mathbf{B}` matrix of
background error covariances by:

.. math:: \mathbf{B} = E[\mathbf{\epsilon}^b.{\mathbf{\epsilon}^b}^T]

The optimal estimation of the true parameters :math:`\mathbf{x}^t`, given the
background :math:`\mathbf{x}^b` and the observations :math:`\mathbf{y}^o`, is
then the "*analysis*" :math:`\mathbf{x}^a` and comes from the minimisation of an
error function, explicit in variational assimilation, or from the filtering
correction in assimilation by filtering.

In **variational assimilation**, in a static case, one classically attempts to
minimize the following function :math:`J`:

.. math:: J(\mathbf{x})=\frac{1}{2}(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+\frac{1}{2}(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

:math:`J` is classically designed as the "*3D-VAR*" functional in data
assimlation (see for example [Talagrand97]_) or as the generalized Tikhonov
regularization functional in optimization (see for example [WikipediaTI]_).
Since :math:`\mathbf{B}` and :math:`\mathbf{R}` covariance matrices are
proportional to the variances of errors, their presence in both terms of the
function :math:`J` can effectively weight the gap terms by the confidence in the
background or observations errors. The parameters vector :math:`\mathbf{x}`
realizing the minimum of this function therefore constitute the analysis
:math:`\mathbf{x}^a`. It is at this level that we have to use the full panoply
of function minimization methods otherwise known in optimization (see also
section `Going further in the state estimation by optimization methods`_).
Depending on the size of the parameters vector :math:`\mathbf{x}` to identify,
and of the availability of gradient or Hessian of :math:`J`, it is appropriate
to adapt the chosen optimization method (gradient, Newton, quasi-Newton...).

In **assimilation by filtering**, in this simple case usually referred to as
"*BLUE*" (for "*Best Linear Unbiased Estimator*"), the :math:`\mathbf{x}^a`
analysis is given as a correction of the background :math:`\mathbf{x}^b` by a
term proportional to the difference between observations :math:`\mathbf{y}^o`
and calculations :math:`\mathbf{H}\mathbf{x}^b`:

.. math:: \mathbf{x}^a = \mathbf{x}^b + \mathbf{K}(\mathbf{y}^o - \mathbf{H}\mathbf{x}^b)

where :math:`\mathbf{K}` is the Kalman gain matrix, which is expressed using
covariance matrices in the following form:

.. math:: \mathbf{K} = \mathbf{B}\mathbf{H}^T(\mathbf{H}\mathbf{B}\mathbf{H}^T+\mathbf{R})^{-1}

The advantage of filtering is to explicitly calculate the gain, to produce then
the *a posteriori* covariance analysis matrix.

In this simple static case, we can show, under an assumption of Gaussian error
distributions (very little restrictive in practice), that the two *variational*
and *filtering* approaches give the same solution.

It is indicated here that these methods of "*3D-VAR*" and "*BLUE*" may be
extended to dynamic problems, called respectively "*4D-VAR*" and "*Kalman
filter*". They can take into account the evolution operator to establish an
analysis at the right time steps of the gap between observations and
simulations, and to have, at every moment, the propagation of the background
through the evolution model. Many other variants have been developed to improve
the numerical quality of the methods or to take into account computer
requirements such as calculation size and time.

Going further in the data assimilation framework
------------------------------------------------

.. index:: single: state estimation
.. index:: single: parameter estimation
.. index:: single: inverse problems
.. index:: single: Bayesian estimation
.. index:: single: optimal interpolation
.. index:: single: mathematical regularization
.. index:: single: regularization methods
.. index:: single: data smoothing

To get more information about the data assimilation techniques, the reader can
consult introductory documents like [Talagrand97]_ or [Argaud09]_, on-line
training courses or lectures like [Bouttier99]_ and [Bocquet04]_ (along with
other materials coming from geosciences applications), or general documents like
[Talagrand97]_, [Tarantola87]_, [Kalnay03]_, [Ide97]_, [Tikhonov77]_ and
[WikipediaDA]_.

Note that data assimilation is not restricted to meteorology or geo-sciences,
but is widely used in other scientific domains. There are several fields in
science and technology where the effective use of observed but incomplete data
is crucial.

Some aspects of data assimilation are also known as *state estimation*,
*parameter estimation*, *inverse problems*, *Bayesian estimation*, *optimal
interpolation*, *mathematical regularization*, *data smoothing*, etc. These
terms can be used in bibliographical searches.

Going further in the state estimation by optimization methods
-------------------------------------------------------------

.. index:: single: state estimation
.. index:: single: optimization methods

As seen before, in a static simulation case, the variational data assimilation
requires to minimize the goal function :math:`J`:

.. math:: J(\mathbf{x})=(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

which is named the "*3D-VAR*" function. It can be seen as a *least squares
minimization* extented form, obtained by adding a regularizing term using
:math:`\mathbf{x}-\mathbf{x}^b`, and by weighting the differences using
:math:`\mathbf{B}` and :math:`\mathbf{R}` the two covariance matrices. The
minimization of the :math:`J` function leads to the *best* :math:`\mathbf{x}`
state estimation. To get more information about these notions, one can consult
reference general documents like [Tarantola87]_.

State estimation possibilities extension, by using more explicitly optimization
methods and their properties, can be imagined in two ways.

First, classical optimization methods involves using various gradient-based
minimizing procedures. They are extremely efficient to look for a single local
minimum. But they require the goal function :math:`J` to be sufficiently regular
and differentiable, and are not able to capture global properties of the
minimization problem, for example: global minimum, set of equivalent solutions
due to over-parametrization, multiple local minima, etc. **A way to extend
estimation possibilities is then to use a whole range of optimizers, allowing
global minimization, various robust search properties, etc**. There is a lot of
minimizing methods, such as stochastic ones, evolutionary ones, heuristics and
meta-heuristics for real-valued problems, etc. They can treat partially
irregular or noisy function :math:`J`, can characterize local minima, etc. The
main drawback is a greater numerical cost to find state estimates, and no
guarantee of convergence in finite time. Here, we only point the following
topics, as the methods are available in the ADAO module: *Quantile Regression*
[WikipediaQR]_ and *Particle Swarm Optimization* [WikipediaPSO]_.

Secondly, optimization methods try usually to minimize quadratic measures of
errors, as the natural properties of such goal functions are well suited for
classical gradient optimization. But other measures of errors can be more
adapted to real physical simulation problems. Then, **an another way to extend
estimation possibilities is to use other measures of errors to be reduced**. For
example, we can cite *absolute error value*, *maximum error value*, etc. These
error measures are not differentiables, but some optimization methods can deal
with:  heuristics and meta-heuristics for real-valued problem, etc. As
previously, the main drawback remain a greater numerical cost to find state
estimates, and no guarantee of convergence in finite time. Here again, we only
point the following methods as it is available in the ADAO module: *Particle
swarm optimization* [WikipediaPSO]_.

The reader interested in the subject of optimization can look at [WikipediaMO]_
as a general entry point.
