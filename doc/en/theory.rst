..
   Copyright (C) 2008-2025 EDF R&D

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
.. index:: single: EstimationOf
.. index:: single: analysis

**Data Assimilation** is a general well established framework for computing the
optimal estimate of the true state of a system, over time if necessary. It uses
values obtained by combining both observations and *a priori* models, including
information about their errors while simultaneously respecting constraints.
This takes into account the laws of behavior or motion of the system through
the equations of the model, and the way the measurements are physically related
to the variables of the system.

In other words, data assimilation merges measurement data of a system, that are
the observations, with *a priori* system physical and mathematical knowledge,
embedded in numerical models. The goal is to obtain the best possible estimate,
called "*analysis*", of the system real state and of its stochastic properties.
Note that this real state (or "*true state*") cannot usually be reached, but
can only be estimated. Moreover, despite the fact that the used information are
stochastic by nature, data assimilation provides deterministic techniques in
order to perform very efficiently the estimation.

Because data assimilation looks for the **best possible** estimate, its
underlying procedure always integrates optimization in order to find this
estimate: particular optimization methods are always embedded in data
assimilation algorithms. Optimization methods can be seen in ADAO as a way to
extend data assimilation applications. They will be introduced this way in the
section :ref:`section_theory_optimization`, but they are far more general and
can be used without data assimilation concepts.

Two main types of applications exist in data assimilation, which are covered by
the same formalism: **fields reconstruction** (see `Fields reconstruction or
measures interpolation`_) and **parameters identification** (see `Parameters
identification, models adjustment, or calibration`_). These are also referred
to as **state estimation** and **parameters estimation** respectively, and one
can if necessary elaborate joint estimation of both (see `Joint state and
parameter estimation in dynamics`_). In ADAO, some algorithms can be used
either in state estimation or in parameter estimation. This is done simply by
changing the required option "*EstimationOf*" in the algorithm parameters.
Before introducing the :ref:`section_theory_da_framework` in a next section,
these two types of applications are briefly described. At the end, some
detailed information allow :ref:`section_theory_more_assimilation` and
:ref:`section_theory_optimization`, as well as :ref:`section_theory_dynamic`
and having :ref:`section_theory_reduction`.

Fields reconstruction or measures interpolation
-----------------------------------------------

.. index:: single: fields reconstruction
.. index:: single: measures interpolation
.. index:: single: fields interpolation
.. index:: single: state estimation
.. index:: single: background

**Fields reconstruction (or interpolation)** consists in finding, from a
restricted set of real measures, the physical field which is the most
*consistent* with these measures.

This *consistency* is to understand in terms of interpolation, that is to say
that the field we want to reconstruct, using data assimilation on measures, has
to fit at best the measures, while remaining constrained by the overall field
calculation. The calculation is thus an *a priori* estimation of the field that
we seek to identify. One also speaks of **state estimation** in this case.

If the system evolves over time, the reconstruction of the whole field has to
be established at each time step, taking into account the information over a
time window. The interpolation process is more complicated in this case because
it is temporal, and not only in terms of instantaneous field values.

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

Parameters identification, models adjustment, or calibration
------------------------------------------------------------

.. index:: single: parameters identification
.. index:: single: parameters adjustment
.. index:: single: models adjustment
.. index:: single: calibration
.. index:: single: background
.. index:: single: regularization
.. index:: single: inverse problems
.. index:: single: parameters estimation

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

All quantities representing the description of physics in a model are likely to
be calibrated in a data assimilation process, whether they are model
parameters, initial conditions or boundary conditions. Their simultaneous
consideration is greatly facilitated by the data assimilation framework, which
makes it possible to objectively process a heterogeneous set of available
information.

Joint estimation of states and parameters
-----------------------------------------

.. index:: single: joint estimation of states and parameters

It is sometimes necessary, when considering the two previous types of
applications, to need to simultaneously estimate states (fields) and parameters
characterizing a physical phenomenon. This is known as **joint estimation of
states and parameters**.

