..
   Copyright (C) 2008-2015 EDF R&D

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

Liste des types d'entrées possibles
-----------------------------------

Chaque variable ADAO présente un pseudo-type qui aide à la remplir et à la
valider. Les différents pseudo-types sont:

.. index:: single: Dict

**Dict**
    Cela indique une variable qui doit être remplie avec un dictionnaire Python
    ``{"clé":"valeur"...}``, usuellement donné soit par une chaîne de caractères
    soit par un fichier script.

.. index:: single: Function

**Function**
    Cela indique une variable qui doit être donnée comme une fonction Python,
    usuellement donnée soit par une chaîne de caractères soit par un fichier
    script.

.. index:: single: Matrix

**Matrix**
    Cela indique une variable qui doit être donnée comme une matrice,
    usuellement donnée soit par une chaîne de caractères soit par un fichier
    script.

.. index:: single: ScalarSparseMatrix

**ScalarSparseMatrix**
    Cela indique une variable qui doit être donnée comme un nombre unique (qui
    sera utilisé pour multiplier une matrice identité), usuellement donné soit
    par une chaîne de caractères soit par un fichier script.

.. index:: single: DiagonalSparseMatrix

**DiagonalSparseMatrix**
    Cela indique une variable qui doit , (qui sera
    utilisé pour remplacer la diagonale d'une matrice identité), usuellement
    donné soit par une chaîne de caractères soit par un fichier script.

.. index:: single: Script

**Script**
    Cela indique un script donné comme un fichier externe. Il peut être désigné
    par un nom de fichier avec chemin complet ou seulement par un nom de fichier
    sans le chemin. Si le fichier est donné uniquement par un nom sans chemin,
    et si un répertoire d'étude est aussi indiqué, le fichier est recherché dans
    le répertoire d'étude donné.

.. index:: single: String

**String**
    Cela indique une chaîne de caractères fournissant une représentation
    littérale d'une matrice, d'un vecteur ou d'une collection de vecteurs, comme
    par exemple "1 2 ; 3 4" ou "[[1,2],[3,4]]" pour une matrice carrée de taille
    2x2.

.. index:: single: Vector

**Vector**
    Cela indique une variable qui doit être remplie comme un vecteur,
    usuellement donné soit par une chaîne de caractères soit par un fichier
    script.

.. index:: single: VectorSerie

**VectorSerie**
    Cela indique une variable qui doit être remplie comme une liste de vecteurs,
    usuellement donnée soit par une chaîne de caractères soit par un fichier
    script.

Lorsqu'une commande ou un mot-clé peut être rempli par un nom de fichier script,
ce script doit présenter une variable ou une méthode que porte le même nom que
la variable à remplir. En d'autres mots, lorsque l'on importe le script dans un
noeud Python de YACS, il doit créer une variable du bon nom dans l'espace de
nommage courant du noeud.
