..
   Copyright (C) 2008-2020 EDF R&D

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

.. _section_ref_entry_types:

Liste des types d'entrées possibles pour les variables utilisateurs
-------------------------------------------------------------------

Chaque variable à renseigner pour l'utilisation d'ADAO peut être représentée à
l'aide de "pseudo-types" particuliers, qui aident à la remplir logiquement et à
la valider informatiquement. Ces pseudo-types représentent explicitement des
formes mathématiques (:ref:`section_ref_entry_types_math`) ou informatiques
simples (:ref:`section_ref_entry_types_info`), que l'on détaille ici. On
utilise aussi les :ref:`section_notations`, en même temps que les
:ref:`section_ref_entry_types_names`.

Le test explicite :ref:`section_ref_algorithm_InputValuesTest` est prévu pour
que l'utilisateur puisse vérifier spécifiquement certaines entrées, avec les
mêmes analyses et critères que lors de la mise en place usuelle d'une étude.

.. _section_ref_entry_types_math:

Pseudo-types de représentation mathématique des données
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

Les entrées sont décrites selon une logique la plus simple possible, de
représentation mathématique, pour des algorithmes ou outils de calculs.

.. include:: snippets/EntryTypeVector.rst

.. include:: snippets/EntryTypeVectorSerie.rst

.. include:: snippets/EntryTypeMatrix.rst

.. include:: snippets/EntryTypeFunction.rst

.. include:: snippets/EntryTypeDict.rst

Les variables auxquelles ces pseudo-types s'appliquent peuvent elles-mêmes être
données à l'aide des descriptions informatiques qui suivent.

.. _section_ref_entry_types_info:

Pseudo-types de description informatique des données
++++++++++++++++++++++++++++++++++++++++++++++++++++

Trois pseudo-types, purement informatiques, permettent de désigner la manière
dont on fournit les variables en entrée.

.. include:: snippets/EntryTypeScript.rst

.. include:: snippets/EntryTypeString.rst

.. include:: snippets/EntryTypeDataFile.rst

.. _section_ref_entry_types_names:

Informations sur les noms imposés pour les entrées par fichier
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Lorsqu'une commande ou un mot-clé peuvent être renseignés à l'aide d'un fichier
script désigné par le pseudo-type "*Script*", ce script doit présenter une
variable ou une méthode qui porte le même nom que la variable à remplir. En
d'autres termes, lorsque l'on importe un tel script dans une commande Python ou
un noeud Python de YACS, il doit créer une variable du bon nom dans l'espace de
nommage courant du noeud. Par exemple, un script Python rendant disponible la
variable d'ébauche, nommée "*Background*", doit présenter la forme suivante ::

    ...
    ...
    Background =...
    ...
    ...

Son importation permet ainsi de créer la variable "*Background*" dans l'espace
de nommage courant. Les points "..." symbolisent du code quelconque autour de
ce début particulier de ligne.

De la même manière, lorsqu'un vecteur particulier peut être renseigné à l'aide
d'un fichier de données désigné par le pseudo-type "*DataFile*", les
informations présentes dans le fichier "*DataFile*" doivent porter le nom du
vecteur à charger.
