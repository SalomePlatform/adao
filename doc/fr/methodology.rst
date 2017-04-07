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

.. _section_methodology:

===========================================================================================
**[DocT]** M�thodologie pour �laborer une �tude d'Assimilation de Donn�es ou d'Optimisation
===========================================================================================

Cette section pr�sente un m�thodologie g�n�rique pour construire une �tude
d'Assimilation de Donn�es ou d'Optimisation. Elle d�crit les �tapes
conceptuelles pour �tablir de mani�re ind�pendante cette �tude. Elle est
ind�pendante de tout outil, mais le module ADAO permet de mettre en oeuvre
efficacement une telle �tude.

Proc�dure logique pour une �tude
--------------------------------

Pour une �tude g�n�rique d'Assimilation de Donn�es ou d'Optimisation, les
principales �tapes m�thodologiques peuvent �tre les suivantes:

    - :ref:`section_m_step1`
    - :ref:`section_m_step2`
    - :ref:`section_m_step3`
    - :ref:`section_m_step4`
    - :ref:`section_m_step5`
    - :ref:`section_m_step6`
    - :ref:`section_m_step7`

Chaque �tape est d�taill�e dans la section suivante.

Proc�dure d�taill�e pour une �tude
----------------------------------

.. _section_m_step1:

�TAPE 1: Sp�cifier la r�solution du syst�me physique et les param�tres � ajuster
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Une source essentielle de connaissance du syst�me physique �tudi� est la
simulation num�rique. Elle est souvent disponible � travers un ou des cas de
calcul, et elle est symbolis�e par un **op�rateur de simulation** (pr�c�demment
inclus dans :math:`H`). Un cas de calcul standard rassemble des hypoth�ses de
mod�les, une impl�mentation num�rique, des capacit�s de calcul, etc. de mani�re
� repr�senter le comportement du syst�me physique. De plus, un cas de calcul est
caract�ris� par exemple par ses besoins en temps de calcul et en m�moire, par la
taille de ses donn�es et de ses r�sultats, etc. La connaissance de tous ces
�l�ments est primordiale dans la mise au point d'une �tude d'assimilation de
donn�es ou d'optimisation.

Pour �tablir correctement une �tude, il faut aussi choisir les inconnues
d'optimisation incluses dans la simulation. Fr�quemment, cela peut �tre � l'aide
de mod�les physiques dont les param�tres peuvent �tre ajust�s. De plus, il est
toujours utile d'ajouter une connaissance de type sensibilit�, comme par exemple
celle de la simulation par rapport aux param�tres qui peuvent �tre ajust�s. Des
�l�ments plus g�n�raux, comme la stabilit� ou la r�gularit� de la simulation par
rapport aux inconnues en entr�e, sont aussi d'un grand int�r�t.

En pratique, les m�thodes d'optimisation peuvent requ�rir une information de
type gradient de la simulation par rapport aux inconnues. Dans ce cas, le
gradient explicite du code doit �tre donn�, ou le gradient num�rique doit �tre
�tabli. Sa qualit� est en relation avec la stabilit� ou la r�gularit� du code de
simulation, et elle doit �tre v�rifi�e avec soin avant de mettre en oeuvre les
calculs d'optimisation. Des conditions sp�cifiques doivent �tre utilis�es pour
ces v�rifications.

Un **op�rateur d'observation** est toujours requis, en compl�ment � l'op�rateur
de simulation. Cet op�rateur d'observation, not� :math:`H` ou inclus dedans,
doit convertir les sorties de la simulation num�rique en quelque-chose qui est
directement comparable aux observations. C'est un op�rateur essentiel, car il
est le moyen pratique de comparer les simulations et les observations. C'est
usuellement r�alis� par �chantillonnage, projection ou int�gration, des sorties
de simulation, mais cela peut �tre plus compliqu�. Souvent, du fait que
l'op�rateur d'observation fasse directement suite � celui de simulation dans un
sch�ma simple d'assimilation de donn�es, cet op�rateur d'observation utilise
fortement les capacit�s de post-traitement et d'extraction du code de
simulation.

