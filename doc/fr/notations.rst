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

.. _section_notations:

Notations et conventions communes
=================================

Dans cette documentation, on utilise les notations standards de l'algèbre
linéaire, de l'assimilation de données (comme décrit dans [Ide97]_) et de
l'optimisation.

Pour les formulations algébriques, les vecteurs sont écrits horizontalement ou
verticalement sans faire la différence. Les matrices sont écrites soit
normalement, ou avec une notation condensée, consistant à utiliser un espace
pour séparer les valeurs, et un "``;``" pour séparer les lignes de la matrice,
de façon continue sur une ligne.

Les fichiers peuvent être indiqués grâce à un chemin absolu ou relatif. Pour
certains systèmes de fichiers anciens ou partagés, le nom complet avec le
chemin ne doit pas contenir plus de 256 caractères. Dans le cas où ce sont des
fichiers de type Python, il est judicieux de ne pas utiliser de points dans le
nom à part pour l'extension, pour éviter des difficultés d'utilisation
compliquées à diagnostiquer.

Les conventions de type et de nommage des fichiers s'appuient fortement sur les
extensions des fichiers eux-mêmes. On en précise brièvement certaines ici, sans
être exhaustifs :

- extension ``.py``   : fichier texte de données ou commandes de type source Python
- extension ``.comm`` : fichier texte de données de commandes EFICAS d'ADAO
- extension ``.xml``  : fichier texte de données de type XML (pour YACS, non exclusif)
- extension ``.txt``  : fichier texte de données à séparateur espace
- extension ``.dat``  : fichier texte de données à séparateur espace
- extension ``.csv``  : fichier texte de données à séparateur virgule ou point-virgule
- extension ``.tsv``  : fichier texte de données à séparateur tabulation
- extension ``.npy``  : fichier binaire de données de type Numpy mono-variable
- extension ``.npz``  : fichier binaire de données de type Numpy multi-variables
- extension ``.sdf``  : fichier binaire de données de type Scientific Data Format

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Asch16]_
- [Bouttier99]_
- [Ide97]_
- [WikipediaMO]_
