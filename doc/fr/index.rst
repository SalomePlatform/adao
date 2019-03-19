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

.. _section_home:

================================================================================
Documentation ADAO
================================================================================

.. image:: images/ADAO_logo.png
   :align: center
   :alt: Logo ADAO

**Le module ADAO fournit des fonctionnalités d'assimilation de données et
d'optimisation** dans un contexte Python [Python]_ ou SALOME [Salome]_.

En bref, l'assimilation de données est un cadre méthodologique pour calculer
l'estimation optimale de la valeur réelle (inaccessible) de l'état d'un
système, éventuellement au cours du temps. Il utilise des informations
provenant de mesures expérimentales, ou observations, et de modèles numériques
*a priori*, y compris des informations sur leurs erreurs. Certaines des
méthodes incluses dans ce cadre sont également connues sous les noms
d'*estimation de paramètres*, de *problèmes inverses*, d'*estimation
bayésienne*, d'*interpolation optimale*, de *reconstruction de champs*, etc. De
plus amples détails peuvent être trouvés dans la partie proposant
:ref:`section_theory`.

La documentation de ce module est divisée en plusieurs grandes catégories,
relatives à la documentation théorique (indiquée dans le titre de section par
**[DocT]**), à la documentation utilisateur (indiquée dans le titre de section
par **[DocU]**), et à la documentation de référence (indiquée dans le titre de
section par **[DocR]**).

La première partie est l':ref:`section_intro`. La seconde partie présente
:ref:`section_theory`, et à leurs concepts, et la partie suivante décrit la
:ref:`section_methodology`. Pour un utilisateur courant, les parties suivantes
présentent des exemples didactiques d'utilisation sous la forme de
:ref:`section_tutorials_in_salome` ou de :ref:`section_tutorials_in_python`,
puis indique les :ref:`section_advanced`, avec l'obtention de renseignements
supplémentaires ou l'usage par scripts de commandes hors interface de contrôle
graphique. Les utilisateurs intéressés par un accès rapide au module peuvent
s'arrêter avant la lecture de la suite, mais un usage utile du module nécessite
de lire et de revenir régulièrement à ces parties. Les parties qui suivent
expliquent comment utiliser une :ref:`section_gui_in_salome` ou une
:ref:`section_tui`. La dernière grande partie détaille la
:ref:`section_reference`, avec trois sous-parties essentielles qui la composent
et qui décrivent les commandes et des options d'algorithmes. Un
:ref:`section_glossary`, des :ref:`section_notations`, une
:ref:`section_bibliography` et un :ref:`genindex` développés complètent le
document. Enfin, pour respecter les exigences de licence du module, n'oubliez
pas de lire la partie :ref:`section_license`.

**Table des matières**

.. toctree::
   :maxdepth: 2

   intro
   theory
   methodology
   tutorials_in_salome
   tutorials_in_python
   advanced
   gui_in_salome
   tui
   reference
   license
   glossary
   notations
   bibliography

**Index et tables**

* :ref:`genindex`
* :ref:`search`

.. * :ref:`section_glossary`
