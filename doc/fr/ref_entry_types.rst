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

Liste des types d'entr�es possibles
-----------------------------------

Chaque variable ADAO pr�sente un pseudo-type qui aide � la remplir et � la
valider. Ces pseudo-types repr�sentent explicitement des formes informatiques ou
math�matiques simples. Deux pseudo-types, purement informatiques, permettent de
d�signer la mani�re dont on fournit les variables en entr�e:

.. index:: single: Script

**Script**
    Cela indique un script donn� comme un fichier externe. Il peut �tre d�sign�
    par un nom de fichier avec chemin complet ou seulement par un nom de fichier
    sans le chemin. Si le fichier est donn� uniquement par un nom sans chemin,
    et si un r�pertoire d'�tude est aussi indiqu�, le fichier est recherch� dans
    le r�pertoire d'�tude donn�.

.. index:: single: String

**String**
    Cela indique une cha�ne de caract�res fournissant une repr�sentation
    litt�rale d'une matrice, d'un vecteur ou d'une collection de vecteurs, comme
    par exemple "1 2 ; 3 4" ou "[[1,2],[3,4]]" pour une matrice carr�e de taille
    2x2.

Les diff�rents autres pseudo-types sont les suivants. Les variables auquelles
ils s'appliquent peuvent elles-m�mes �tre donn�es soit par une cha�ne de
caract�res (un "*String*"), soit par un fichier script (un "*Script*"):

.. index:: single: Dict

**Dict**
    Cela indique une variable qui doit �tre remplie avec un dictionnaire Python
    ``{"cl�":"valeur"...}``.

.. index:: single: Function

**Function**
    Cela indique une variable qui doit �tre donn�e comme une fonction Python.
    Les fonctions sont des entr�es sp�ciales d�crites par des
    :ref:`section_ref_operator_requirements`.

.. index:: single: Matrix

**Matrix**
    Cela indique une variable qui doit �tre donn�e comme une matrice.

.. index:: single: ScalarSparseMatrix

**ScalarSparseMatrix**
    Cela indique une variable qui doit �tre donn�e comme un nombre unique (qui
    sera ensuite utilis� pour multiplier une matrice identit�).

.. index:: single: DiagonalSparseMatrix

**DiagonalSparseMatrix**
    Cela indique une variable qui doit doit �tre donn�e comme un vecteur, (qui
    sera ensuite utilis� comme la diagonale d'une matrice carr�e).

.. index:: single: Vector

**Vector**
    Cela indique une variable qui doit �tre remplie comme un vecteur.

.. index:: single: VectorSerie

**VectorSerie**
    Cela indique une variable qui doit �tre remplie comme une liste de vecteurs.

Lorsqu'une commande ou un mot-cl� peut �tre rempli par un nom de fichier script
d�sign� par le pseudo-type "*Script*", ce script doit pr�senter une variable ou
une m�thode que porte le m�me nom que la variable � remplir. En d'autres termes,
lorsque l'on importe le script dans un noeud Python de YACS, il doit cr�er une
variable du bon nom dans l'espace de nommage courant du noeud. Par exemple, un
script Python rendant disponible la variable d'�bauche, nomm�e "*Background*",
doit pr�senter la forme suivante::

    ...
    Background =...
    ...

Son importation permet ainsi de cr�er la variable "*Background*". Les points
"..." symbolisent du code quelconque autour de ce d�but particulier de ligne.
