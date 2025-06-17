..
   Copyright (C) 2008-2025 EDF R&D

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

.. _section_glossary:

Glossaire
=========

.. glossary::
   :sorted:

   Cas
      Un cas ADAO est défini par un jeu de données et de choix, rassemblés par
      l'intermédiaire de l'interface utilisateur du module (en TUI comme en
      GUI). Les données sont les mesures physiques qui doivent être
      techniquement disponibles avant ou pendant l'exécution du cas. Le (ou
      les) code(s) de simulation et la méthode d'assimilation de données ou
      d'optimisation, ainsi que leurs paramètres, doivent être choisis, ils
      définissent les propriétés d'exécution du cas.

   Itération (interne)
      Une itération (interne) a lieu lorsque l'on utilise des méthodes
      d'optimisation itératives (par exemple pour l'algorithme de 3DVAR). Les
      itérations internes sont effectuées à l'intérieur de chaque opération
      d'optimisation itérative. Le comportement itératif est entièrement
      intégré dans l'exécution des algorithmes itératifs, et il n'est apparent
      pour l'utilisateur que lorsque son observation est explicitement demandée
      en utilisant des "*Observer*" attachés à des variables de calcul. Voir
      aussi :term:`Pas (d'assimilation)`.

   Pas (d'assimilation)
      Un pas (d'assimilation) a lieu lorsqu'une nouvelle observation, ou un
      nouveau jeu d'observations, est utilisé, pour suivre par exemple le
      déroulement temporel d'un système dynamique. Remarque : un *unique pas*
      d'assimilation peut contenir par nature *plusieurs itérations*
      d'optimisation lorsque l'assimilation utilise une méthode itérative
      d'optimisation. Voir aussi :term:`Itération (interne)`.

   Système physique
      C'est l'objet d'étude que l'on va représenter par simulation numérique,
      et que l'on observe par des mesures.

   Simulateur numérique
      Ensemble des relations numériques et des équations caractérisant le
      système physique étudié.

   Simulation numérique
      Mise en oeuvre calculatoire de l'ensemble constitué du simulateur
      numérique et d'un jeu particulier de toutes les variables d'entrée et de
      contrôle du simulateur. Ces variables permettent de mettre le simulateur
      numérique en capacité de représenter numériquement le comportement du
      système.

   Observations ou mesures
      Ce sont des quantités qui proviennent d'instruments de mesures et qui
      caractérisent le système physique à étudier. Ces quantités peuvent varier
      en espace ou en temps, peuvent être ponctuelles ou intégrées. Elles sont
      elles-mêmes caractérisées par leur nature de mesure, leur dimension, etc.

   Opérateur d'observation
      C'est une transformation de l'état simulé en un ensemble de quantités
      explicitement comparables aux observations.

   Conditions aux limites
      Ce sont des variables particulières d'entrée et de contrôle du
      simulateur, qui caractérisent la description du comportement du système
      en bordure du domaine spatial de simulation.

   Conditions initiales
      Ce sont des variables particulières d'entrée et de contrôle du
      simulateur, qui caractérisent la description du comportement du système
      en bordure initiale du domaine temporel de simulation.

   APosterioriCovariance
      Mot-clé indiquant la matrice de covariance des erreurs *a posteriori*
      d'analyse.

   APosterioriCorrelations
      Mot-clé indiquant la matrice de corrélation des erreurs *a posteriori*
      d'analyse.

   APosterioriVariances
      Mot-clé indiquant la matrice diagonale des variances des erreurs *a
      posteriori* d'analyse.

   APosterioriStandardDeviations
      Mot-clé indiquant la matrice diagonale des écarts-types des erreurs *a
      posteriori* d'analyse.

   BMA
      L'acronyme signifie *Background moins Analysis*. C'est la différence
      entre l'état d'ébauche et l'état optimal estimé, correspondant à
      l'expression mathématique :math:`\mathbf{x}^b - \mathbf{x}^a`.

   OMA
      L'acronyme signifie *Observation moins Analysis*. C'est la différence
      entre les observations et le résultat de la simulation basée sur l'état
      optimal estimé, l'analyse, filtré pour être compatible avec les
      observations, correspondant à l'expression mathématique
      :math:`\mathbf{y}^o - \mathbf{H}\mathbf{x}^a`.

   OMB
      L'acronyme signifie *Observation moins Background*. C'est la différence
      entre les observations et le résultat de la simulation basée sur l'état
      d'ébauche,  filtré pour être compatible avec les observations,
      correspondant à l'expression mathématique :math:`\mathbf{y}^o -
      \mathbf{H}\mathbf{x}^b`.

   SigmaBck2
      Mot-clé indiquant le paramètre de Desroziers-Ivanov mesurant la
      consistance de la partie due à l'ébauche dans l'estimation optimale d'état
      par assimilation de données. Sa valeur peut être comparée à 1, une "bonne"
      estimation conduisant à un paramètre "proche" de 1.

   SigmaObs2
      Mot-clé indiquant le paramètre de Desroziers-Ivanov mesurant la
      consistance de la partie due à l'observation dans l'estimation optimale
      d'état par assimilation de données. Sa valeur peut être comparée à 1, une
      "bonne" estimation conduisant à un paramètre "proche" de 1.

   MahalanobisConsistency
      Mot-clé indiquant le paramètre de Mahalanobis mesurant la consistance de
      l'estimation optimale d'état par assimilation de données. Sa valeur peut
      être comparée à 1, une "bonne" estimation conduisant à un paramètre
      "proche" de 1.

   Analyse
      C'est l'état optimal de représentation du système estimé par une
      procédure d'assimilation de données ou d'optimisation.

   Background
      C'est le terme anglais pour désigner l'ébauche.

   Ebauche
      C'est une part (choisie pour être modifiable) de la représentation de
      l'état du système, représentation connue *a priori* ou initiale, qui
      n'est pas optimale, et qui est utilisée comme une estimation grossière ou
      comme "la meilleure connue", avant une estimation optimale.

   Innovation
      Différence entre les observations et le résultat de la simulation basée
      sur l'état d'ébauche,  filtré pour être compatible avec les observations.
      C'est similaire à OMB dans les cas statiques.

   CostFunctionJ
      Mot-clé indiquant la fonction de minimisation, notée :math:`J`.

   CostFunctionJo
      Mot-clé indiquant la partie due aux observations dans la fonction de
      minimisation, notée :math:`J^o`.

   CostFunctionJb
      Mot-clé indiquant la partie due à l'ébauche dans la fonction de
      minimisation, notée :math:`J^b`.

   CurrentState
      Mot-clé indiquant l'état courant utilisé au cours du déroulement d'un
      algorithme d'optimisation.
