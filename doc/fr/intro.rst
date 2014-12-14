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

.. _section_intro:

================================================================================
Introduction � ADAO
================================================================================

Le but du module est ADAO **d'aider � l'usage de l'assimilation de donn�es ou de
l'optimisation en lien avec d'autres modules ou codes de simulation dans
SALOME**. Le module ADAO fournit une interface � des algorithmes classiques
d'assimilation de donn�es ou d'optimisation, et permet d'int�grer leur usage
dans une �tude SALOME. Les modules de calcul ou de simulation doivent fournir
une ou plusieurs m�thodes d'appel sp�cifiques afin d'�tre appelable dans le
cadre SALOME/ADAO, et tous les modules SALOME peuvent �tre utilis�s grace �
l'int�gration dans YACS de ADAO.

Son principal objectif est de **permettre l'usage de diverses m�thodes standards
d'assimilation de donn�es ou d'optimisation, tout en restant facile � utiliser
et en fournissant une d�marche pour aider � la mise en oeuvre**. Pour
l'utilisateur final, qui a pr�alablement recueilli les informations sur son
probl�me physique, l'environnement lui permet d'avoir une d�marche de type
"souris\&click" pour construire un cas ADAO valide et pour l'�valuer.

Le module couvre une grande vari�t� d'applications pratiques, de fa�on robuste,
permettant des applications r�elles, mais aussi d'effectuer de l'exp�rimentation
m�thodologique rapide. Son �volutivit�, des points de vue m�thodologique et
num�rique, permettra l'extension de son domaine d'application.
