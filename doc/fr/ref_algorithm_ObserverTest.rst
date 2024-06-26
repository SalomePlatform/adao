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

.. index:: single: ObserverTest
.. _section_ref_algorithm_ObserverTest:

Algorithme de vérification "*ObserverTest*"
-------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet de vérifier une fonction externe et fournie par
l'utilisateur, utilisée comme un *observer*. Cette fonction externe peut être
appliquée pour chacune des variables potentiellement observables. Elle n'est
activée que sur celles qui sont explicitement associées avec cet *observer*
dans sa déclaration.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropDerivativeFree.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Observers.rst

Les commandes optionnelles générales, disponibles dans l'interface en édition,
sont indiquées dans la :ref:`section_ref_checking_keywords`.

*Astuce pour cet algorithme :*

    Comme les commandes *"CheckingPoint"* et *"ObservationOperator"*, dans
    l'interface graphique, sont requises pour TOUS les algorithmes de
    vérification, il faut fournir une valeur, malgré le fait que ces commandes
    ne soient pas nécessaires pour ce test (et que leurs valeurs ne sont donc
    pas utilisées). La manière la plus simple est de donner "1" comme un STRING
    pour les deux, avec un *"ObservationOperator"* devant être de type *Matrix*
    creuse.