.. _section_m_step2:

�TAPE 2: Sp�cifier les crit�res de qualification des r�sultats physiques
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Comme les syst�mes �tudi�s ont une r�alit� physique, il est important d'exprimer
les **information physiques qui peuvent aider � qualifier un �tat simul� du
syst�me**. Il y a deux grand types d'informations qui conduisent � des crit�res
permettant la qualification et la quantification de r�sultats d'optimisation.

Premi�rement, provenant d'une connaissance math�matique ou num�rique, un grand
nombre d'indicateurs standards permettent de qualifier, en relatif ou en absolu,
l'int�r�t d'un �tat optimal. Par exemple, des �quations d'�quilibre ou des
conditions de fermeture sont des mesures compl�mentaires de la qualit� d'un �tat
du syst�me. Des crit�res bien choisis comme des RMS, des RMSE, des extrema de
champs, des int�grales, etc. permettent d'�valuer la qualit� d'un �tat optimis�.

Deuxi�mement, provenant d'une connaissance physique ou exp�rimentale, des
informations utiles peuvent �tre obtenus � partir de l'interpr�tation des
r�sultats d'optimisation. En particulier, la validit� physique ou l'int�r�t
technique permettent d'�valuer l'int�r�t de r�sultats des r�sultats num�riques
de l'optimisation.

Pour obtenir une information signifiante de ces deux types de connaissances, il
est recommand�, si possible, de construire des crit�res num�riques pour
faciliter l'�valuation de la qualit� globale des r�sultats num�riques

.. _section_m_step3:

�TAPE 3: Identifier et d�crire les observations disponibles
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

En tant que seconde source d'information principale � propos du syst�me physique
� �tudier, les **observations, ou mesures,** not�es :math:`\mathbf{y}^o`,
doivent �tre d�crites avec soin. La qualit� des mesures, leur erreurs
intrins�ques, leur particularit�s, sont importantes � conna�tre, pour pouvoir
introduire ces informations dans les calculs d'assimilation de donn�es ou
d'optimisation.

Les observations doivent non seulement �tre disponibles, mais aussi doivent
pouvoir �tre introduites efficacement dans l'environnement num�rique de calcul
ou d'optimisation. Ainsi l'environnement d'acc�s num�rique aux observations est
fondamental pour faciliter l'usage effectif de mesures vari�es et de sources
diverses, et pour encourager des essais extensifs utilisant des mesures.
L'environnement d'acc�s num�rique int�gre la disponibilit� de bases de donn�es
ou pas, les formats de donn�es, les interfaces d'acc�s, etc.

.. _section_m_step4:

�TAPE 4: Sp�cifier les �l�ments de mod�lisation de l'AD/Optimisation (covariances, �bauche...)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Des �l�ments suppl�mentaires de mod�lisation en Assimilation de Donn�es ou en
Optimisation permettent d'am�liorer l'information � propos de la repr�sentation
d�taill�e du syst�me physique �tudi�.

La connaissance *a-priori* de l'�tat du syst�me peut �tre repr�sent�e en
utilisant l'**�bauche**, not�e :math:`\mathbf{x}^b`, et la **matrice de
covariance des erreurs d'�bauche**, not�e :math:`\mathbf{B}`. Ces informations
sont extr�mement importantes � compl�ter, en particulier pour obtenir des
r�sultats signifiants en Assimilation de Donn�es.

Par ailleurs, des informations sur les erreurs d'observation peuvent �tre
utilis�es pour compl�ter la **matrice de covariance des erreurs d'observation**,
not�e :math:`\mathbf{R}`. Comme pour :math:`\mathbf{B}`, il est recommand�
d'utiliser des informations soigneusement v�rifi�es pour renseigner ces matrices
de covariances.

Dans le cas de simulations dynamiques, il est de plus n�cessaire de d�finir un
**op�rateur d'�volution** et la **matrice de covariance des erreurs
d'�volution** associ�e.

.. _section_m_step5:

�TAPE 5: Choisir l'algorithme d'optimisation et ses param�tres
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

