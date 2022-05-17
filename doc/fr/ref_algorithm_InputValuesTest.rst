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

.. index:: single: InputValuesTest
.. _section_ref_algorithm_InputValuesTest:

Algorithme de vérification "*InputValuesTest*"
----------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo00.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet de vérifier le contenu des variables d'entrée courantes
et la manière dont les données sont interprétées ou lues lors de leur
acquisition, à travers l'affichage des informations de taille et des
statistique sur les entrées. Il permet aussi de restituer la totalité du
contenu des variables lues sous forme imprimée pour vérification (*attention,
si une variable est de grande taille, cette restitution peut être
informatiquement problématique*).

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Background.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/Observation.rst

*Astuce pour cet algorithme :*

    Comme la commande *"ObservationOperator"*, dans l'interface graphique, est
    requise pour TOUS les algorithmes de vérification, il faut fournir une
    valeur, malgré le fait que cette commandes ne soit pas nécessaires pour cet
    test (et sa valeur n'est donc pas utilisée). La manière la plus simple est
    de donner "1" comme un STRING, pour un *"ObservationOperator"* devant être
    de type *Matrix* creuse.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/NumberOfPrintedDigits.rst

.. include:: snippets/PrintAllValuesFor.rst

.. include:: snippets/ShowInformationOnlyFor.rst

.. include:: snippets/SetDebug.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_ParallelFunctionTest`
