..
   Copyright (C) 2008-2021 EDF R&D

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

.. _section_glossary:

Glossary
========

.. glossary::
   :sorted:

   case
      One ADAO case is defined by a set of data and of choices, packed together
      through the user interface of the module. The data are physical
      measurements that have technically to be available before or during the
      case execution. The simulation code(s) and the data assimilation or
      optimization method, and their parameters, has to be chosen, they define
      the execution properties of the case.

   iteration
      One iteration occurs when using iterative optimizers (e.g. 3DVAR), and it
      is entirely hidden in the main YACS OptimizerLoop Node named
      "*compute_bloc*". Nevertheless, the user can watch the iterative process
      through the "*YACS Container Log*" window, which is updated during the
      process, and using "*Observers*" attached to calculation variables.

   physical system
      This is the object of study that will be represented by numerical
      simulation and observed by measurements.

   digital simulator
      All the numerical relationships and equations characterizing the physical
      system studied.

   numerical simulation
      Computational implementation of the set composed of the numerical
      simulator and a particular set of all the input and control variables of
      the simulator. These variables enable the digital simulator to be able to
      numerically represent the system's behaviour.

   observations or measurements
      These are quantities that come from measuring instruments and
      characterize the physical system to be studied. These quantities can vary
      in space or time, can be punctual or integrated. They are themselves
      characterized by their measurement nature, size, etc.

   observation operator
      It is a transformation of the simulated state into a set of quantities
      explicitly comparable to the observations.

   boundary conditions
      These are particular input and control variables of the simulator, which
      characterize the description of the system's behaviour at the border of
      the simulation spatial domain.

   initial conditions
      These are specific simulator input and control variables that
      characterize the description of the system's behavior at the initial edge
      of the simulation time domain.

   APosterioriCovariance
      Keyword to indicate the covariance matrix of *a posteriori* analysis
      errors.

   APosterioriCorrelations
      Keyword to indicate the correlation matrix of *a posteriori* analysis
      errors.

   APosterioriVariances
      Keyword to indicate the variances diagonal matrix of *a posteriori*
      analysis errors.

   APosterioriStandardDeviations
      Keyword to indicate the standard errors diagonal matrix of *a posteriori*
      analysis errors.

   BMA
      The acronym means *Background minus Analysis*. It is the difference
      between the background state and the optimal state estimation,
      corresponding to the mathematical expression :math:`\mathbf{x}^b -
      \mathbf{x}^a`.

   OMA
      The acronym means *Observation minus Analysis*. It is the difference
      between the observations and the result of the simulation based on the
      optimal state estimation, the analysis, filtered to be compatible with
      the observation, corresponding to the mathematical expression
      :math:`\mathbf{y}^o - \mathbf{H}\mathbf{x}^a`.

   OMB
      The acronym means *Observation minus Background*. It is the difference
      between the observations and the result of the simulation based on the
      background state, filtered to be compatible with the observation,
      corresponding to the mathematical expression :math:`\mathbf{y}^o -
      \mathbf{H}\mathbf{x}^b`.

   SigmaBck2
      Keyword to indicate the Desroziers-Ivanov parameter measuring the
      background part consistency of the data assimilation optimal state
      estimation. Its value can be compared to 1, a "good" estimation leading to
      a parameter "close" to 1.

   SigmaObs2
      Keyword to indicate the Desroziers-Ivanov parameter measuring the
      observation part consistency of the data assimilation optimal state
      estimation. Its value can be compared to 1, a "good" estimation leading to
      a parameter "close" to 1.

   MahalanobisConsistency
      Keyword to indicate the Mahalanobis parameter measuring the consistency of
      the data assimilation optimal state estimation. Its value can be compared
      to 1, a "good" estimation leading to a parameter "close" to 1.

   analysis
      It is the optimal state estimated through a data assimilation or
      optimization procedure.

   background
      It is a part (chosen to be modified) of the system state representation,
      representation known *a priori* or initial one, which is not optimal, and
      which is used as a rough estimate, or a "best estimate", before an
      optimal estimation.

   innovation
      Difference between the observations and the result of the simulation based
      on the background state, filtered to be compatible with the observation.
      It is similar with OMB in static cases.

   CostFunctionJ
      Keyword to indicate the minimization function, noted as :math:`J`.

   CostFunctionJo
      Keyword to indicate the observation part of the minimization function,
      noted as :math:`J^o`.

   CostFunctionJb
      Keyword to indicate the background part of the minimization function,
      noted as :math:`J^b`.

   CurrentState
      Keyword to indicate the current state used during an optimization
      algorithm procedure.