L'Assimilation de Donn�es ou l'Optimisation demandent de r�soudre un probl�me
d'optimisation, le plus souvent sous la forme d'un probl�me de minimisation.
Selon la disponibilit� du gradient de la fonction co�t en fonction des
param�tres d'optimisation, la classe recommand�e de m�thodes sera diff�rente.
Les m�thodes d'optimisation variationnelles ou avec lin�arisation locale
n�cessitent ce gradient. A l'oppos�, les m�thodes sans d�riv�es ne n�cessitent
pas ce gradient, mais pr�sentent souvent un co�t de calcul notablement
sup�rieur.

A l'int�rieur m�me d'une classe de m�thodes d'optimisation, pour chaque m�thode,
il y a usuellement un compromis � faire entre les *"capacit�s g�n�riques de la
m�thode"* et ses *"performances particuli�res sur un probl�me sp�cifique"*. Les
m�thodes les plus g�n�riques, comme par exemple la minimisation variationnelle
utilisant l':ref:`section_ref_algorithm_3DVAR`, pr�sentent de remarquables
propri�t�s num�riques d'efficacit�, de robustesse et de fiabilit�, ce qui
conduit � les recommander ind�pendamment du probl�me � r�soudre. De plus, il est
souvent difficile de r�gler les param�tres d'une m�thode d'optimisation, donc la
m�thodes la plus robuste est souvent celle qui pr�sente le moins de param�tres.
Au final, au moins au d�but, il est recommand� d'utiliser les m�thodes les plus
g�n�riques et de changer le moins possible les param�tres par d�faut connus.

.. _section_m_step6:

�TAPE 6: Conduire les calculs d'optimisation et obtenir les r�sultats
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Apr�s avoir mis au point une �tude d'Assimilation de Donn�es ou d'Optimisation,
les calculs doivent �tre conduits de mani�re efficace.

Comme l'optimisation requiert usuellement un grand nombre de simulations
physiques �l�mentaires du syst�me, les calculs sont souvent effectu�s dans un
environnement de calculs hautes performances (HPC, ou Hight Performance
Computing) pour r�duire le temps complet d'utilisateur. M�me si le probl�me
d'optimisation est petit, le temps de simulation du syst�me physique peut �tre
long, n�cessitant des ressources de calcul cons�quentes. Ces besoins doivent
�tre pris en compte suffisamment t�t dans la proc�dure d'�tude pour �tre
satisfaits sans n�cessiter un effort trop important.

Pour la m�me raison de besoins de calculs importants, il est aussi important de
pr�parer soigneusement les sorties de la proc�dure d'optimisation. L'�tat
optimal est la principale information requise, mais un grand nombre d'autres
informations sp�ciales peuvent �tre obtenues au cours du calcul d'optimisation
ou � la fin: �valuation des erreurs, �tats interm�diaires, indicateurs de
qualit�, etc. Toutes ces informations, n�cessitant parfois des calculs
additionnels, doivent �tre connues et demand�es au d�but du processus
d'optimisation.

.. _section_m_step7:

�TAPE 7: Exploiter les r�sultats et qualifier leur pertinence physique
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Une fois les r�sultats obtenus, ils doivent �tre interpr�t�s en termes de
significations physique et num�rique. M�me si la d�marche d'optimisation donne
toujours un nouvel �tat optimal qui est au moins aussi bon que l'�tat *a
priori*, et le plus souvent meilleur, cet �tat optimal doit par exemple �tre
v�rifi� par rapport aux crit�res de qualit� identifi�s au moment de
:ref:`section_m_step2`. Cela peut conduire � des �tudes statistiques ou
num�riques de mani�re � �valuer l'int�r�t d'un �tat optimal pour repr�senter la
syst�me physique.

Au-del� de cette analyse qui doit �tre r�alis�e pour chaque �tude d'Assimilation
de Donn�es ou d'Optimisation, il est tr�s utile d'exploiter les r�sultats
d'optimisation comme une partie int�gr�e dans une �tude plus compl�te du syst�me
physique d'int�r�t.
