..
   Copyright (C) 2008-2019 EDF R&D

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
de l'optimisation en lien avec d'autres modules ou codes de simulation dans
SALOME**. Le module ADAO fournit une interface à des algorithmes classiques
d'assimilation de données ou d'optimisation, et permet d'intégrer leur usage
dans une étude SALOME. Les modules de calcul ou de simulation doivent fournir
une ou plusieurs méthodes d'appel spécifiques afin d'être appelable dans le
cadre SALOME/ADAO, et tous les modules SALOME peuvent être utilisés grace à
l'intégration dans YACS de ADAO.

Son principal objectif est de **permettre l'usage de diverses méthodes standards
d'assimilation de données ou d'optimisation, tout en restant facile à utiliser
et en fournissant une démarche pour aider à la mise en oeuvre**. Pour
l'utilisateur final, qui a préalablement recueilli les informations sur son
problème physique, l'environnement lui permet d'avoir une démarche de type
"souris\&click" pour construire un cas ADAO valide et pour l'évaluer.

Le module couvre une grande variété d'applications pratiques, de façon robuste,
permettant des applications réelles, mais aussi d'effectuer de l'expérimentation
méthodologique rapide. Son évolutivité, des points de vue méthodologique et
numérique, permettra l'extension de son domaine d'application.
