..
   Copyright (C) 2008-2014 EDF R&D

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

.. index:: single: AlgorithmParameters
.. _section_ref_options_AlgorithmParameters:

Description des options d'un algorithme par "*AlgorithmParameters*"
-------------------------------------------------------------------

Chaque algorithme peut être contrôlé en utilisant des options particulières,
données à travers la commande optionnelle "*AlgorithmParameters*", à la manière
de l'exemple qui suit, dans un fichier Python::

    AlgorithmParameters = {
        "StoreInternalVariables" : True,
        "MaximumNumberOfSteps" : 25,
        "StoreSupplementaryCalculations" : ["APosterioriCovariance","OMA"],
        }

Pour donner les valeurs de la commande "*AlgorithmParameters*" par une chaîne de
caractères, directement dans l'interface EFICAS, on doit utiliser des guillemets
simples pour fournir une définition standard de dictionnaire, comme par
exemple::

    '{"StoreInternalVariables":True,"MaximumNumberOfSteps":25}'

Si une option est spécifiée par l'utilisateur pour un algorithme qui ne la
supporte pas, cette option est simplement laissée inutilisée et ne bloque pas le
traitement. La signification des acronymes ou des noms particuliers peut être
trouvée dans l':ref:`genindex` ou dans le :ref:`section_glossary`.
