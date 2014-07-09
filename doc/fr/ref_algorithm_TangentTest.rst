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

.. index:: single: TangentTest
.. _section_ref_algorithm_TangentTest:

Algorithme de vérification "*TangentTest*"
------------------------------------------

Description
+++++++++++

Cet algorithme permet de vérifier la qualité de l'opérateur tangent, en
calculant un résidu dont les propriétés théoriques sont connues.

On observe le résidu suivant, provenant du rapport d'incréments utilisant
l'opérateur linéaire tangent :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) ||}{|| \alpha * TangentF_x * \mathbf{dx} ||}

qui doit rester stable en :math:`1+O(\alpha)` jusqu'à ce que l'on atteigne la
précision du calcul.

Lorsque :math:`|R-1|/\alpha` est inférieur ou égal à une valeur stable lorsque
:math:`\alpha` varie, le tangent est valide, jusqu'à ce que l'on atteigne la
précision du calcul.

Si :math:`|R-1|/\alpha` est très faible, le code de calcul :math:`F` est
vraisemblablement linéaire ou quasi-linéaire (ce que l'on peut vérifier par
l':ref:`section_ref_algorithm_LinearityTest`), et le tangent est valide jusqu'à
ce que l'on atteigne la précision du calcul.

On prend :math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` et
:math:`\mathbf{dx}=\alpha*\mathbf{dx}_0`. :math:`F` est le code de calcul.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: CheckingPoint
.. index:: single: ObservationOperator
.. index:: single: AmplitudeOfInitialDirection
.. index:: single: EpsilonMinimumExponent
.. index:: single: InitialDirection
.. index:: single: SetSeed

Les commandes requises générales, disponibles dans l'interface en édition, sont
les suivantes:

  CheckingPoint
    *Commande obligatoire*. Elle définit le vecteur utilisé comme l'état autour
    duquel réaliser le test requis, noté :math:`\mathbf{x}` et similaire à
    l'ébauche :math:`\mathbf{x}^b`. Sa valeur est définie comme un objet de type
    "*Vector*".

  ObservationOperator
    *Commande obligatoire*. Elle indique l'opérateur d'observation, notée
    précédemment :math:`H`, qui transforme les paramètres d'entrée
    :math:`\mathbf{x}` en résultats :math:`\mathbf{y}` qui sont à comparer aux
    observations :math:`\mathbf{y}^o`.  Sa valeur est définie comme un objet de
    type "*Function*". Différentes formes fonctionnelles peuvent être
    utilisées, comme décrit dans la section
    :ref:`section_ref_operator_requirements`. Si un contrôle :math:`U` est
    inclus dans le modèle d'observation, l'opérateur doit être appliqué à une
    paire :math:`(X,U)`.

Les commandes optionnelles générales, disponibles dans l'interface en édition,
sont indiquées dans la :ref:`section_ref_checking_keywords`. En particulier, la
commande optionnelle "*AlgorithmParameters*" permet d'indiquer les options
particulières, décrites ci-après, de l'algorithme. On se reportera à la
:ref:`section_ref_options_AlgorithmParameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  AmplitudeOfInitialDirection
    Cette clé indique la mise à l'échelle de la perturbation initiale construite
    comme un vecteur utilisé pour la dérivée directionnelle autour du point
    nominal de vérification. La valeur par défaut est de 1, ce qui signifie pas
    de mise à l'échelle.

  EpsilonMinimumExponent
    Cette clé indique la valeur de l'exposant minimal du coefficient en
    puissance de 10 qui doit être utilisé pour faire décroître le multiplicateur
    de l'incrément. La valeur par défaut est de -8, et elle doit être entre 0 et
    -20. Par exemple, la valeur par défaut conduit à calculer le résidu de la
    formule avec un incrément fixe multiplié par 1.e0 jusqu'à 1.e-8.

  InitialDirection
    Cette clé indique la direction vectorielle utilisée pour la dérivée
    directionnelle autour du point nominal de vérification. Cela doit être un
    vecteur. Si elle n'est pas spécifiée, la direction par défaut est une
    perturbation par défaut autour de zéro de la même taille vectorielle que le
    point de vérification.

  SetSeed
    Cette clé permet de donner un nombre entier pour fixer la graine du
    générateur aléatoire utilisé pour générer l'ensemble. Un valeur pratique est
    par exemple 1000. Par défaut, la graine est laissée non initialisée, et elle
    utilise ainsi l'initialisation par défaut de l'ordinateur.

Voir aussi
++++++++++

Références vers d'autres sections :
  - :ref:`section_ref_algorithm_FunctionTest`
  - :ref:`section_ref_algorithm_AdjointTest`
  - :ref:`section_ref_algorithm_GradientTest`
