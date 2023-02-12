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

.. _section_reference:

================================================================================
**[DocR]** Reference description of the ADAO commands and keywords
================================================================================

The following sections present the reference description of the ADAO commands
and keywords available through the textual interface (TUI), the graphical
interface (GUI) or through scripts. Two first common sections present the
:ref:`section_reference_entry` and the :ref:`section_reference_special_entry`.
After that, one describes successively the
:ref:`section_reference_assimilation` and the
:ref:`section_reference_checking`.

Each command or keyword to be defined through the ADAO TUI or GUI has some
properties. The first property is to be *required*, *optional* or only factual,
describing a type of input. The second property is to be an "open" variable
with a fixed type but with any value allowed by the type, or a "restricted"
variable, limited to some specified values. The embedded case editor GUI having
build-in validating capacities, the properties of the commands or keywords
given through this interface are automatically correct.

.. _section_reference_entry:

================================================================================
**[DocR]** General entries and outputs
================================================================================

This section describes in a very general way the different options of input
types and output variables. The mathematical notations used are explained in
section :ref:`section_theory`.

.. toctree::
   :maxdepth: 1

   ref_entry_types
   ref_options_AlgorithmParameters
   ref_output_variables

.. _section_reference_special_entry:

============================================================================================
**[DocR]** Special entries: measurements, functions, matrices, "*observer*", post-processing
============================================================================================

This section describes special inputs, such as functional or matrix forms, and
the requirements for using them. The mathematical concepts and notations
related to these inputs are explained in section :ref:`section_theory`.

.. toctree::
   :maxdepth: 1

   ref_observations_requirements
   ref_operator_requirements
   ref_covariance_requirements
   ref_observers_requirements
   ref_userpostanalysis_requirements

.. _section_reference_assimilation:

================================================================================
**[DocR]** Data assimilation or optimization calculation cases
================================================================================

This section describes algorithmic choices to use data assimilation methods,
optimization methods or methods with reduction, available in ADAO, detailing
their characteristics and their options.

Some examples on these commands usage are available in the section
:ref:`section_tutorials_in_salome`, in the section
:ref:`section_tutorials_in_python` and in the sample files installed with ADAO.
The mathematical concepts and notations used are explained in the section
:ref:`section_theory`.

.. toctree::
   :maxdepth: 1

   ref_algorithm_3DVAR
   ref_algorithm_4DVAR
   ref_algorithm_Blue
   ref_algorithm_DerivativeFreeOptimization
   ref_algorithm_DifferentialEvolution
   ref_algorithm_EnsembleBlue
   ref_algorithm_EnsembleKalmanFilter
   ref_algorithm_ExtendedBlue
   ref_algorithm_ExtendedKalmanFilter
   ref_algorithm_KalmanFilter
   ref_algorithm_LinearLeastSquares
   ref_algorithm_NonLinearLeastSquares
   ref_algorithm_ParticleSwarmOptimization
   ref_algorithm_QuantileRegression
   ref_algorithm_TabuSearch
   ref_algorithm_UnscentedKalmanFilter
   ref_assimilation_keywords

.. _section_reference_checking:

================================================================================
**[DocR]** Checking cases
================================================================================

This section describes the checking algorithms available in ADAO, detailing
their usage characteristics and their options.

Some examples on these commands usage are available in the section
:ref:`section_tutorials_in_salome`, in the section
:ref:`section_tutorials_in_python` and in the sample files installed with ADAO.
The mathematical concepts and notations used are explained in the section
:ref:`section_theory`.

.. toctree::
   :maxdepth: 1

   ref_algorithm_AdjointTest
   ref_algorithm_ControledFunctionTest
   ref_algorithm_FunctionTest
   ref_algorithm_GradientTest
   ref_algorithm_InputValuesTest
   ref_algorithm_LinearityTest
   ref_algorithm_LocalSensitivityTest
   ref_algorithm_ObserverTest
   ref_algorithm_ParallelFunctionTest
   ref_algorithm_SamplingTest
   ref_algorithm_TangentTest
   ref_checking_keywords

.. _section_reference_task:

================================================================================
**[DocR]** Dedicated tasks or study oriented cases
================================================================================

This section describes the dedicated task or study oriented cases available in
ADAO, detailing their usage characteristics and their options.

These tasks use algorithms from data assimilation methods, optimization methods
or methods with reduction. We refer to the :ref:`section_theory` section and
the :ref:`section_reference_assimilation` section for the underlying
algorithmic details.

.. toctree::
   :maxdepth: 1

   ref_algorithm_EnsembleOfSimulationGenerationTask
   ref_algorithm_MeasurementsOptimalPositioningTask
   ref_task_keywords
