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

.. index:: single: AlgorithmParameters
.. _section_ref_options_AlgorithmParameters:

Description des options d'un algorithme par "*AlgorithmParameters*"
-------------------------------------------------------------------

Chaque algorithme peut �tre contr�l� en utilisant des options particuli�res,
donn�es � travers la commande optionnelle "*AlgorithmParameters*".

Il y a 2 m�thodes pratiques pour l'utilisateur pour fournir ces options. La
m�thode est choisie � l'aide du mot-cl� "*FROM*", inclus dans l'entr�e
"*AlgorithmParameters*" dans EFICAS.

Si une option est sp�cifi�e par l'utilisateur pour un algorithme qui ne la
supporte pas, cette option est simplement laiss�e inutilis�e et ne bloque pas le
traitement. La signification des acronymes ou des noms particuliers peut �tre
trouv�e dans l':ref:`genindex` ou dans le :ref:`section_glossary`.

Premi�re m�thode : utiliser une cha�ne de caract�res dans EFICAS
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour donner les valeurs de la commande "*AlgorithmParameters*" par une cha�ne de
caract�res, directement dans l'interface graphique EFICAS, l'utilisateur
s�lectionne ce type dans le mot-cl� "*FROM*", comme montr� dans la figure qui
suit :

  .. adao_algopar_string:
  .. image:: images/adao_algopar_string.png
    :align: center
    :width: 100%
  .. centered::
    **Utiliser une cha�ne de caract�res pour les param�tres algorithmiques**

Dans le champs de saisie, il faut utiliser des guillemets simples pour une
d�finition standard de dictionnaire, comme par exemple::

    '{"StoreInternalVariables":True,"MaximumNumberOfSteps":25}'

C'est la mani�re recommand�e pour d�finir des param�tres algorithmiques.

Seconde m�thode : utiliser un fichier de script Python externe
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour donner les valeurs de la commande "*AlgorithmParameters*" par un fichier de
script Python externe, l'utilisateur s�lectionne dans EFICAS ce type dans le
mot-cl� "*FROM*", comme montr� dans la figure qui suit :

  .. :adao_algopar_script
  .. image:: images/adao_algopar_script.png
    :align: center
    :width: 100%
  .. centered::
    **Utiliser un fichier externe pour les param�tres algorithmiques**

Ce fichier script Python externe doit d�finir alors une variable au nom impos�
"*AlgorithmParameters*", � la mani�re de l'exemple qui suit::

    AlgorithmParameters = {
        "StoreInternalVariables" : True,
        "MaximumNumberOfSteps" : 25,
        "StoreSupplementaryCalculations" : ["APosterioriCovariance","OMA"],
        }

Le fichier peut aussi contenir d'autres commandes Python.