Without going into the advanced methods to solve this problem, we can mention
the conceptually very simple approach of considering the vector of states to be
interpolated as *augmented* by the vector of parameters to be calibrated. It
can be noted that we are in *state estimation* or *reconstruction of fields*,
and that in the temporal case of parameters identification, the evolution of
the parameters to estimate is simply the identity. The assimilation or
optimization algorithms can then be applied to the augmented vector. Valid for
moderate nonlinearities in the simulation, this simple method extends the
optimization space, and thus leads to larger problems, but it is often possible
to reduce the representation to numerically computable cases. Without
exhaustiveness, the separated variables optimization, the reduced rank
filtering, or the specific treatment of covariance matrices, are common
techniques to avoid this dimension problem. In the temporal case, we will see
below indications for a `Joint state and parameter estimation in dynamics`_.

To go further, we refer to the mathematical methods of optimization and
augmentation developed in many books or specialized articles, finding their
origin for example in [Lions68]_, [Jazwinski70]_ or [Dautray85]_. In particular
in the case of more marked nonlinearities during the numerical simulation of
the states, it is advisable to treat in a more complete but also more complex
way the problem of joint estimation of states and parameters.

.. _section_theory_da_framework:

Simple description of the data assimilation methodological framework
--------------------------------------------------------------------

.. index:: single: analysis
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
observation can be combined into a single observation operator noted
:math:`\mathcal{H}` (linear or nonlinear). It transforms the input parameters
:math:`\mathbf{x}` to results :math:`\mathbf{y}`, to be directly compared to
observations :math:`\mathbf{y}^o`:

.. math:: \mathbf{y} = \mathcal{H}(\mathbf{x})

Moreover, we use the linearized operator :math:`\mathbf{H}` to represent the
effect of the full operator :math:`\mathcal{H}` around a linearization point
(and we will usually omit thereafter to mention :math:`\mathcal{H}`, even if it
is possible to keep it, to mention only :math:`\mathbf{H}`). In reality, we
have already indicated that the stochastic nature of variables is essential,
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

The background can be written formally as a function of the true value, by
introducing the errors vector :math:`\mathbf{\epsilon}^b` such that:

.. math:: \mathbf{x}^b = \mathbf{x}^t + \mathbf{\epsilon}^b

The background errors :math:`\mathbf{\epsilon}^b` are also assumed of zero
mean, in the same manner as for observations. We define the :math:`\mathbf{B}`
matrix of background error covariances by:

.. math:: \mathbf{B} = E[\mathbf{\epsilon}^b.{\mathbf{\epsilon}^b}^T]

The optimal estimation of the true parameters :math:`\mathbf{x}^t`, given the
background :math:`\mathbf{x}^b` and the observations :math:`\mathbf{y}^o`, is
then called an "*analysis*", noted as :math:`\mathbf{x}^a`, and comes from the
minimisation of an error function, explicit in variational assimilation, or
from the filtering correction in assimilation by filtering.

In **variational assimilation**, in a static case, one classically attempts to
minimize the following function :math:`J`:

