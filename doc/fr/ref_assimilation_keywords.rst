..
   Copyright (C) 2008-2022 EDF R&D

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

.. _section_ref_assimilation_keywords:

Liste des commandes et mots-clés pour un cas d'assimilation de données ou d'optimisation
----------------------------------------------------------------------------------------

On résume ici l'ensemble des commandes disponibles pour décrire un cas de
calcul en évitant les particularités de chaque algorithme. C'est donc un
inventaire commun des commandes.

Le jeu de commandes pour un cas d'assimilation de données ou d'optimisation est
lié à la description d'un cas de calcul, qui est une procédure en *Assimilation
de Données*, en *Méthodes avec Réduction* ou en méthodes *Optimisation*.

Le premier terme décrit le choix entre un calcul ou une vérification. Dans
l'interface graphique, chacun des trois types de calculs, individuellement
plutôt orientés soit *assimilation de données*, soit "méthodes d'optimisation*,
"soit *méthodes avec réduction* (sachant que certains sont simultanément dans
plusieurs catégories), est impérativement désigné par l'une ces commandes:

.. include:: snippets/ASSIMILATION_STUDY.rst

.. include:: snippets/OPTIMIZATION_STUDY.rst

.. include:: snippets/REDUCTION_STUDY.rst

Les autres termes imbriqués sont classés par ordre alphabétique. Ils ne sont
pas obligatoirement requis pour tous les algorithmes. Les différentes commandes
sont les suivantes:

.. include:: snippets/AlgorithmParameters.rst

.. include:: snippets/Background.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/ControlInput.rst

.. include:: snippets/Debug.rst

.. include:: snippets/EvolutionError.rst

.. include:: snippets/EvolutionModel.rst

.. include:: snippets/ExecuteInContainer.rst

.. include:: snippets/InputVariables.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. include:: snippets/Observers.rst

.. include:: snippets/OutputVariables.rst

.. include:: snippets/StudyName.rst

.. include:: snippets/StudyRepertory.rst

.. include:: snippets/UserDataInit.rst

.. include:: snippets/UserPostAnalysis.rst
