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

.. _section_theory:

=================================================================================
**[DocT]** Une br�ve introduction � l'Assimilation de Donn�es et � l'Optimisation
=================================================================================

.. index:: single: Data Assimilation
.. index:: single: assimilation de donn�es
.. index:: single: �tat vrai
.. index:: single: observation
.. index:: single: a priori

L'**assimilation de donn�es** est un cadre g�n�ral pour le calcul de
l'estimation optimale de l'�tat r�el d'un syst�me, au cours du temps si
n�cessaire. Il utilise les valeurs obtenues en combinant des observations et des
mod�les *a priori*, incluant de plus des informations sur leurs erreurs.

En d'autres termes, l'assimilation de donn�es rassemble les donn�es mesur�es
d'un syst�me, qui sont les observations, avec une connaissance physique et
math�matique *a priori* du syst�me, int�gr�e dans les mod�les num�riques, afin
d'obtenir la meilleure estimation possible de l'�tat r�el du syst�me et de ses
propri�t�s stochastiques. On note que cet �tat r�el (ou "�tat" vrai") ne peut
�tre atteint, mais peut seulement �tre estim�. De plus, malgr� le fait que les
informations utilis�es sont stochastiques par nature, l'assimilation de donn�es
fournit des techniques d�terministes afin de r�aliser l'estimation de mani�re
tr�s efficace.

L'assimilation de donn�es cherchant l'estimation la **meilleure possible**, la
d�marche technique sous-jacente int�gre toujours de l'optimisation afin de
trouver cette estimation : des m�thodes d'optimisation choisies sont toujours
int�gr�s dans les algorithmes d'assimilation de donn�es. Par ailleurs, les
m�thodes d'optimisation peuvent �tre vues dans ADAO comme un moyen d'�tendre les
applications d'assimilation de donn�es. Elles seront pr�sent�es de cette fa�on
dans la section pour `Approfondir l'estimation d'�tat par des m�thodes
d'optimisation`_, mais elles sont beaucoup plus g�n�rale et peuvent �tre
utilis�s sans les concepts d'assimilation de donn�es.

Deux types principaux d'applications existent en assimilation de donn�es, qui
sont couverts par le m�me formalisme : l'**identification de param�tres** et la
**reconstruction de champs**. Avant d'introduire la `Description simple du cadre
m�thodologique de l'assimilation de donn�es`_ dans une prochaine section, nous
d�crivons bri�vement ces deux types d'applications. A la fin de ce chapitre,
quelques r�f�rences permettent d'`Approfondir le cadre m�thodologique de
l'assimilation de donn�es`_ et d'`Approfondir l'estimation d'�tat par des
m�thodes d'optimisation`_.

Reconstruction de champs ou interpolation de donn�es
----------------------------------------------------

.. index:: single: reconstruction de champs
.. index:: single: interpolation de donn�es
.. index:: single: interpolation de champs

La **reconstruction (ou l'interpolation) de champs** consiste � trouver, �
partir d'un nombre restreint de mesures r�elles, le champs physique qui est le
plus *coh�rent* avec ces mesures.

La *coh�rence* est � comprendre en termes d'interpolation, c'est-�-dire que le
champ que l'on cherche � reconstruire, en utilisant de l'assimilation de donn�es
sur les mesures, doit s'adapter au mieux aux mesures, tout en restant contraint
par la simulation globale du champ. Le champ calcul� est donc une estimation *a
priori* du champ que l'on cherche � identifier.

Si le syst�me �volue dans le temps, la reconstruction doit �tre �tablie � chaque
pas de temps, du champ dans son ensemble. Le processus d'interpolation est dans
ce cas plus compliqu� car il est temporel, et plus seulement en termes de
valeurs instantan�es du champ.

Un exemple simple de reconstruction de champs provient de la m�t�orologie, dans
laquelle on recherche les valeurs de variables comme la temp�rature ou la
pression en tout point du domaine spatial. On dispose de mesures instantan�es de
ces quantit�s en certains points, mais aussi d'un historique de ces mesures. De
plus, ces variables sont contraintes par les �quations d'�volution de
l'atmosph�re, qui indiquent par exemple que la pression en un point ne peut pas
prendre une valeur quelconque ind�pendamment de la valeur au m�me point � un
temps pr�c�dent. On doit donc faire la reconstruction d'un champ en tout point
de l'espace, de mani�re "coh�rente" avec les �quations d'�volution et avec les
mesures aux pr�c�dents pas de temps.

Identification de param�tres, ajustement de mod�les, calibration
----------------------------------------------------------------

.. index:: single: identification de param�tres
.. index:: single: ajustement de param�tres
.. index:: single: ajustement de mod�les
.. index:: single: calibration
.. index:: single: �bauche
.. index:: single: r�gularisation
.. index:: single: probl�mes inverses

L'**identification (ou l'ajustement) de param�tres** par assimilation de donn�es
est une forme de calibration d'�tat qui utilise simultan�ment les mesures
physiques et une estimation *a priori* des param�tres (appel�e l'"*�bauche*")
d'�tat que l'on cherche � identifier, ainsi qu'une caract�risation de leurs
erreurs. De ce point de vue, cette d�marche utilise toutes les informations
disponibles sur le syst�me physique, avec des hypoth�ses restrictives mais
r�alistes sur les erreurs, pour trouver l'"*estimation optimale*" de l'�tat
vrai. On peut noter, en termes d'optimisation, que l'�bauche r�alise la
"*r�gularisation*", au sens math�matique de Tikhonov [Tikhonov77]_
[WikipediaTI]_, du probl�me principal d'identification de param�tres. On peut
aussi d�signer cette d�marche comme une r�solution de type "*probl�me inverse*".

En pratique, les deux �carts (ou incr�ments) observ�s "*calculs-mesures*" et
"*calculs-�bauche*" sont combin�s pour construire la correction de calibration
des param�tres ou des conditions initiales. L'ajout de ces deux incr�ments
requiert une pond�ration relative, qui est choisie pour refl�ter la confiance
que l'on donne � chaque information utilis�e. Cette confiance est repr�sent�e
par la covariance des erreurs sur l'�bauche et sur les observations. Ainsi
l'aspect stochastique des informations, mesur� *a priori*, est essentiel pour
construire une fonction d'erreur pour la calibration.

Un exemple simple d'identification de param�tres provient de tout type de
simulation physique impliquant un mod�le param�tr�. Par exemple, une simulation
de m�canique statique d'une poutre contrainte par des forces est d�crite par les
param�tres de la poutre, comme un coefficient de Young, ou par l'intensit� des
forces appliqu�es. Le probl�me d'estimation de param�tres consiste � chercher
par exemple la bonne valeur du coefficient de Young de telle mani�re � ce que la
simulation de la poutre corresponde aux mesures, en y incluant la connaissance
des erreurs.

Description simple du cadre m�thodologique de l'assimilation de donn�es
-----------------------------------------------------------------------

.. index:: single: �bauche
.. index:: single: covariances d'erreurs d'�bauche
.. index:: single: covariances d'erreurs d'observation
.. index:: single: covariances
.. index:: single: 3DVAR
.. index:: single: Blue

On peut d�crire ces d�marches de mani�re simple. Par d�faut, toutes les
variables sont des vecteurs, puisqu'il y a plusieurs param�tres � ajuster, ou un
champ discretis� � reconstruire.

Selon les notations standards en assimilation de donn�es, on note
:math:`\mathbf{x}^a` les param�tres optimaux qui doivent �tre d�termin�s par
calibration, :math:`\mathbf{y}^o` les observations (ou les mesures
exp�rimentales) auxquelles on doit comparer les sorties de simulation,
:math:`\mathbf{x}^b` l'�bauche (valeurs *a priori*, ou valeurs de 
r�gularisation) des param�tres cherch�s, :math:`\mathbf{x}^t` les param�tres
inconnus id�aux qui donneraient exactement les observations (en supposant que
toutes les erreurs soient nulles et que le mod�le soit exact) en sortie.

Dans le cas le plus simple, qui est statique, les �tapes de simulation et
d'observation peuvent �tre combin�es en un unique op�rateur d'observation not�
:math:`H` (lin�aire ou non-lin�aire). Il transforme formellement les param�tres
:math:`\mathbf{x}` en entr�e en r�sultats :math:`\mathbf{y}`, qui peuvent �tre
directement compar�s aux observations :math:`\mathbf{y}^o` :

.. math:: \mathbf{y} = H(\mathbf{x})

De plus, on utilise l'op�rateur lin�aris� :math:`\mathbf{H}` pour repr�senter
l'effet de l'op�rateur complet :math:`H` autour d'un point de lin�arisation (et
on omettra ensuite de mentionner :math:`H` m�me si l'on peut le conserver). En
r�alit�, on a d�j� indiqu� que la nature stochastique des variables est
essentielle, provenant du fait que le mod�le, l'�bauche et les observations sont
tous incorrects. On introduit donc des erreurs d'observations additives, sous la
forme d'un vecteur al�atoire :math:`\mathbf{\epsilon}^o` tel que :

.. math:: \mathbf{y}^o = \mathbf{H} \mathbf{x}^t + \mathbf{\epsilon}^o

Les erreurs repr�sent�es ici ne sont pas uniquement celles des observations, ce
sont aussi celles de la simulation. On peut toujours consid�rer que ces erreurs
sont de moyenne nulle. En notant :math:`E[.]` l'esp�rance math�matique
classique, on peut alors d�finir une matrice :math:`\mathbf{R}` des covariances
d'erreurs d'observation par l'expression :

.. math:: \mathbf{R} = E[\mathbf{\epsilon}^o.{\mathbf{\epsilon}^o}^T]

L'�bauche peut aussi �tre �crite formellement comme une fonction de la valeur
vraie, en introduisant le vecteur d'erreurs :math:`\mathbf{\epsilon}^b` tel que
:

.. math:: \mathbf{x}^b = \mathbf{x}^t + \mathbf{\epsilon}^b

Les erreurs :math:`\mathbf{\epsilon}^b` sont aussi suppos�es de moyenne nulle,
de la m�me mani�re que pour les observations. On d�finit la matrice
:math:`\mathbf{B}` des covariances d'erreurs d'�bauche par :

.. math:: \mathbf{B} = E[\mathbf{\epsilon}^b.{\mathbf{\epsilon}^b}^T]

L'estimation optimale des param�tres vrais :math:`\mathbf{x}^t`, �tant donn�
l'�bauche :math:`\mathbf{x}^b` et les observations :math:`\mathbf{y}^o`, est
ainsi l'"*analyse*" :math:`\mathbf{x}^a` et provient de la minimisation d'une
fonction d'erreur, explicite en assimilation variationnelle, ou d'une correction
de filtrage en assimilation par filtrage.

En **assimilation variationnelle**, dans un cas statique, on cherche
classiquement � minimiser la fonction :math:`J` suivante :

.. math:: J(\mathbf{x})=\frac{1}{2}(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+\frac{1}{2}(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

:math:`J` est classiquement d�sign�e comme la fonctionnelle "*3D-VAR*" en
assimilation de donn�es (voir par exemple [Talagrand97]_) ou comme la
fonctionnelle de r�gularisation de Tikhonov g�n�ralis�e en optimisation (voir
par exemple [WikipediaTI]_). Comme les matrices de covariance :math:`\mathbf{B}`
et :math:`\mathbf{R}` sont proportionnelles aux variances d'erreurs, leur
pr�sence dans les deux termes de la fonctionnelle :math:`J` permet effectivement
de pond�rer les termes d'�carts par la confiance dans les erreurs d'�bauche ou
d'observations. Le vecteur :math:`\mathbf{x}` des param�tres r�alisant le
minimum de cette fonction constitue ainsi l'analyse :math:`\mathbf{x}^a`. C'est
� ce niveau que l'on doit utiliser toute la panoplie des m�thodes de
minimisation de fonctions connues par ailleurs en optimisation (voir aussi la
section `Approfondir l'estimation d'�tat par des m�thodes d'optimisation`_).
Selon la taille du vecteur :math:`\mathbf{x}` des param�tres � identifier, et la
disponibilit� du gradient ou de la hessienne de :math:`J`, il est judicieux
d'adapter la m�thode d'optimisation choisie (gradient, Newton, quasi-Newton...).

En **assimilation par filtrage**, dans ce cas simple usuellement d�nomm�
"*BLUE*" (pour "*Best Linear Unbiased Estimator*"), l'analyse
:math:`\mathbf{x}^a` est donn�e comme une correction de l'�bauche
:math:`\mathbf{x}^b` par un terme proportionnel � la diff�rence entre les
observations :math:`\mathbf{y}^o` et les calculs :math:`\mathbf{H}\mathbf{x}^b` :

.. math:: \mathbf{x}^a = \mathbf{x}^b + \mathbf{K}(\mathbf{y}^o - \mathbf{H}\mathbf{x}^b)

o� :math:`\mathbf{K}` est la matrice de gain de Kalman, qui s'exprime � l'aide
des matrices de covariance sous la forme suivante :

.. math:: \mathbf{K} = \mathbf{B}\mathbf{H}^T(\mathbf{H}\mathbf{B}\mathbf{H}^T+\mathbf{R})^{-1}

L'avantage du filtrage est le calcul explicite du gain, pour produire ensuite la
matrice *a posteriori* de covariance d'analyse.

Dans ce cas statique simple, on peut montrer, sous une hypoth�se de
distributions gaussiennes d'erreurs (tr�s peu restrictive en pratique), que les
deux approches *variationnelle* et *de filtrage* donnent la m�me solution.

On indique que ces m�thodes de "*3D-VAR*" et de "*BLUE*" peuvent �tre �tendues �
des probl�mes dynamiques, sous les noms respectifs de "*4D-VAR*" et de "*filtre
de Kalman*". Elles peuvent prendre en compte l'op�rateur d'�volution pour
�tablir aux bons pas de temps une analyse de l'�cart entre les observations et
les simulations et pour avoir, � chaque instant, la propagation de l'�bauche �
travers le mod�le d'�volution. Un grand nombre de variantes ont �t� d�velopp�es
pour accro�tre la qualit� num�rique des m�thodes ou pour prendre en compte des
contraintes informatiques comme la taille ou la dur�e des calculs.

Approfondir le cadre m�thodologique de l'assimilation de donn�es
----------------------------------------------------------------

.. index:: single: estimation d'�tat
.. index:: single: estimation de param�tres
.. index:: single: probl�mes inverses
.. index:: single: estimation bay�sienne
.. index:: single: interpolation optimale
.. index:: single: r�gularisation math�matique
.. index:: single: m�thodes de r�gularisation
.. index:: single: m�thodes de lissage

Pour obtenir de plus amples informations sur les techniques d'assimilation de
donn�es, le lecteur peut consulter les documents introductifs comme
[Talagrand97]_ ou [Argaud09]_, des supports de formations ou de cours comme
[Bouttier99]_ et [Bocquet04]_ (ainsi que d'autres documents issus des
applications des g�osciences), ou des documents g�n�raux comme [Talagrand97]_,
[Tarantola87]_, [Kalnay03]_, [Ide97]_, [Tikhonov77]_ et [WikipediaDA]_.

On note que l'assimilation de donn�es n'est pas limit�e � la m�t�orologie ou aux
g�o-sciences, mais est largement utilis�e dans d'autres domaines scientifiques.
Il y a de nombreux champs d'applications scientifiques et technologiques dans
lesquels l'utilisation efficace des donn�es observ�es, mais incompl�tes, est
cruciale.

Certains aspects de l'assimilation de donn�es sont aussi connus sous les noms
d'*estimation d'�tat*, d'*estimation de param�tres*, de *probl�mes inverses*,
d'*estimation bay�sienne*, d'*interpolation optimale*, de *r�gularisation
math�matique*, de *lissage de donn�es*, etc. Ces termes peuvent �tre utilis�s
dans les recherches bibliographiques.

Approfondir l'estimation d'�tat par des m�thodes d'optimisation
---------------------------------------------------------------

.. index:: single: estimation d'�tat
.. index:: single: m�thodes d'optimisation

Comme vu pr�c�demment, dans un cas de simulation statique, l'assimilation
variationnelle de donn�es n�cessite de minimiser la fonction objectif :math:`J`:

.. math:: J(\mathbf{x})=(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

qui est d�nomm�e la fonctionnelle du "*3D-VAR*". Elle peut �tre vue comme la
forme �tendue d'une *minimisation moindres carr�s*, obtenue en ajoutant un terme
de r�gularisation utilisant :math:`\mathbf{x}-\mathbf{x}^b`, et en pond�rant les
diff�rences par les deux matrices de covariances :math:`\mathbf{B}` et
:math:`\mathbf{R}`. La minimisation de la fonctionnelle :math:`J` conduit � la
*meilleure* estimation de l'�tat :math:`\mathbf{x}`. Pour obtenir plus
d'informations sur ces notions, on se reportera aux ouvrages g�n�raux de
r�f�rence comme [Tarantola87]_.

Les possibilit�s d'extension de cette estimation d'�tat, en utilisant de mani�re
plus explicite des m�thodes d'optimisation et leurs propri�t�s, peuvent �tre
imagin�es de deux mani�res.

En premier lieu, les m�thodes classiques d'optimisation impliquent l'usage de
m�thodes de minimisation vari�es bas�es sur un gradient. Elles sont extr�mement
efficaces pour rechercher un minimum local isol�. Mais elles n�cessitent que la
fonctionnelle :math:`J` soit suffisamment r�guli�re et diff�rentiable, et elles
ne sont pas en mesure de saisir des propri�t�s globales du probl�me de
minimisation, comme par exemple : minimum global, ensemble de solutions
�quivalentes dues � une sur-param�trisation, multiples minima locaux, etc. **Une
m�thode pour �tendre les possibilit�s d'estimation consiste donc � utiliser
l'ensemble des m�thodes d'optimisation existantes, permettant la minimisation
globale, diverses propri�t�s de robustesse de la recherche, etc**. Il existe de
nombreuses m�thodes de minimisation, comme les m�thodes stochastiques,
�volutionnaires, les heuristiques et m�ta-heuristiques pour les probl�mes �
valeurs r�elles, etc. Elles peuvent traiter des fonctionnelles :math:`J` en
partie irr�guli�res ou bruit�es, peuvent caract�riser des minima locaux, etc. Le
principal d�savantage de ces m�thodes est un co�t num�rique souvent bien
sup�rieur pour trouver les estimations d'�tats, et pas de garantie de
convergence en temps fini. Ici, on ne mentionne que des m�thodes qui sont
disponibles dans le module ADAO : la *r�gression de quantile (Quantile
Regression)* [WikipediaQR]_ et l'*optimisation par essaim de particules
(Particle Swarm Optimization)* [WikipediaPSO]_.

En second lieu, les m�thodes d'optimisation cherchent usuellement � minimiser
des mesures quadratiques d'erreurs, car les propri�t�s naturelles de ces
fonctions objectifs sont bien adapt�es � l'optimisation classique par gradient.
Mais d'autres mesures d'erreurs peuvent �tre mieux adapt�es aux probl�mes de
simulation de la physique r�elle. Ainsi, **une autre mani�re d'�tendre les
possibilit�s d'estimation consiste � utiliser d'autres mesures d'erreurs �
r�duire**. Par exemple, on peut citer l'**erreur absolue**, l'**erreur
maximale**, etc. Ces mesures d'erreurs ne sont pas diff�rentiables, mais
certaines m�thodes d'optimisation peuvent les traiter: heuristiques et
m�ta-heuristiques pour les probl�mes � valeurs r�elles, etc. Comme pr�c�demment,
le principal d�savantage de ces m�thodes est un co�t num�rique souvent bien
sup�rieur pour trouver les estimations d'�tats, et pas de garantie de
convergence en temps fini. Ici encore, on ne mentionne que des m�thodes qui sont
disponibles dans le module ADAO : l'*optimisation par essaim de particules
(Particle Swarm Optimization)* [WikipediaPSO]_.

Le lecteur int�ress� par le sujet de l'optimisation pourra utilement commencer
sa recherche gr�ce au point d'entr�e [WikipediaMO]_.
