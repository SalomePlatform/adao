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

.. index:: single: FunctionTest
.. _section_ref_algorithm_FunctionTest:

Algorithme de v�rification "*FunctionTest*"
-------------------------------------------

Description
+++++++++++

Cet algorithme permet de v�rifier que l'op�rateur d'observation fonctionne
correctement et que son appel se d�roule de mani�re compatible avec son usage
dans les algorithmes d'ADAO. De mani�re pratique, il permet d'appeler une ou
plusieurs fois l'op�rateur, en activant ou non le mode "debug" lors de
l'ex�cution.

Une statistique sur les vecteurs en entr�e et en sortie de chaque ex�cution de
l'op�rateur est indiqu�e, et une autre globale est fournie de mani�re
r�capitulative � la fin de l'algorithme de v�rification. La pr�cision
d'affichage est contr�lable pour permettre l'automatisation des tests
d'op�rateur.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: CheckingPoint
.. index:: single: ObservationOperator
.. index:: single: NumberOfPrintedDigits
.. index:: single: NumberOfRepetition
.. index:: single: SetDebug

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
param�tres de la commande "*AlgorithmParameters*" permettent d'indiquer les options
particuli�res, d�crites ci-apr�s, de l'algorithme. On se reportera � la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  NumberOfPrintedDigits
    Cette cl� indique le nombre de d�cimales de pr�cision pour les affichages de
    valeurs r�elles. La valeur par d�faut est 5, avec un minimum de 0.

    Exemple : ``{"NumberOfPrintedDigits":5}``

  NumberOfRepetition
    Cette cl� indique le nombre de fois o� r�p�ter l'�valuation de la fonction.
    La valeur par d�faut est 1.

    Exemple : ``{"NumberOfRepetition":3}``

  SetDebug
    Cette cl� requiert l'activation, ou pas, du mode de d�bogage durant
    l'�valuation de la fonction. La valeur par d�faut est "True", les choix sont
    "True" ou "False".

    Exemple : ``{"SetDebug":False}``

Voir aussi
++++++++++

R�f�rences vers d'autres sections :
  - :ref:`section_ref_algorithm_LinearityTest`
