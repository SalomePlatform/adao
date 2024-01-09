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

.. _section_ref_checking_keywords:

Liste des commandes et mots-clés pour un cas de vérification
------------------------------------------------------------

On résume ici l’ensemble des commandes et des mots-clés disponibles pour
décrire un cas de vérification en évitant les particularités de chaque
algorithme. C’est donc un inventaire commun des commandes.

Un terme particulier désigne le choix explicite d'une vérification. Dans
l'interface graphique, ce choix se fait par la commande obligatoire
"*CHECKING_STUDY*".

Tous les termes possibles, imbriqués ou non, sont classés par ordre
alphabétique. Ils ne sont pas obligatoirement requis pour tous les algorithmes.
Les commandes ou mots-clés disponibles sont les suivants:

.. include:: snippets/AlgorithmParameters.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/CHECKING_STUDY.rst

.. include:: snippets/Debug.rst

.. include:: snippets/ExecuteInContainer.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. include:: snippets/Observers.rst

.. include:: snippets/StudyName.rst

.. include:: snippets/StudyRepertory.rst

.. include:: snippets/UserDataInit.rst
