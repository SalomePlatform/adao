..
   Copyright (C) 2008-2023 EDF R&D

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

.. _section_intro:

================================================================================
Introduction à ADAO
================================================================================

Le but du module ADAO est **d'aider à l'usage de l'assimilation de données ou
de l'optimisation, en lien avec d'autres modules ou codes de simulation, dans
un contexte Python** [Python]_ **ou SALOME** [Salome]_. Il fournit une
interface simple à de nombreux algorithmes robustes et performants
d'assimilation de données ou d'optimisation, avec ou sans réduction, ainsi que
des aides aux tests et aux vérifications. Il permet d'intégrer ces outils dans
une étude Python ou SALOME.

Son principal objectif est de **permettre l'usage de méthodes standards et
robustes d'assimilation de données ou d'optimisation, dans une démarche usuelle
d'étude en simulation numérique, de manière performante, tout en restant facile
à paramétrer, et en fournissant une démarche simplifiée pour aider à la mise en
oeuvre**. Pour l'utilisateur final, qui a préalablement recueilli les
informations sur son problème physique, l'environnement lui permet d'avoir une
démarche centrée sur la simple déclaration de ces informations pour construire
un cas ADAO valide, pour ensuite l'évaluer, et pour en tirer les résultats
physiques dont il a besoin.

Le module couvre une grande variété d'applications pratiques, de façon robuste,
permettant des applications réelles, et aussi d'effectuer de l'expérimentation
méthodologique rapide. Il est basé sur l'utilisation d'autres modules Python ou
SALOME, en particulier YACS et EFICAS s'ils sont disponibles, et sur
l'utilisation d'une bibliothèque et d'outils génériques sous-jacents
d'assimilation de données. Les modules utilisateurs de calcul ou de simulation
doivent fournir une ou plusieurs méthodes d'appel spécifiques afin d'être
appelables dans le cadre Python ou SALOME. En environnement SALOME, tous les
modules natifs peuvent être utilisés grâce à l'intégration en Python ou en
YACS.
