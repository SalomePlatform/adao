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

.. index:: single: LinearityTest
.. _section_ref_algorithm_LinearityTest:

Algorithme de v�rification "*LinearityTest*"
--------------------------------------------

Description
+++++++++++

Cet algorithme permet de v�rifier la qualit� de lin�arit� de l'op�rateur, en
calculant un r�sidu dont les propri�t�s th�oriques sont connues. Plusieurs
formules de r�sidu sont utilisables.

Dans tous les cas, on prend :math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` et
:math:`\mathbf{dx}=\alpha*\mathbf{dx}_0`. :math:`F` est le code de calcul.

R�sidu "CenteredDL"
*******************

On observe le r�sidu suivant, provenant de la diff�rence centr�e des valeurs de
:math:`F` au point nominal et aux points perturb�s, normalis�e par la valeur au
point nominal :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) + F(\mathbf{x}-\alpha*\mathbf{dx}) - 2*F(\mathbf{x}) ||}{|| F(\mathbf{x}) ||}

S'il reste constamment tr�s faible par rapport � 1, l'hypoth�se de lin�arit�
de :math:`F` est v�rifi�e.

Si le r�sidu varie, ou qu'il est de l'ordre de 1 ou plus, et qu'il n'est
faible qu'� partir d'un certain ordre d'incr�ment, l'hypoth�se de lin�arit�
de :math:`F` n'est pas v�rifi�e.

Si le r�sidu d�croit et que la d�croissance se fait en :math:`\alpha^2` selon
:math:`\alpha`, cela signifie que le gradient est bien calcul� jusqu'au niveau
d'arr�t de la d�croissance quadratique.

R�sidu "Taylor"
***************

On observe le r�sidu issu du d�veloppement de Taylor de la fonction :math:`F`,
normalis�e par la valeur au point nominal :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) - \alpha * \nabla_xF(\mathbf{dx}) ||}{|| F(\mathbf{x}) ||}

S'il reste constamment tr�s faible par rapport � 1, l'hypoth�se de lin�arit�
de :math:`F` est v�rifi�e.

Si le r�sidu varie, ou qu'il est de l'ordre de 1 ou plus, et qu'il n'est
faible qu'� partir d'un certain ordre d'incr�ment, l'hypoth�se de lin�arit�
de :math:`F` n'est pas v�rifi�e.

Si le r�sidu d�croit et que la d�croissance se fait en :math:`\alpha^2` selon
:math:`\alpha`, cela signifie que le gradient est bien calcul� jusqu'au niveau
d'arr�t de la d�croissance quadratique.

R�sidu "NominalTaylor"
**********************

On observe le r�sidu obtenu � partir de deux approximations d'ordre 1 de
:math:`F(\mathbf{x})`, normalis�es par la valeur au point nominal :

.. math:: R(\alpha) = \max(|| F(\mathbf{x}+\alpha*\mathbf{dx}) - \alpha * F(\mathbf{dx}) || / || F(\mathbf{x}) ||,|| F(\mathbf{x}-\alpha*\mathbf{dx}) + \alpha * F(\mathbf{dx}) || / || F(\mathbf{x}) ||)

S'il reste constamment �gal � 1 � moins de 2 ou 3 pourcents pr�s (c'est-�-dire
que :math:`|R-1|` reste �gal � 2 ou 3 pourcents), c'est que l'hypoth�se de
lin�arit� de :math:`F` est v�rifi�e.

S'il est �gal � 1 sur une partie seulement du domaine de variation de
l'incr�ment :math:`\alpha`, c'est sur sous-domaine que l'hypoth�se de lin�arit�
de :math:`F` est v�rifi�e.

R�sidu "NominalTaylorRMS"
*************************

On observe le r�sidu obtenu � partir de deux approximations d'ordre 1 de
:math:`F(\mathbf{x})`, normalis�es par la valeur au point nominal, dont on
calcule l'�cart quadratique (RMS) avec la valeur au point nominal :

.. math:: R(\alpha) = \max(RMS( F(\mathbf{x}), F(\mathbf{x}+\alpha*\mathbf{dx}) - \alpha * F(\mathbf{dx}) ) / || F(\mathbf{x}) ||,RMS( F(\mathbf{x}), F(\mathbf{x}-\alpha*\mathbf{dx}) + \alpha * F(\mathbf{dx}) ) / || F(\mathbf{x}) ||)

S'il reste constamment �gal � 0 � moins de 1 ou 2 pourcents pr�s, c'est
que l'hypoth�se de lin�arit� de F est v�rifi�e.

S'il est �gal � 0 sur une partie seulement du domaine de variation de
l'incr�ment :math:`\alpha`, c'est sur cette partie que l'hypoth�se de lin�arit�
de F est v�rifi�e.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: CheckingPoint
.. index:: single: ObservationOperator
.. index:: single: AmplitudeOfInitialDirection
.. index:: single: EpsilonMinimumExponent
.. index:: single: InitialDirection
.. index:: single: ResiduFormula
.. index:: single: SetSeed

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
sont indiqu�es dans la :ref:`section_ref_checking_keywords`. En particulier, la
commande optionnelle "*AlgorithmParameters*" permet d'indiquer les options
particuli�res, d�crites ci-apr�s, de l'algorithme. On se reportera � la
:ref:`section_ref_options_AlgorithmParameters` pour le bon usage de cette
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
    Le choix par d�faut est "CenteredDL", et les choix possibles sont
    "CenteredDL" (r�sidu de la diff�rence entre la fonction au point nominal et
    ses valeurs avec des incr�ments positif et n�gatif, qui doit rester tr�s
    faible), "Taylor" (r�sidu du d�veloppement de Taylor de l'op�rateur
    normalis� par sa valeur nominal, qui doit rester tr�s faible),
    "NominalTaylor" (r�sidu de l'approximation � l'ordre 1 de l'op�rateur,
    normalis� au point nominal, qui doit rester proche de 1), et
    "NominalTaylorRMS" (r�sidu de l'approximation � l'ordre 1 de l'op�rateur,
    normalis� par l'�cart quadratique moyen (RMS) au point nominal, qui doit
    rester proche de 0).

    Exemple : ``{"ResiduFormula":"CenteredDL"}``

  SetSeed
    Cette cl� permet de donner un nombre entier pour fixer la graine du
    g�n�rateur al�atoire utilis� pour g�n�rer l'ensemble. Un valeur pratique est
    par exemple 1000. Par d�faut, la graine est laiss�e non initialis�e, et elle
    utilise ainsi l'initialisation par d�faut de l'ordinateur.

    Exemple : ``{"SetSeed":1000}``

Voir aussi
++++++++++

R�f�rences vers d'autres sections :
  - :ref:`section_ref_algorithm_FunctionTest`
