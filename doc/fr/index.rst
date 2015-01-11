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

.. _section_home:

================================================================================
Documentation ADAO
================================================================================

.. image:: images/ADAO_logo.png
   :align: center
   :width: 20%

Le module ADAO fournit des fonctionnalités d'**assimilation de données et
d'optimisation** dans un contexte SALOME. Il est basé sur l'utilisation d'autres
modules, à savoir YACS et EFICAS, et sur l'utilisation d'une bibliothèque
générique sous-jacente d'assimilation de données.

En bref, l'assimilation de données est un cadre méthodologique pour calculer
l'estimation optimale de la valeur réelle (inaccessible) de l'état d'un système
au cours du temps. Il utilise des informations provenant de mesures
expérimentales, ou observations, et de modèles numériques *a priori*, y compris
des informations sur leurs erreurs. Certaines des méthodes incluses dans ce
cadre sont également connues sous les noms  d'*estimation des paramètres*, de
*problèmes inverses*, d'*estimation bayésienne*, d'*interpolation optimale*,
etc. De plus amples détails peuvent être trouvés dans la partie
:ref:`section_theory`.

La documentation de ce module est divisée en plusieurs parties. La première est
une :ref:`section_intro`. La seconde partie présente :ref:`section_theory`, et à
leurs concepts. La troisième partie explique comment :ref:`section_using`.  La
quatrième partie présente des exemples d'utilisation sous la forme de
:ref:`section_examples`. La cinquième partie détaille la
:ref:`section_reference`. Les utilisateurs intéressés par un accès rapide au
module peuvent s'arrêter avant la lecture de cette partie, mais un usage utile
du module nécessite de lire et de revenir régulièrement aux troisième et
cinquième parties. La dernière partie se focalise sur des
:ref:`section_advanced`, sur l'obtention de renseignements supplémentaires, ou
sur l'usage par scripts, sans interface utilisateur graphique (GUI). Enfin, pour
respecter les exigences de licence du module, n'oubliez pas de lire la partie
:ref:`section_license`.

Dans cette documentation, on utilise les notations standards de l'algèbre
linéaire, de l'assimilation de données (comme décrit dans [Ide97]_) et de
l'optimisation. En particulier, les vecteurs sont écrits horizontalement ou
verticalement sans faire la différence. Les matrices sont écrites soit
normalement, ou avec une notation condensée, consistant à utiliser un espace
pour séparer les valeurs, et un "``;``" pour séparer les lignes de la matrice,
de façon continue sur une ligne.

Table des matières
------------------

.. toctree::
   :maxdepth: 2

   intro
   theory
   using
   examples
   advanced
   reference
   license
   glossary
   bibliography

Index et tables
---------------

* :ref:`genindex`
* :ref:`search`

.. * :ref:`section_glossary`
