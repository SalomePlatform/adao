..
   Copyright (C) 2008-2024 EDF R&D

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

On résume ici l’ensemble des commandes et des mots-clés disponibles pour
décrire un cas de calcul en évitant les particularités de chaque algorithme.
C’est donc un inventaire commun des commandes.

Le jeu de commandes pour un cas d'assimilation de données ou d'optimisation est
lié à la description d'un cas de calcul, qui est une procédure en *Assimilation
de Données* (désignée en interface graphique par la commande
"*ASSIMILATION_STUDY*"), en *Méthodes avec Réduction* (désignée en interface
graphique par la commande "*REDUCTION_STUDY*") ou en méthodes *Optimisation*
(désignée en interface graphique par la commande "*OPTIMIZATION_STUDY*").

Tous les termes possibles, imbriqués ou non, sont classés par ordre
alphabétique. Ils ne sont pas obligatoirement requis pour tous les algorithmes.
Les commandes ou mots-clés disponibles sont les suivants:

.. include:: snippets/AlgorithmParameters.rst

.. include:: snippets/ASSIMILATION_STUDY.rst

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

.. include:: snippets/OPTIMIZATION_STUDY.rst

.. include:: snippets/OutputVariables.rst

.. include:: snippets/REDUCTION_STUDY.rst

.. include:: snippets/StudyName.rst

.. include:: snippets/StudyRepertory.rst

.. include:: snippets/UserDataInit.rst

.. include:: snippets/UserPostAnalysis.rst