.. math:: J(\mathbf{x})=\frac{1}{2}(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+\frac{1}{2}(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

:math:`J` is classically designed as the "*3D-Var*" functional in data
assimilation (see for example [Talagrand97]_) or as the generalized Tikhonov
regularization functional in optimization (see for example [WikipediaTI]_).
Since :math:`\mathbf{B}` and :math:`\mathbf{R}` covariance matrices are
proportional to the variances of errors, their presence in both terms of the
function :math:`J` can effectively weight the gap terms by the confidence in
the background or observations errors. The parameters vector :math:`\mathbf{x}`
realizing the minimum of this function therefore constitute the analysis
:math:`\mathbf{x}^a`. It is at this level that we have to use the full panoply
of function minimization methods otherwise known in optimization (see also
section :ref:`section_theory_optimization`). Depending on the size of the
parameters vector :math:`\mathbf{x}` to identify, and of the availability of
gradient or Hessian of :math:`J`, it is appropriate to adapt the chosen
optimization method (gradient, Newton, quasi-Newton...).

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
distributions (very little restrictive in practice) and of :math:`\mathcal{H}`
linearity, that the two *variational* and *filtering* approaches give the same
solution.

It is indicated here that these methods of "*3D-Var*" and "*BLUE*" may be
extended to dynamic or time-related problems, called respectively "*4D-Var*"
and "*Kalman Filter (KF)*" and their derivatives. They have to take into
account an evolution operator to establish an analysis at the right time steps
of the gap between observations and simulations, and to have, at every moment,
the propagation of the background through the evolution model. The next section
provides information on :ref:`section_theory_dynamic`. In
the same way, these methods can be used in case of non linear observation or
evolution operators. Many other variants have been developed to improve the
numerical quality of the methods or to take into account computer requirements
such as calculation size and time.

A schematic view of Data Assimilation and Optimization approaches
-----------------------------------------------------------------

To help the reader get an idea of the approaches that can be used with ADAO in
Data Assimilation and Optimization, we propose here a simplified scheme
describing an arbitrary classification of methods. It is partially and freely
inspired by [Asch16]_ (Figure 1.5).

  .. _meth_steps_in_study:
  .. image:: images/meth_ad_and_opt.png
    :align: center
    :width: 75%
  .. centered::
    **A simplified classification of methods that can be used with ADAO in Data Assimilation and Optimization (acronyms and internal descriptive links are listed below)**

It is deliberately simple to remain readable, the dashed lines showing some of
the simplifications or extensions. For example, it does not specifically
mention the methods with reductions (of which it is given hereafter
:ref:`section_theory_reduction`), some of which were variations of the basic
methods shown here, nor does it mention the more detailed extensions. It also
omits the test methods available in ADAO and useful for the study.

Each method mentioned in this diagram is the subject of a specific descriptive
section in the chapter on :ref:`section_reference_assimilation`. The acronyms
mentioned in the diagram have the meaning indicated in the associated internal
links:

- 3D-Var: :ref:`section_ref_algorithm_3DVAR`,
- 4D-Var: :ref:`section_ref_algorithm_4DVAR`,
- Blue: :ref:`section_ref_algorithm_Blue`,
- DiffEvol : :ref:`section_ref_algorithm_DifferentialEvolution`,
- EKF: :ref:`section_ref_algorithm_ExtendedKalmanFilter`,
- EnKF: :ref:`section_ref_algorithm_EnsembleKalmanFilter`,
- DFO: :ref:`section_ref_algorithm_DerivativeFreeOptimization`,
- Incr-Var: Incremental version Variational optimization,
- KF: :ref:`section_ref_algorithm_KalmanFilter`,
- LLS: :ref:`section_ref_algorithm_LinearLeastSquares`,
- NLLS: :ref:`section_ref_algorithm_NonLinearLeastSquares`,
- QR: :ref:`section_ref_algorithm_QuantileRegression`,
- Swarm: :ref:`section_ref_algorithm_ParticleSwarmOptimization`,
- Tabu: :ref:`section_ref_algorithm_TabuSearch`,
- UKF: :ref:`section_ref_algorithm_UnscentedKalmanFilter`.

.. _section_theory_reduction:

An overview of reduction methods and of reduced optimization
------------------------------------------------------------

.. index:: single: reduction
.. index:: single: reduction methods
.. index:: single: reduced methods
.. index:: single: reduced space
.. index:: single: neutral sub-space
.. index:: single: SVD
.. index:: single: POD
.. index:: single: PCA
.. index:: single: Kahrunen-Loeve
.. index:: single: RBM
.. index:: single: ROM
.. index:: single: EIM
.. index:: single: Fourier
.. index:: single: wavelets
.. index:: single: EOF
.. index:: single: sparse

Data assimilation and optimization approaches always imply a certain amount of
reiteration of a unitary numerical simulation representing the physics that is
to be treated. In order to handle this physics as well as possible, this
elementary numerical simulation is often of large size, even huge, and leads to
an extremely high computational cost when it is repeated. The complete physical
simulation is often called "*high fidelity simulation*" (or "*full scale
simulation*").

To avoid this practical challenge, **different strategies to reduce the cost of
the optimization calculation exist, and some of them also allow to control the
numerical error implied by this reduction**. These strategies are seamlessly
integrated into some of the ADAO methods or are the purpose of special
algorithms.

To establish such an approach, one seeks to reduce at least one of the
ingredients that make up the data assimilation or optimization problem. One can
thus classify the reduction methods according to the ingredient on which they
operate, knowing that some methods deal with several of them. A rough
classification is provided here, which the reader can complete by reading
general mathematical books or articles, or those specialized in his physics.

Reduction of data assimilation or optimization algorithms:
    the optimization algorithms themselves can generate significant
    computational costs to process numerical information. Various methods can
    be used to reduce their algorithmic cost, for example by working in the
    most suitable reduced space for optimization, or by using multi-level
    optimization techniques. ADAO has such techniques that are included in
    variants of classical algorithms, leading to exact or approximate but
    numerically more efficient resolutions. By default, the algorithmic options
    chosen in ADAO are always the most efficient when they do not impact the
    quality of the optimization.

Reduction of the representation of covariances:
    in data assimilation algorithms, covariances are the most expensive
    quantities to handle or to store, often becoming the limiting quantities
    from the point of view of the computational cost. Many methods try to use a
    reduced representation of these matrices (leading sometimes but not
    necessarily to reduce the dimension of the optimization space).
    Classically, factorization, decomposition (spectral, Fourier, wavelets...)
    or ensemble estimation (EOF...) techniques, or combinations, are used to
    reduce the numerical load of these covariances in the computations. ADAO
    uses some of these techniques, in combination with sparse computation
    techniques, to make the handling of covariance matrices more efficient.

Reduction of the physical model:
    the simplest way to reduce the cost of the unit calculation consists in
    reducing the simulation model itself, by representing it in a more economic
    way. Numerous methods allow this reduction of models by ensuring a more or
    less rigorous control of the approximation error generated by the
    reduction. The use of simplified models of the physics allows a reduction
    but without always producing an error control. On the contrary, all
    decomposition methods (Fourier, wavelets, SVD, POD, PCA, Kahrunen-Loeve,
    RBM, EIM, etc.) aim at a reduction of the representation space with an
    explicit error control. Although they are very frequently used, they must
    nevertheless be completed by a fine analysis of the interaction with the
    optimization algorithm in which the reduced computation is inserted, in
    order to avoid instabilities, discrepancies or inconsistencies that are
    notoriously harmful. ADAO fully supports the use of this type of reduction
    method, even if it is often necessary to establish this generic independent
    reduction prior to the optimization.

Reduction of the data assimilation or optimization space:
    the size of the optimization space depends greatly on the type of problem
    treated (estimation of states or parameters) but also on the number of
    observations available to conduct the data assimilation. It is therefore
    sometimes possible to conduct the optimization in the smallest space by
    adapting the internal formulation of the optimization algorithms. When it
    is possible and judicious, ADAO integrates this kind of reduced formulation
    to improve the numerical performance without reducing the quality of the
    optimization.

Combining multiple reductions:
    many advanced algorithms seek to combine multiple reduction techniques
    simultaneously. However, it is difficult to have both generic and robust
    methods, and to use several very efficient reduction techniques at the same
    time. ADAO integrates some of the most robust methods, but this aspect is
    still largely the subject of research and development.

One can end this quick overview of reduction methods highlighting that their
use is ubiquitous in real applications and in numerical tools, and that ADAO
allows to use proven methods without even knowing it.

.. _section_theory_more_assimilation:

Going further in the data assimilation framework
------------------------------------------------

.. index:: single: adjustment
.. index:: single: artificial intelligence
.. index:: single: Bayesian estimation
.. index:: single: calibration
.. index:: single: data smoothing
.. index:: single: data-driven
.. index:: single: field interpolation
.. index:: single: inverse problems
.. index:: single: inversion
.. index:: single: machine learning
.. index:: single: mathematical regularization
.. index:: single: meta-heuristics
.. index:: single: model reduction
.. index:: single: optimal interpolation
.. index:: single: parameter adjustment
.. index:: single: parameter estimation
.. index:: single: quadratic optimization
.. index:: single: regularization methods
.. index:: single: state estimation
.. index:: single: variational optimization

To get more information about the data assimilation techniques, the reader can
consult introductory documents like [Talagrand97]_ or [Argaud09]_, on-line
training courses or lectures like [Bouttier99]_ and [Bocquet04]_ (along with
other materials coming from geosciences applications), or general documents
like [Talagrand97]_, [Tarantola87]_, [Asch16]_, [Kalnay03]_, [Ide97]_,
[Tikhonov77]_ and [WikipediaDA]_. In a more mathematical way, one can also
consult [Lions68]_, [Jazwinski70]_.

Note that data assimilation is not restricted to meteorology or geo-sciences,
but is widely used in other scientific domains. There are several fields in
science and technology where the effective use of observed but incomplete data
is crucial.

Some aspects of data assimilation are also known by other names. Without being
exhaustive, we can mention the names of *calibration*, *adjustment*, *state
estimation*, *parameter estimation*, *parameter adjustment*, *inverse problems*
or *inversion*, *Bayesian estimation*, *field interpolation* or *optimal
interpolation*, *variational optimization*, *quadratic optimization*,
*mathematical regularization*, *meta-heuristics for optimization*, *model
reduction*, *data smoothing*, *data-driven* modeling, model and data learning
(*Machine Learning* and *Artificial Intelligence*), etc. These terms can be
used in bibliographic searches.

.. _section_theory_optimization:

Going further in the state estimation by optimization methods
-------------------------------------------------------------

.. index:: single: state estimation
.. index:: single: optimization methods
.. index:: single: Local optimization
.. index:: single: Global optimization
.. index:: single: DerivativeFreeOptimization
.. index:: single: ParticleSwarmOptimization
.. index:: single: DifferentialEvolution
.. index:: single: QuantileRegression
.. index:: single: QualityCriterion

As seen before, in a static simulation case, the variational data assimilation
requires to minimize the goal function :math:`J`:

.. math:: J(\mathbf{x})=\frac{1}{2}(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+\frac{1}{2}(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

which is named the "*3D-Var*" objective function. It can be seen as a *least
squares minimization* extended form, obtained by adding a regularizing term
using :math:`\mathbf{x}-\mathbf{x}^b`, and by weighting the differences using
:math:`\mathbf{B}` and :math:`\mathbf{R}` the two covariance matrices. The
minimization of the :math:`J` function leads to the *best* :math:`\mathbf{x}`
state estimation. To get more information about these notions, one can consult
reference general documents like [Tarantola87]_.

State estimation possibilities extension, by using more explicitly optimization
methods and their properties, can be imagined in two ways.

First, classical optimization methods often involves using various
gradient-based minimizing procedures. They are extremely efficient to look for
a single local minimum. But they require the goal function :math:`J` to be
sufficiently regular and differentiable, and are not able to capture global
properties of the minimization problem, for example: global minimum, set of
equivalent solutions due to over-parametrization, multiple local minima, etc.
**An approach to extend estimation possibilities is then to use a whole range of
optimizers, allowing global minimization, various robust search properties,
etc**. There is a lot of minimizing methods, such as stochastic ones,
evolutionary ones, heuristics and meta-heuristics for real-valued problems,
etc. They can treat partially irregular or noisy function :math:`J`, can
characterize local minima, etc. The main drawbacks are a greater numerical cost
to find state estimates, and often a lack of guarantee of convergence in finite
time. Here, we only point the following topics, as the methods are available in
ADAO:

- *Derivative Free Optimization (or DFO)* (see :ref:`section_ref_algorithm_DerivativeFreeOptimization`),
- *Particle Swarm Optimization (or PSO)* (see :ref:`section_ref_algorithm_ParticleSwarmOptimization`),
- *Differential Evolution (or DE)* (see :ref:`section_ref_algorithm_DifferentialEvolution`),
- *Quantile Regression (or QR)* (see :ref:`section_ref_algorithm_QuantileRegression`).

Secondly, optimization methods try usually to minimize quadratic measures of
errors, as the natural properties of such goal functions are well suited for
classical gradient optimization. But other measures of errors can be more
adapted to real physical simulation problems. Then, **an another way to extend
estimation possibilities is to use other measures of errors to be reduced**.
For example, we can cite *absolute error value*, *maximum error value*, etc.
The most classical instances of error measurements are recalled or specified
below, indicating their identifiers in ADAO for the possible selection of a
quality criterion:

- the objective function for the augmented weighted least squares error measurement (which is the basic default functional in all data assimilation algorithms, often named "*3D-Var*" objective function, and which is known in the quality criteria for ADAO as "*AugmentedWeightedLeastSquares*", "*AWLS*" or "*DA*") is:

    .. index:: single: AugmentedWeightedLeastSquares (QualityCriterion)
    .. index:: single: AWLS (QualityCriterion)
    .. math:: J(\mathbf{x})=\frac{1}{2}(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+\frac{1}{2}(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

- the objective function for the weighted least squares error measurement (which is the squared :math:`L^2` weighted norm of the innovation, with a :math:`1/2` coefficient to be homogeneous with the previous one, and which is known in the quality criteria for ADAO as "*WeightedLeastSquares*" or "*WLS*") is:

    .. index:: single: WeightedLeastSquares (QualityCriterion)
    .. index:: single: WLS (QualityCriterion)
    .. math:: J(\mathbf{x})=\frac{1}{2}(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

- the objective function for the least squares error measurement (which is the squared :math:`L^2` norm of the innovation, with a :math:`1/2` coefficient to be homogeneous with the previous ones, and which is known in the quality criteria for ADAO as "*LeastSquares*", "*LS*" or "*L2*") is:

    .. index:: single: LeastSquares (QualityCriterion)
    .. index:: single: LS (QualityCriterion)
    .. index:: single: L2 (QualityCriterion)
    .. math:: J(\mathbf{x})=\frac{1}{2}(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})=\frac{1}{2}||\mathbf{y}^o-\mathbf{H}.\mathbf{x}||_{L^2}^2

- the objective function for the absolute error value measurement (which is the :math:`L^1` norm of the innovation, and which is known in the quality criteria for ADAO as "*AbsoluteValue*" or "*L1*") is:

    .. index:: single: AbsoluteValue (QualityCriterion)
    .. index:: single: L1 (QualityCriterion)
    .. math:: J(\mathbf{x})=||\mathbf{y}^o-\mathbf{H}.\mathbf{x}||_{L^1}

- the objective function for the maximum error value measurement (which is the :math:`L^{\infty}` norm, and which is known in the quality criteria for ADAO as "*MaximumError*", "*ME*" or "*Linf*") is:

    .. index:: single: MaximumError (QualityCriterion)
    .. index:: single: ME (QualityCriterion)
    .. index:: single: Linf (QualityCriterion)
    .. math:: J(\mathbf{x})=||\mathbf{y}^o-\mathbf{H}.\mathbf{x}||_{L^{\infty}}

These error measures may be not differentiable for the last two, but some
optimization methods can still handle them:  heuristics and meta-heuristics for
real-valued problem, etc. As previously, the main drawback remain a greater
numerical cost to find state estimates, and often a lack of guarantee of
convergence in finite time. Here again, we only point the following methods as
it is available in the ADAO module:

- *Derivative Free Optimization (or DFO)* (see :ref:`section_ref_algorithm_DerivativeFreeOptimization`),
- *Particle Swarm Optimization (or PSO)* (see :ref:`section_ref_algorithm_ParticleSwarmOptimization`),
- *Differential Evolution (or DE)* (see :ref:`section_ref_algorithm_DifferentialEvolution`).

The reader interested in the subject of optimization can look at [WikipediaMO]_
as a general entry point.

.. _section_theory_dynamic:

Going further in data assimilation for dynamics
-----------------------------------------------

.. index:: single: dynamic (system)
.. index:: single: system dynamic
.. index:: single: temporal evolution
.. index:: single: ODE (Ordinary Differential Equation)
.. index:: single: EstimationOf

We can analyze a system in temporal evolution (dynamics) with the help of data
assimilation, in order to explicitly take into account the flow of time in the
estimation of states or parameters. We briefly introduce here the problematic,
and some theoretical or practical tools, to facilitate the user treatment of
such situations. It is nevertheless indicated that the variety of physical and
user problems is large, and that it is therefore recommended to adapt the
treatment to the constraints, whether they are physical, numerical or
computational.

General form of dynamic systems
+++++++++++++++++++++++++++++++

Systems in temporal evolution can be studied or represented using dynamic
systems. In this case, it is easy to conceive the analysis of their behavior
with the help of data assimilation (it is even in this precise case that the
data assimilation approach was initially widely developed).

We formalize the numerical simulation framework in a simple way. A simple
dynamic system dynamic system on the state :math:`\mathbf{x}` can be described
in continuous time in the form:

.. math:: \forall t \in \mathbb{R}^{+}, \frac{d\mathbf{x}}{dt} = \mathcal{D}(\mathbf{x},\mathbf{u},t)

where :math:`\mathbf{x}` is the unknown state vector, :math:`\mathbf{u}` is a
known external control vector, and :math:`\mathcal{D}` is the (possibly
non-linear) operator of the system dynamics. It is an Ordinary Differential
Equation (ODE), of the first order, on the state. In discrete time, this
dynamical system can be written in the following form:

.. math:: \forall n \in \mathbb{N}, \mathbf{x}_{n+1} = M(\mathbf{x}_{n},\mathbf{u}_{n},t_n\rightarrow t_{n+1})

for an indexing :math:`t_n` of discrete times with :math:`n\in\mathbf{N}`.
:math:`M` is the discrete evolution operator, symbolically obtained from
:math:`\mathcal{D}` by the discretization scheme. Usually, we omit the time
notation in the evolution operator :math:`M`. Approximating the
:math:`\mathcal{D}` operator by :math:`M` introduces (or adds, if it already
exists) a :math:`\epsilon` model error.

We can then characterize two types of estimates in dynamics, which we describe
hereafter on the discrete time dynamical system: `State estimation in
dynamics`_ and `Parameter estimation in dynamics`_. Combined, the two types can
be used to make a `Joint state and parameter estimation in dynamics`_. In ADAO,
some algorithms can be used either in state estimation or in parameter
estimation. This is done simply by changing the required option
"*EstimationOf*" in the algorithm parameters.

State estimation in dynamics
++++++++++++++++++++++++++++

The state estimation can be conducted by data assimilation on the discrete time
version of the dynamical system, written in the following form:

.. math:: \mathbf{x}_{n+1} = M(\mathbf{x}_{n},\mathbf{u}_{n}) + \mathbf{\epsilon}_{n}

.. math:: \mathbf{y}_{n} = H(\mathbf{x}_{n}) + \mathbf{\nu}_{n}

where :math:`\mathbf{x}` is the system state to be estimated,
:math:`\mathbf{x}_{n}` and :math:`\mathbf{y}_{n}` are respectively the
computed (unobserved) and measured (observed) state of the system, :math:`M`
and :math:`H` are the incremental evolution and observation operators,
respectively, :math:`\mathbf{\epsilon}_{n}` and :math:`\mathbf{\nu}_{n}` are
the evolution and observation noise or error, respectively, and
:math:`\mathbf{u}_{n}` is a known external control. The two operators :math:`M`
and :math:`H` are directly usable in data assimilation with ADAO.

Parameter estimation in dynamics
++++++++++++++++++++++++++++++++

The parameter estimation can be written a differently to be solved by data
assimilation. Still on the discrete time version of the dynamical system, we
look for a nonlinear :math:`G` mapping, parameterized by :math:`\mathbf{a}`,
between inputs :math:`\mathbf{x}_{n}` and measurements :math:`\mathbf{y}_{n}`
at each step :math:`t_n`, the error to be controlled as a function of
parameters :math:`\mathbf{y}_{n}` being
:math:`\mathbf{y}_{n}-G(\mathbf{x}_{n},\mathbf{a})`. We can proceed by
optimization on this error, with regularization, or by filtering by writing the
problem represented in state estimation:

.. math:: \mathbf{a}_{n+1} = \mathbf{a}_{n} + \mathbf{\epsilon}_{n}

.. math:: \mathbf{y}_{n} = G(\mathbf{x}_{n},\mathbf{a}_{n}) + \mathbf{\nu}_{n}

where, this time, the choice of the evolution and observation error models
:math:`\mathbf{\epsilon}_{n}` and :math:`\mathbf{\nu}_{n}` condition the
performance of convergence and observation tracking (while the error
representations come from the behavior of the physics in the case of state
estimation). The estimation of the parameters :math:`\mathbf{a}` is done by
using pairs :math:`(\mathbf{x}_{n},\mathbf{y}_{n})` of corresponding inputs and
outputs. Moreover, the error functionals are based on the difference between
the input estimate and the output estimate.

In this case of parameter estimation, in order to apply data assimilation
methods, we therefore impose the hypothesis that the evolution operator is the
identity (*Note: it is therefore not used, but must be declared in ADAO, for
example as a 1 matrix*), and the observation operator is :math:`G`.

Joint state and parameter estimation in dynamics
++++++++++++++++++++++++++++++++++++++++++++++++

A special case concerns the joint estimation of state and parameters used in a
dynamic system. One seeks to jointly estimate the state :math:`\mathbf{x}`
(which depends on time) and the parameters :math:`\mathbf{a}` (which here does
not depend on time). There are several ways to deal with this problem, but the
most general one is to use a state vector augmented by the parameters, and to
extend the operators accordingly.

To do this, using the notations of the previous two subsections, we define the
auxiliary variable :math:`\mathbf{w}` such that:

.. math:: \mathbf{w} = \left[
    \begin{array}{c}
    \mathbf{x} \\
    \mathbf{a}
    \end{array}
    \right]
    = \left[
    \begin{array}{c}
    \mathbf{w}_{|x} \\
    \mathbf{w}_{|a}
    \end{array}
    \right]

and the operators of evolution :math:`\tilde{M}` and observation
:math:`\tilde{H}` associated to the augmented problem:

.. math:: \tilde{M}(\mathbf{w},\mathbf{u}) = \left[
    \begin{array}{c}
    M(\mathbf{w}_{|x},\mathbf{u}) \\
    \mathbf{w}_{|a}
    \end{array}
    \right]
    = \left[
    \begin{array}{c}
    M(\mathbf{x},\mathbf{u}) \\
    \mathbf{a}
    \end{array}
    \right]

.. math:: \tilde{H}(\mathbf{w}) = \left[
    \begin{array}{c}
    H(\mathbf{w}_{|x}) \\
    G(\mathbf{w}_{|x},\mathbf{w}_{|a})
    \end{array}
    \right]
    = \left[
    \begin{array}{c}
    H(\mathbf{x}) \\
    G(\mathbf{x},\mathbf{a})
    \end{array}
    \right]

With these notations, by extending the noise variables
:math:`\mathbf{\epsilon}` and :math:`\mathbf{\nu}` appropriately, the joint
state :math:`\mathbf{x}` and parameters :math:`\mathbf{a}` discrete-time
estimation problem, using the joint variable :math:`\mathbf{w}`, is then
written:

.. math:: \mathbf{w}_{n+1} = \tilde{M}(\mathbf{w}_{n},\mathbf{u}_{n}) + \mathbf{\epsilon}_{n}

.. math:: \mathbf{y}_{n} = \tilde{H}(\mathbf{w}_{n}) + \mathbf{\nu}_{n}

where :math:`\mathbf{w}_{n}=[\mathbf{x}_n~~\mathbf{a}_n]^T`. The incremental
evolution and observation operators are therefore respectively the augmented
operators :math:`\tilde{M}` and :math:`\tilde{H}`, and are directly suitable
for study cases with ADAO.

Conceptual scheme for data assimilation in dynamics
+++++++++++++++++++++++++++++++++++++++++++++++++++

To complete the description, we can represent the data assimilation process in
a dynamics specific way using a temporal scheme, which describes the action of
the evolution (:math:`M` or :math:`\tilde{M}`) and observation (:math:`H` or
:math:`\tilde{H}`) operators during the discrete simulation and the recursive
estimation of the state (:math:`\mathbf{x}`). A possible representation is as
follows, particularly appropriate for iterative Kalman filtering algorithms:

  .. _schema_d_AD_temporel:
  .. figure:: images/schema_temporel_KF.png
    :align: center
    :width: 100%

    **Timeline of steps for data assimilation operators in dynamics**

with **P** the state error covariance and *t* the discrete iterative time. In
this scheme, the analysis **(x,P)** is obtained by means of the "*correction*"
by observing the "*prediction*" of the previous state. Another way of
understanding data assimilation in dynamics, by observing the states in the
measurement space, is to represent the same sequential assimilation process as
in the previous figure in the following form:

  .. _schema_d_AD_sequentiel:
  .. figure:: images/schema_temporel_sequentiel.png
    :align: center
    :width: 100%

    **Sequential scheme of states and measures for data assimilation in dynamics**

The concepts described in this diagram can be directly and simply used in ADAO
to understand and elaborate study cases, and are included in the description
and the examples of some algorithms.
