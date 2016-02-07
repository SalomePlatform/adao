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

.. index:: single: AlgorithmParameters
.. index:: single: Parameters
.. index:: single: Defaults
.. _section_ref_options_Algorithm_Parameters:

Description des options d'un algorithme dans "*AlgorithmParameters*"
--------------------------------------------------------------------

Chaque algorithme peut �tre contr�l� en utilisant des options ou des param�tres
particuliers. Ils sont donn�s � travers la commande optionnelle "*Parameters*"
incluse dans la commande obligatoire "*AlgorithmParameters*".

Il y a 3 m�thodes pratiques pour l'utilisateur pour fournir ces options. La
m�thode est d�termin�e de la mani�re suivante dans l'interface graphique
d'�dition :

#. premi�rement � l'aide du mot-cl� "*Parameters*" dans la commande "*AlgorithmParameters*", qui permet de choisir entre "*Defaults*" (utilisation de mots-cl�s explicites pr�-remplis par les valeurs par d�faut des param�tres) et "*Dict*" (utilisation d'un dictionnaire pour renseigner les mots-cl�s n�cessaires),
#. puis deuxi�mement, uniquement dans le cas "*Dict*" de "*Parameters*", par le mot-cl� "*FROM*" inclus qui permet de choisir entre une entr�e par cha�ne de caract�res ou une entr�e par fichier de script Python.

Si une option ou un param�tre est sp�cifi� par l'utilisateur pour un algorithme
qui ne la supporte pas, cette option est simplement laiss�e inutilis�e et ne
bloque pas le traitement. La signification des acronymes ou des noms
particuliers peut �tre trouv�e dans l':ref:`genindex` ou dans le
:ref:`section_glossary`.

Premi�re m�thode : utiliser les mots-cl�s explicites pr�-remplis
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour donner les valeurs des param�tres par les mots-cl�s explicites pr�-remplis,
directement dans l'interface graphique, l'utilisateur s�lectionne le type
"*Defaults*" dans le mot-cl� "*Parameters*", puis les mots-cl�s dans la liste
pr�vue "*Parameters[Algo]*" qui appara�t, associ�e � l'algorithme choisi, comme
montr� dans la figure qui suit :

  .. adao_algopar_defaults:
  .. image:: images/adao_algopar_defaults.png
    :align: center
    :width: 100%
  .. centered::
    **Utiliser les mots-cl�s explicites pr�-remplis pour les param�tres algorithmiques**

Chaque param�tre est optionnel, et il pr�sente sa valeur par d�faut lorsqu'il
est s�lectionn� par l'utilisateur. On peut alors modifier sa valeur, ou la
renseigner dans le cas de listes par exemple.

C'est la mani�re recommand�e pour modifier uniquement une partie des param�tres
algorithmiques de mani�re s�re. Cette m�thode ne permet de d�finir que les
param�tres autoris�s pour un algorithme donn�, et les valeurs d�finies ne sont
pas conserv�es si l'utilisateur change d'algorithme.

Seconde m�thode : utiliser une cha�ne de caract�res dans l'interface graphique
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour donner les valeurs des param�tres par une cha�ne de caract�res, directement
dans l'interface graphique, l'utilisateur s�lectionne le type "*Dict*" dans le
mot-cl� "*Parameters*", puis le type "*String*" dans le mot-cl� "*FROM*" de la
commande "*Dict*" qui appara�t, comme montr� dans la figure qui suit :

  .. adao_algopar_string:
  .. image:: images/adao_algopar_string.png
    :align: center
    :width: 100%
  .. centered::
    **Utiliser une cha�ne de caract�res pour les param�tres algorithmiques**

Dans le champs de saisie, il faut utiliser des guillemets simples pour une
d�finition standard de dictionnaire, comme par exemple::

    '{"MaximumNumberOfSteps":25,"SetSeed":1000}'

C'est la mani�re recommand�e pour d�finir des param�tres algorithmiques. Cette
m�thode permet en particulier de conserver des options ou des param�tres pour
d'autres algorithmes que celui que l'on utilise au moment pr�sent. Cela facilite
le changement d'algorithme ou la conservation de valeurs par d�faut diff�rentes
des d�fauts standards.

Troisi�me m�thode : utiliser un fichier de script Python externe
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour donner les valeurs des param�tres par un fichier de script Python externe,
l'utilisateur s�lectionne dans l'interface graphique le type "*Dict*" dans le
mot-cl� "*Parameters*", puis le type "*Script*" dans le mot-cl� "*FROM*" de la
commande "*Dict*" qui appara�t, comme montr� dans la figure qui suit :

  .. :adao_algopar_script
  .. image:: images/adao_algopar_script.png
    :align: center
    :width: 100%
  .. centered::
    **Utiliser un fichier externe pour les param�tres algorithmiques**

Ce fichier script Python externe doit d�finir alors une variable au nom impos�
"*AlgorithmParameters*", � la mani�re de l'exemple qui suit::

    AlgorithmParameters = {
        "MaximumNumberOfSteps" : 25,
        "StoreSupplementaryCalculations" : ["APosterioriCovariance","OMA"],
        }

Le fichier peut aussi contenir d'autres commandes Python. Cette m�thode permet
aussi, comme la pr�c�dente, de conserver des options ou des param�tres pour
d'autres algorithmes que celui que l'on utilise.
