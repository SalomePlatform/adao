..
   Copyright (C) 2008-2026 EDF R&D

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

.. _section_ref_sampling_requirements:

Requirements for describing a state sampling
--------------------------------------------

.. index:: single: SamplingTest
.. index:: single: State sampling
.. index:: single: Sampling

In general, it is useful to have a sampling of states when you are interested
in analyses that benefit from knowledge of a set of simulations or a set of
similar measurements, but each obtained for a different state.

This is the case for the explicit definition of simulatable states of
:ref:`section_ref_algorithm_SamplingTest`,
:ref:`section_ref_algorithm_EnsembleOfSimulationGenerationTask` and
:ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`.

All these states can be described explicitly or implicitly, to simplify their
listing. Various possible descriptions are given below, followed by very simple
examples to show the types of state distribution obtained in the space.

Explicit or implicit description of the state sampling collection
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The state sampling collection can be described using dedicated keywords in the
command set of an algorithm that requires it.

The sampling of the states :math:`\mathbf{x}` can be provided explicitly or in
the form of hypercubes, explicit or sampled according to common distributions,
or using Latin Hypercube Sampling (LHS) or Sobol sequences. Depending on the
method, the sample will be included in the domain described by its bounds, or
will come from the description of the unbounded domain of state variables.

These possible keywords are:

.. include:: snippets/SampleAsExplicitHyperCube.rst

.. include:: snippets/SampleAsIndependentRandomVariables.rst

.. include:: snippets/SampleAsIndependentRandomVectors.rst

.. include:: snippets/SampleAsMinMaxLatinHyperCube.rst

.. include:: snippets/SampleAsMinMaxSobolSequence.rst

.. include:: snippets/SampleAsMinMaxStepHyperCube.rst

.. include:: snippets/SampleAsnUplet.rst

Beware of the size of the implicit hypercube (and then to the number of
computations) that can be reached, it can grow quickly to be quite large.

Simple examples of state-space distributions
++++++++++++++++++++++++++++++++++++++++++++

To illustrate the commands, we propose here simple state distributions obtained
in a 2-dimensional state space (to be representable), and the commands that
enable them to be obtained. We arbitrarily choose to place 25 states in each
case. In most of the commands, since the states are described separately
according to each coordinate, 5 coordinate values are requested per axis.

The first three keywords illustrate the same distribution, as they are simply
different ways of describing it.

Explicit state distribution by keyword "*SampleAsnUplet*"
.........................................................

Explicit sample generation command by "*SampleAsnUplet*" is as follows:

.. code-block:: python

    [...]
    "SampleAsnUplet":[[0, 0], [0, 1], [0, 2], [0, 3], [0, 4],
                      [1, 0], [1, 1], [1, 2], [1, 3], [1, 4],
                      [2, 0], [2, 1], [2, 2], [2, 3], [2, 4],
                      [3, 0], [3, 1], [3, 2], [3, 3], [3, 4],
                      [4, 0], [4, 1], [4, 2], [4, 3], [4, 4]]
    [...]

La répartition des états ainsi décrite correspond à l'illustration  :

  .. image:: images/sampling_01_SampleAsnUplet.png
    :align: center

Note: here we've chosen an ordered distribution, similar to those we'll obtain
much more synthetically with some of the following commands, precisely to
illustrate this point.

Implicit state distribution by keyword "*SampleAsExplicitHyperCube*"
....................................................................

Implicit sample generation command by "*SampleAsExplicitHyperCube*" is as
follows:

.. code-block:: python

    [...]
    "SampleAsExplicitHyperCube":[[0, 1, 2, 3, 4], [0, 1, 2, 3, 4]]
    # ou
    "SampleAsExplicitHyperCube":[range(0, 5), range(0, 5)]
    [...]

The distribution of states thus described corresponds to the illustration:

  .. image:: images/sampling_02_SampleAsExplicitHyperCube.png
    :align: center

Implicit state distribution by keyword "*SampleAsMinMaxStepHyperCube*"
......................................................................

Implicit sample generation command by "*SampleAsMinMaxStepHyperCube*" is as
follows:

.. code-block:: python

    [...]
    "SampleAsMinMaxStepHyperCube":[[0, 4, 1], [0, 4, 1]]
    [...]

The distribution of states thus described corresponds to the illustration:

  .. image:: images/sampling_03_SampleAsMinMaxStepHyperCube.png
    :align: center

Implicit state distribution by keyword "*SampleAsMinMaxLatinHyperCube*"
.......................................................................

Implicit sample generation command by "*SampleAsMinMaxLatinHyperCube*", in
dimension 2 et and with 25 points, is as follows:

.. code-block:: python

    [...]
    "SampleAsMinMaxLatinHyperCube":[[0, 4], [0, 4], [2, 25]]
    [...]

The distribution of states thus described corresponds to the illustration:

  .. image:: images/sampling_04_SampleAsMinMaxLatinHyperCube.png
    :align: center

Implicit state distribution by keyword "*SampleAsMinMaxSobolSequence*"
.......................................................................

Implicit sample generation command by "*SampleAsMinMaxSobolSequence*", in
dimension 2 et and with 25 points, is as follows:

.. code-block:: python

    [...]
    "SampleAsMinMaxSobolSequence":[[0, 4], [0, 4], [2, 25]]
    [...]

The distribution of states (there will be 32 here by construction principle of
the Sobol sequence) thus described corresponds to the illustration:

  .. image:: images/sampling_05_SampleAsMinMaxSobolSequence.png
    :align: center

Implicit state distribution by keyword "*SampleAsIndependentRandomVariables*" with normal laws
..............................................................................................

Implicit sample generation command by "*SampleAsIndependentRandomVariables*" is as
follows, using a normal distribution (1,1) by coordinate:

.. code-block:: python

    [...]
    "SampleAsIndependentRandomVariables":[['normal', [1, 1], 5], ['normal', [1, 1], 5]]
    [...]

The distribution of states thus described corresponds to the illustration:

  .. image:: images/sampling_06_SampleAsIndependentRandomVariables_normal.png
    :align: center

Implicit state distribution by keyword "*SampleAsIndependentRandomVariables*" with log-normal laws
..................................................................................................

Implicit sample generation command by "*SampleAsIndependentRandomVariables*" is
as follows, using a log-normal distribution (1,1) (i.e. whose logarithmic
distribution is normal) by coordinate:

.. code-block:: python

    [...]
    "SampleAsIndependentRandomVariables":[['lognormal', [1, 1], 5], ['lognormal', [1, 1], 5]]
    [...]

The distribution of states thus described corresponds to the illustration:

  .. image:: images/sampling_07_SampleAsIndependentRandomVariables_lognormal.png
    :align: center

Implicit state distribution by keyword "*SampleAsIndependentRandomVariables*" with uniform laws
...............................................................................................

Implicit sample generation command by "*SampleAsIndependentRandomVariables*" is
as follows, using a uniform distribution between 0.01 and 1 for coordinate
distribution:

.. code-block:: python

    [...]
    "SampleAsIndependentRandomVariables":[['uniform', [0.01, 1], 5], ['uniform', [0.01, 1], 5]]
    [...]

The distribution of states thus described corresponds to the illustration:

  .. image:: images/sampling_08_SampleAsIndependentRandomVariables_uniform.png
    :align: center

Implicit state distribution by keyword "*SampleAsIndependentRandomVariables*" with log-uniform laws
...................................................................................................

Implicit sample generation command by "*SampleAsIndependentRandomVariables*" is
as follows, using a uniform distribution between 0.01 and 1 (i.e. whose
logarithmic distribution is uniform) for coordinate distribution:

.. code-block:: python

    [...]
    "SampleAsIndependentRandomVariables":[['loguniform', [0.01, 1], 5], ['loguniform', [0.01, 1], 5]]
    [...]

The distribution of states thus described corresponds to the illustration:

  .. image:: images/sampling_09_SampleAsIndependentRandomVariables_loguniform.png
    :align: center

Implicit state distribution by keyword "*SampleAsIndependentRandomVariables*" with Weibull laws
...............................................................................................

Implicit sample generation command by "*SampleAsIndependentRandomVariables*" is
as follows, using a 1-parameter Weibull distribution of value 5 for coordinate
distribution:

.. code-block:: python

    [...]
    "SampleAsIndependentRandomVariables":[['weibull', [5], 5], ['weibull', [5], 5]]
    [...]

The distribution of states thus described corresponds to the illustration:

  .. image:: images/sampling_10_SampleAsIndependentRandomVariables_weibull.png
    :align: center

Implicit state distribution by keyword "*SampleAsIndependentRandomVectors*" with normal laws
............................................................................................

The implicit command for generating samples of independent vectors by
"*SampleAsIndependentRandomVectors*" is as follows, in dimension 2 and with 25
points, using a normal distribution (1,1) for each coordinate:

.. code-block:: python

    [...]
    "SampleAsIndependentRandomVectors":[['normal', [1, 1]], ['normal', [1, 1]], [2, 25]]
    [...]

The distribution of states thus described corresponds to the illustration:

  .. image:: images/sampling_11_SampleAsIndependentRandomVectors_normal.png
    :align: center

Implicit state distribution by keyword "*SampleAsIndependentRandomVectors*" with log-normal laws
................................................................................................

The implicit command for generating samples of independent vectors by
"*SampleAsIndependentRandomVectors*" is as follows, in dimension 2 and with 25
points, using a log-normal distribution (1,1) (i.e. whose logarithmic
distribution is normal) for each coordinate:

.. code-block:: python

    [...]
    "SampleAsIndependentRandomVectors":[['lognormal', [1, 1]], ['lognormal', [1, 1]], [2, 25]]
    [...]

The distribution of states thus described corresponds to the illustration:

  .. image:: images/sampling_12_SampleAsIndependentRandomVectors_lognormal.png
    :align: center

Implicit state distribution by keyword "*SampleAsIndependentRandomVectors*" with uniform laws
.............................................................................................

The implicit command for generating samples of independent vectors by
"*SampleAsIndependentRandomVectors*" is as follows, in dimension 2 and with 25
points, using a uniform distribution between 0.01 and 1 for each coordinate:

.. code-block:: python

    [...]
    "SampleAsIndependentRandomVectors":[['normal', [0.01, 1]], ['normal', [0.01, 1]], [2, 25]]
    [...]

The distribution of states thus described corresponds to the illustration:

  .. image:: images/sampling_13_SampleAsIndependentRandomVectors_uniform.png
    :align: center

Implicit state distribution by keyword "*SampleAsIndependentRandomVectors*" with log-uniform laws
.................................................................................................

The implicit command for generating samples of independent vectors by
"*SampleAsIndependentRandomVectors*" is as follows, in dimension 2 and with 25
points, using a log-uniform distribution (i.e. whose logarithmic distribution
is uniform) between 0.01 and 1 for each coordinate:

.. code-block:: python

    [...]
    "SampleAsIndependentRandomVectors":[['lognormal', [1, 1]], ['lognormal', [1, 1]], [2, 25]]
    [...]

The distribution of states thus described corresponds to the illustration:

  .. image:: images/sampling_14_SampleAsIndependentRandomVectors_loguniform.png
    :align: center

Implicit state distribution by keyword "*SampleAsIndependentRandomVectors*" with Weibull laws
.............................................................................................

The implicit command for generating samples of independent vectors by
"*SampleAsIndependentRandomVectors*" is as follows, in dimension 2 and with 25
points, using a 1-parameter Weibull distribution of value 5 for coordinate
distribution:

.. code-block:: python

    [...]
    "SampleAsIndependentRandomVectors":[['weibull', [5]], ['weibull', [5]], [2, 25]]
    [...]

The distribution of states thus described corresponds to the illustration:

  .. image:: images/sampling_15_SampleAsIndependentRandomVectors_weibull.png
    :align: center

