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

.. _section_reference:

================================================================================
**[DocR]** Description de r�f�rence des commandes et mots-cl�s ADAO
================================================================================

Les sections suivantes pr�sentent la description de r�f�rence des commandes et
mots-cl�s ADAO disponibles � travers l'interface graphique (GUI) ou � travers
des scripts. Les deux premi�res sections communes pr�sentent les
:ref:`section_reference_entry` et les :ref:`section_reference_special_entry`.
Ensuite, on d�crit successivement les :ref:`section_reference_assimilation` et
les :ref:`section_reference_checking`.

Chaque commande ou mot-cl� � d�finir par l'interface graphique (GUI) a des
propri�t�s particuli�res. La premi�re propri�t� est d'�tre *requise*,
*optionnelle* ou simplement utile, d�crivant un type d'entr�e. La seconde
propri�t� est d'�tre une variable "ouverte" avec un type fix� mais avec
n'importe quelle valeur autoris�e par le type, ou une variable "ferm�e", limit�e
� des valeurs sp�cifi�es. L'�diteur graphique int�gr� disposant de capacit�s
intrins�ques de validation, les propri�t�s des commandes ou mots-cl�s donn�es �
l'aide de l'interface graphique sont automatiquement correctes.

.. _section_reference_entry:

========================================================================================
**[DocR]** Entr�es et sorties g�n�rales
========================================================================================

Cette section d�crit de mani�re g�n�rale les diff�rentes possibilit�s de types
d'entr�es et de variables de sortie que l'on peut utiliser. Les notations
math�matiques utilis�es sont expliqu�es dans la section :ref:`section_theory`.

.. toctree::
   :maxdepth: 1
   
   ref_entry_types
   ref_options_AlgorithmParameters
   ref_output_variables

.. _section_reference_special_entry:

========================================================================================
**[DocR]** Entr�es sp�ciales : fonctions, matrices, "*observer*"
========================================================================================

Cette section d�crit les entr�es sp�ciales, comme les formes fonctionnelles ou
matricielles, que l'on peut utiliser. Les notations math�matiques utilis�es
sont expliqu�es dans la section :ref:`section_theory`.

.. toctree::
   :maxdepth: 1
   
   ref_operator_requirements
   ref_covariance_requirements
   ref_observers_requirements

.. _section_reference_assimilation:

============================================================================================
**[DocR]** Cas d'assimilation de donn�es ou d'optimisation
============================================================================================

Cette section d�crit les algorithmes d'assimilation de donn�es ou d'optimisation
disponibles dans ADAO, d�taillant leurs caract�ristiques d'utilisation et leurs
options.

Des exemples sur l'usage de ces commandes sont disponibles dans la section
:ref:`section_examples` et dans les fichiers d'exemple install�s avec le module
ADAO. Les notations math�matiques utilis�es sont expliqu�es dans la section
:ref:`section_theory`.

.. toctree::
   :maxdepth: 1
   
   ref_assimilation_keywords
   ref_algorithm_3DVAR
   ref_algorithm_4DVAR
   ref_algorithm_Blue
   ref_algorithm_DerivativeFreeOptimization
   ref_algorithm_EnsembleBlue
   ref_algorithm_ExtendedBlue
   ref_algorithm_ExtendedKalmanFilter
   ref_algorithm_KalmanFilter
   ref_algorithm_LinearLeastSquares
   ref_algorithm_NonLinearLeastSquares
   ref_algorithm_ParticleSwarmOptimization
   ref_algorithm_QuantileRegression
   ref_algorithm_UnscentedKalmanFilter

.. _section_reference_checking:

================================================================================
**[DocR]** Cas de v�rification
================================================================================

Cette section d�crit les algorithmes de v�rification disponibles dans ADAO,
d�taillant leurs caract�ristiques d'utilisation et leurs options.

Des exemples sur l'usage de ces commandes sont disponibles dans la section
:ref:`section_examples` et dans les fichiers d'exemple install�s avec le module
ADAO. Les notations math�matiques utilis�es sont expliqu�es dans la section
:ref:`section_theory`.

.. toctree::
   :maxdepth: 1
   
   ref_checking_keywords
   ref_algorithm_AdjointTest
   ref_algorithm_FunctionTest
   ref_algorithm_GradientTest
   ref_algorithm_LinearityTest
   ref_algorithm_ObserverTest
   ref_algorithm_SamplingTest
   ref_algorithm_TangentTest
