..
   Copyright (C) 2008-2017 EDF R&D

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

.. index:: single: GradientTest
.. _section_ref_algorithm_GradientTest:

Algorithme de v�rification "*GradientTest*"
-------------------------------------------

Description
+++++++++++

Cet algorithme permet de v�rifier la qualit� du gradient de l'op�rateur, en
calculant un r�sidu dont les propri�t�s th�oriques sont connues. Plusieurs
formules de r�sidu sont disponibles.

Dans tous les cas, on prend :math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` et
:math:`\mathbf{dx}=\alpha*\mathbf{dx}_0`. :math:`F` est le code de calcul.

R�sidu "Taylor"
***************

On observe le r�sidu issu du d�veloppement de Taylor de la fonction :math:`F`,
normalis� par la valeur au point nominal :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) - \alpha * \nabla_xF(\mathbf{dx}) ||}{|| F(\mathbf{x}) ||}

Si le r�sidu d�croit et que la d�croissance se fait en :math:`\alpha^2` selon
:math:`\alpha`, cela signifie que le gradient est bien calcul� jusqu'� la
pr�cision d'arr�t de la d�croissance quadratique, et que :math:`F` n'est pas
lin�aire.

Si le r�sidu d�croit et que la d�croissance se fait en :math:`\alpha` selon
:math:`\alpha`, jusqu'� un certain seuil apr�s lequel le r�sidu est faible et
constant, cela signifie que :math:`F` est lin�aire et que le r�sidu d�croit �
partir de l'erreur faite dans le calcul du terme :math:`\nabla_xF`.

R�sidu "TaylorOnNorm"
*********************

On observe le r�sidu issu du d�veloppement de Taylor de la fonction :math:`F`,
rapport� au param�tre :math:`\alpha` au carr� :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) - \alpha * \nabla_xF(\mathbf{dx}) ||}{\alpha^2}

C'est un r�sidu essentiellement similaire au crit�re classique de Taylor d�crit
pr�c�demment, mais son comportement peut diff�rer selon les propri�t�s
num�riques des calculs de ses diff�rents termes.

Si le r�sidu est constant jusqu'� un certain seuil et croissant ensuite, cela
signifie que le gradient est bien calcul� jusqu'� cette pr�cision d'arr�t, et
que :math:`F` n'est pas lin�aire.

Si le r�sidu est syst�matiquement croissant en partant d'une valeur faible par
rapport � :math:`||F(\mathbf{x})||`, cela signifie que :math:`F` est
(quasi-)lin�aire et que le calcul du gradient est correct jusqu'au moment o� le
r�sidu est de l'ordre de grandeur de :math:`||F(\mathbf{x})||`.

R�sidu "Norm"
*************

On observe le r�sidu, qui est bas� sur une approximation du gradient :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) ||}{\alpha}

qui doit rester constant jusqu'� ce que l'on atteigne la pr�cision du calcul.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: CheckingPoint
.. index:: single: ObservationOperator
.. index:: single: AmplitudeOfInitialDirection
.. index:: single: EpsilonMinimumExponent
.. index:: single: InitialDirection
.. index:: single: ResiduFormula
.. index:: single: SetSeed
.. index:: single: StoreSupplementaryCalculations

Les commandes requises g�n�rales, disponibles dans l'interface en �dition, sont
les suivantes:

  CheckingPoint
    *Commande obligatoire*. Elle d�finit le vecteur utilis� comme l'�tat autour
    duquel r�aliser le test requis, not� :math:`\mathbf{x}` et similaire �
    l'�bauche :math:`\mathbf{x}^b`. Sa valeur est d�finie comme un objet de type
    "*Vector*".

  ObservationOperator
    *Commande obligatoire*. Elle indique l'op�rateur d'observation, not�e
    pr�c�demment :math:`H`, qui transforme les param�tres d'entr�e
    :math:`\mathbf{x}` en r�sultats :math:`\mathbf{y}` qui sont � comparer aux
    observations :math:`\mathbf{y}^o`.  Sa valeur est d�finie comme un objet de
    type "*Function*". Diff�rentes formes fonctionnelles peuvent �tre
    utilis�es, comme d�crit dans la section
    :ref:`section_ref_operator_requirements`. Si un contr�le :math:`U` est
    inclus dans le mod�le d'observation, l'op�rateur doit �tre appliqu� � une
    paire :math:`(X,U)`.

Les commandes optionnelles g�n�rales, disponibles dans l'interface en �dition,
sont indiqu�es dans la :ref:`section_ref_checking_keywords`. De plus, les
param�tres de la commande "*AlgorithmParameters*" permettent d'indiquer les
options particuli�res, d�crites ci-apr�s, de l'algorithme. On se reportera � la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  AmplitudeOfInitialDirection
    Cette cl� indique la mise � l'�chelle de la perturbation initiale construite
    comme un vecteur utilis� pour la d�riv�e directionnelle autour du point
    nominal de v�rification. La valeur par d�faut est de 1, ce qui signifie pas
    de mise � l'�chelle.

    Exemple : ``{"AmplitudeOfInitialDirection":0.5}``

  EpsilonMinimumExponent
    Cette cl� indique la valeur de l'exposant minimal du coefficient en
    puissance de 10 qui doit �tre utilis� pour faire d�cro�tre le multiplicateur
    de l'incr�ment. La valeur par d�faut est de -8, et elle doit �tre entre 0 et
    -20. Par exemple, la valeur par d�faut conduit � calculer le r�sidu de la
    formule avec un incr�ment fixe multipli� par 1.e0 jusqu'� 1.e-8.

    Exemple : ``{"EpsilonMinimumExponent":-12}``

  InitialDirection
    Cette cl� indique la direction vectorielle utilis�e pour la d�riv�e
    directionnelle autour du point nominal de v�rification. Cela doit �tre un
    vecteur. Si elle n'est pas sp�cifi�e, la direction par d�faut est une
    perturbation par d�faut autour de z�ro de la m�me taille vectorielle que le
    point de v�rification.

    Exemple : ``{"InitialDirection":[0.1,0.1,100.,3}``

  ResiduFormula
    Cette cl� indique la formule de r�sidu qui doit �tre utilis�e pour le test.
    Le choix par d�faut est "Taylor", et les choix possibles sont "Taylor"
    (r�sidu du d�veloppement de Taylor normalis� de l'op�rateur, qui doit
    d�cro�tre comme le carr� de la perturbation), "TaylorOnNorm" (r�sidu du
    d�veloppement de Taylor rapport� � la perturbation de l'op�rateur, qui doit
    rester constant) et "Norm" (r�sidu obtenu en prenant la norme du
    d�veloppement de Taylor � l'ordre 0, qui approxime le gradient, et qui doit
    rester constant).

    Exemple : ``{"ResiduFormula":"Taylor"}``

  SetSeed
    Cette cl� permet de donner un nombre entier pour fixer la graine du
    g�n�rateur al�atoire utilis� pour g�n�rer l'ensemble. Un valeur pratique est
    par exemple 1000. Par d�faut, la graine est laiss�e non initialis�e, et elle
    utilise ainsi l'initialisation par d�faut de l'ordinateur.

    Exemple : ``{"SetSeed":1000}``

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage co�teux. La valeur par d�faut est une liste vide,
    aucune de ces variables n'�tant calcul�e et stock�e par d�faut. Les noms
    possibles sont dans la liste suivante : ["CurrentState", "Residu",
    "SimulatedObservationAtCurrentState"].

    Exemple : ``{"StoreSupplementaryCalculations":["CurrentState"]}``

Informations et variables disponibles � la fin de l'algorithme
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

En sortie, apr�s ex�cution de l'algorithme, on dispose d'informations et de
variables issues du calcul. La description des
:ref:`section_ref_output_variables` indique la mani�re de les obtenir par la
m�thode nomm�e ``get`` de la variable "*ADD*" du post-processing. Les variables
d'entr�e, mises � disposition de l'utilisateur en sortie pour faciliter
l'�criture des proc�dures de post-processing, sont d�crites dans
l':ref:`subsection_r_o_v_Inventaire`.

Les sorties non conditionnelles de l'algorithme sont les suivantes:

  Residu
    *Liste de valeurs*. Chaque �l�ment est la valeur du r�sidu particulier
    v�rifi� lors d'un algorithme de v�rification, selon l'ordre des tests
    effectu�s.

    Exemple : ``r = ADD.get("Residu")[:]``

Les sorties conditionnelles de l'algorithme sont les suivantes:

  CurrentState
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�tat courant utilis�
    au cours du d�roulement de l'algorithme d'optimisation.

    Exemple : ``Xs = ADD.get("CurrentState")[:]``

  SimulatedObservationAtCurrentState
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'observation simul� �
    partir de l'�tat courant, c'est-�-dire dans l'espace des observations.

    Exemple : ``hxs = ADD.get("SimulatedObservationAtCurrentState")[-1]``

Voir aussi
++++++++++

R�f�rences vers d'autres sections :
  - :ref:`section_ref_algorithm_FunctionTest`
  - :ref:`section_ref_algorithm_LinearityTest`
  - :ref:`section_ref_algorithm_TangentTest`
  - :ref:`section_ref_algorithm_AdjointTest`
