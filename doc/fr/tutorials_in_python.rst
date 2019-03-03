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

.. _section_tutorials_in_python:

================================================================================
**[DocU]** Tutoriaux sur l'utilisation du module ADAO dans Python
================================================================================

Cette section présente quelques exemples d'utilisation du module ADAO en Python
SALOME. Le premier montre comment construire un cas simple d'assimilation de
données définissant explicitement toutes les données d'entrée requises à
travers l'interface utilisateur textuelle (TUI). Le second montre, sur le même
cas, comment définir les données d'entrée à partir de sources externes à
travers des scripts.

Les notations mathématiques utilisées ci-dessous sont expliquées dans la
section :ref:`section_theory`.

Construire un cas d'estimation avec une définition explicite des données
------------------------------------------------------------------------
