..
   Copyright (C) 2008-2016 EDF R&D

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

Le module ADAO fournit des fonctionnalit�s d'**assimilation de donn�es et
d'optimisation** dans un contexte SALOME. Il est bas� sur l'utilisation d'autres
modules, � savoir YACS et EFICAS, et sur l'utilisation d'une biblioth�que et des
outils g�n�riques sous-jacents d'assimilation de donn�es.

En bref, l'assimilation de donn�es est un cadre m�thodologique pour calculer
l'estimation optimale de la valeur r�elle (inaccessible) de l'�tat d'un syst�me
au cours du temps. Il utilise des informations provenant de mesures
exp�rimentales, ou observations, et de mod�les num�riques *a priori*, y compris
des informations sur leurs erreurs. Certaines des m�thodes incluses dans ce
cadre sont �galement connues sous les noms  d'*estimation des param�tres*, de
*probl�mes inverses*, d'*estimation bay�sienne*, d'*interpolation optimale*,
etc. De plus amples d�tails peuvent �tre trouv�s dans la partie proposant
:ref:`section_theory`.

La documentation de ce module est divis�e en plusieurs grandes cat�gories,
relatives � la documentation th�orique (indiqu�e dans le titre par **[DocT]**),
� la documentation utilisateur (indiqu�e dans le titre par **[DocU]**), et � la
documentation de r�f�rence (indiqu�e dans le titre par **[DocR]**).

La premi�re partie est l':ref:`section_intro`. La seconde partie pr�sente
:ref:`section_theory`, et � leurs concepts. Pour un utilisateur courant, la
troisi�me partie explique comment :ref:`section_using`, et la quatri�me partie
pr�sente des exemples d'utilisation sous la forme de :ref:`section_examples`.
Les utilisateurs int�ress�s par un acc�s rapide au module peuvent s'arr�ter
avant la lecture de la suite, mais un usage utile du module n�cessite de lire et
de revenir r�guli�rement aux troisi�me et septi�me parties. La cinqui�me partie
indique les :ref:`section_advanced`, avec l'obtention de renseignements
suppl�mentaires ou l'usage par scripts d'ex�cution sans interface utilisateur
graphique (GUI). La partie suivante d�taille la :ref:`section_reference`, avec
quatre sous-parties principales qui suivent, la derni�re sous-partie d�crivant
une :ref:`section_tui` du module. Enfin, pour respecter les exigences de licence
du module, n'oubliez pas de lire la partie :ref:`section_license`.

Dans cette documentation, on utilise les notations standards de l'alg�bre
lin�aire, de l'assimilation de donn�es (comme d�crit dans [Ide97]_) et de
l'optimisation. En particulier, les vecteurs sont �crits horizontalement ou
verticalement sans faire la diff�rence. Les matrices sont �crites soit
normalement, ou avec une notation condens�e, consistant � utiliser un espace
pour s�parer les valeurs, et un "``;``" pour s�parer les lignes de la matrice,
de fa�on continue sur une ligne.

Table des mati�res
------------------

.. toctree::
   :maxdepth: 2

   intro
   theory
   using
   examples
   advanced
   reference
   tui
   license
   glossary
   bibliography

Index et tables
---------------

* :ref:`genindex`
* :ref:`search`

.. * :ref:`section_glossary`
