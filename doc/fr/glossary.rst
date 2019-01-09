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

.. _section_glossary:

Glossaire
=========

.. glossary::
   :sorted:

   cas
      Un cas ADAO est défini par un jeu de données et de choix, rassemblés par
      l'intermédiaire de l'interface utilisateur du module. Les données sont les
      mesures physiques qui doivent être techniquement disponibles avant ou
      pendant l'exécution du cas. Le (ou les) code(s) de simulation et la
      méthode d'assimilation de données ou d'optimisation, ainsi que leurs
      paramètres, doivent être choisis, ils définissent les propriétés
      d'exécution du cas.

   itération
      Une itération a lieu lorsque l'on utilise des méthodes d'optimisation
      itératives (par exemple le 3DVAR), et c'est entièrement caché à
      l'intérieur du noeud principal de type YACS OptimizerLoop nommé
      "*compute_bloc*". Néanmoins, l'utilisateur peut observer le processus
      itératif à l'aide de la fenêtre "*YACS Container Log*", qui est mise à
      jour au fur et à mesure du déroulement du calcul, et en utilisant des
      "*Observers*" attachés à des variables de calcul.

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

   BMA (Background minus Analysis)
      Différence entre l'état d'ébauche et l'état optimal estimé, notée
      :math:`\mathbf{x}^b - \mathbf{x}^a`.

   OMA (Observation minus Analysis)
      Différence entre les observations et le résultat de la simulation basée
      sur l'état optimal estimé, l'analyse, filtré pour être compatible avec les
      observations, notée :math:`\mathbf{y}^o - \mathbf{H}\mathbf{x}^a`.

   OMB (Observation minus Background)
      Différence entre les observations et le résultat de la simulation basée
      sur l'état d'ébauche,  filtré pour être compatible avec les observations,
      notée :math:`\mathbf{y}^o - \mathbf{H}\mathbf{x}^b`.

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

   analyse
      L'état optimal estimé par une procédure d'assimilation de données ou
      d'optimisation.

   background
      C'est le terme anglais pour désigner l'ébauche.

   ébauche
      C'est l'état du système connu *a priori*, qui n'est pas optimal, et qui
      est utilisé comme une estimation grossière, ou "la meilleure connue",
      avant une estimation optimale.

   innovation
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
