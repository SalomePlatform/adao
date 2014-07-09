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

.. index:: single: ObserverTest
.. _section_ref_algorithm_ObserverTest:

Algorithme de v�rification "*ObserverTest*"
-------------------------------------------

Description
+++++++++++

Cet algorithme permet de v�rifier une fonction externe et fournie par
l'utilisateur, utilis�e comme un *observer*. Cette fonction externe peut �tre
appliqu�e � chacune des variables potentiellement observables. Elle n'est
activ�e que sur celles qui sont explicitement associ�es avec l'*observer* dans
l'interface.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: CheckingPoint
.. index:: single: ObservationOperator
.. index:: single: Observers

Les commandes requises g�n�rales, disponibles dans l'interface en �dition, sont
les suivantes:

  Observers  
    *Commande obligatoire*. Elle permet de d�finir des observateurs internes,
    qui sont des fonctions li�es � une variable particuli�re, qui sont ex�cut�es
    chaque fois que cette variable est modifi�e. C'est une mani�re pratique de
    suivre des variables d'int�r�t durant le processus d'assimilation de donn�es
    ou d'optimisation, en l'affichant ou en la tra�ant, etc. Des exemples
    courants (squelettes) sont fournis pour aider l'utilisateur ou pour
    faciliter l'�laboration d'un cas.

Les commandes optionnelles g�n�rales, disponibles dans l'interface en �dition,
sont indiqu�es dans la :ref:`section_ref_checking_keywords`.
    
*Astuce pour cet algorithme :*

    Comme les commandes *"CheckingPoint"* et *"ObservationOperator"* sont
    requises pour TOUS les algorithmes de v�rification dans l'interface, vous
    devez fournir une valeur, malgr� le fait que ces commandes ne sont pas
    requises pour *"ObserverTest"*, et ne seront pas utilis�es. La mani�re la
    plus simple est de donner "1" comme un STRING pour les deux,
    l'*"ObservationOperator"* devant �tre de type *Matrix*.
