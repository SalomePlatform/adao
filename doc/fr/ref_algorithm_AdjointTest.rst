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

.. index:: single: AdjointTest
.. _section_ref_algorithm_AdjointTest:

Algorithme de v�rification "*AdjointTest*"
------------------------------------------

Description
+++++++++++

Cet algorithme permet de v�rifier la qualit� de l'op�rateur adjoint, en
calculant un r�sidu dont les propri�t�s th�oriques sont connues.

On observe le r�sidu suivant, qui est la diff�rence de deux produits scalaires :

.. math:: R(\alpha) = | < TangentF_x(\mathbf{dx}) , \mathbf{y} > - < \mathbf{dx} , AdjointF_x(\mathbf{y}) > |

qui doit rester constamment �gal � z�ro � la pr�cision du calcul. On prend
:math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` et
:math:`\mathbf{dx}=\alpha*\mathbf{dx}_0`. :math:`F` est le code de calcul.
:math:`\mathbf{y}` doit �tre dans l'image de :math:`F`. S'il n'est pas donn�, on
prend :math:`\mathbf{y} = F(\mathbf{x})`.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: CheckingPoint
.. index:: single: ObservationOperator
.. index:: single: AmplitudeOfInitialDirection
.. index:: single: EpsilonMinimumExponent
.. index:: single: InitialDirection
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

  EpsilonMinimumExponent
    Cette cl� indique la valeur de l'exposant minimal du coefficient en
    puissance de 10 qui doit �tre utilis� pour faire d�cro�tre le multiplicateur
    de l'incr�ment. La valeur par d�faut est de -8, et elle doit �tre entre 0 et
    -20. Par exemple, la valeur par d�faut conduit � calculer le r�sidu de la
    formule avec un incr�ment fixe multipli� par 1.e0 jusqu'� 1.e-8.

  InitialDirection
    Cette cl� indique la direction vectorielle utilis�e pour la d�riv�e
    directionnelle autour du point nominal de v�rification. Cela doit �tre un
    vecteur. Si elle n'est pas sp�cifi�e, la direction par d�faut est une
    perturbation par d�faut autour de z�ro de la m�me taille vectorielle que le
    point de v�rification.

  SetSeed
    Cette cl� permet de donner un nombre entier pour fixer la graine du
    g�n�rateur al�atoire utilis� pour g�n�rer l'ensemble. Un valeur pratique est
    par exemple 1000. Par d�faut, la graine est laiss�e non initialis�e, et elle
    utilise ainsi l'initialisation par d�faut de l'ordinateur.

Voir aussi
++++++++++

R�f�rences vers d'autres sections :
  - :ref:`section_ref_algorithm_FunctionTest`
  - :ref:`section_ref_algorithm_TangentTest`
  - :ref:`section_ref_algorithm_GradientTest`
