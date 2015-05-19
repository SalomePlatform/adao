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

.. _section_ref_output_variables:

Variables et informations disponibles en sortie
-----------------------------------------------

Comment obtenir les informations disponibles en sortie
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: UserPostAnalysis
.. index:: single: algoResults
.. index:: single: getResults
.. index:: single: get
.. index:: single: ADD

En sortie, apr�s ex�cution d'une assimilation de donn�es, d'une optimisation
ou d'une v�rification, on dispose de variables et d'informations issues du
calcul. L'obtention de ces informations se fait ensuite de mani�re standardis�e
� l'aide de l'�tape de post-processing du calcul.

L'�tape est ais�ment identifi�e par l'utilisateur dans son cas ADAO de
d�finition (par le mot-cl� "*UserPostAnalysis*") ou dans son sch�ma YACS
d'ex�cution (par des noeuds ou blocs situ�s apr�s le bloc de calcul, et reli�s
graphiquement au port de sortie "*algoResults*" du bloc de calcul):

#. Dans le cas o� l'utilisateur d�finit le post-processing dans son cas ADAO, il utilise un fichier script externe ou des commandes dans le champ de type "*String*" ou "*Template*". Le script qu'il fournit dispose d'une variable fixe "*ADD*" dans l'espace de noms.
#. Dans le cas o� l'utilisateur d�finit le post-processing dans son sch�ma YACS par un noeud Python situ� apr�s le bloc de calcul, il doit ajouter un port d'entr�e de type "*pyobj*" nomm� par exemple "*Study*", reli� graphiquement au port de sortie "*algoResults*" du bloc de calcul. Le noeud Python de post-processing doit ensuite d�buter par ``ADD = Study.getResults()``.

Des patrons (ou "templates") sont donn�s ci-apr�s en
:ref:`subsection_r_o_v_Template`.  Dans tous les cas, le post-processing de
l'utilisateur dispose dans l'espace de noms d'une variable dont le nom est
"*ADD*", et dont l'unique m�thode utilisable est nomm�e ``get``. Les arguments
de cette m�thode sont un nom d'information de sortie, comme d�crit dans
l':ref:`subsection_r_o_v_Inventaire`.

Par exemple, pour avoir l'�tat optimal apr�s un calcul d'assimilation de donn�es
ou d'optimisation, on utilise l'appel suivant::

    ADD.get("Analysis")

Cet appel renvoie une liste de valeurs de la notion demand�e (ou, dans le cas 
de variables d'entr�es qui ne sont par nature qu'en un unique exemplaire, la
valeur elle-m�me). On peut alors demander un �l�ment particulier de la liste par
les commandes standards de liste (en particulier ``[-1]`` pour le dernier, et
``[:]`` pour tous les �l�ments).

.. _subsection_r_o_v_Template:

Exemples de scripts Python pour obtenir ou traiter les sorties
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Template
.. index:: single: AnalysisPrinter
.. index:: single: AnalysisSaver
.. index:: single: AnalysisPrinterAndSaver

Ces exemples pr�sentent des commandes ou scripts Python qui permettent d'obtenir
ou de traiter les sorties d'une ex�cution d'algorithme. Pour aider
l'utilisateur, ils sont directement disponibles dans l'interface, � la
construction du cas ADAO dans l'�diteur int�gr� de cas, dans les champs de type
"*Template*". De mani�re �quivalente, ces commandes peuvent �tre contenues dans
un script utilisateur externe (et ins�r�es dans le cas ADAO par l'entr�e de type
"*Script*") ou contenues dans une cha�ne de caract�res, y compris les retour �
la ligne (et ins�r�es dans le cas ADAO par l'entr�e de type "*String*"). De
nombreuses variantes peuvent �tre imagin�es � partir de ces exemples simples,
l'objectif �tant surtout d'aider l'utilisateur � effectuer le traitement exact
dont il a besoin en sortie.

Le premier exemple (appel� "*AnalysisPrinter*" dans les entr�es de type
"*Template*") consiste � afficher, dans la sortie standard d'ex�cution, la
valeur de l'analyse ou de l'�tat optimal, not� :math:`\mathbf{x}^a` dans la
partie :ref:`section_theory`. Cela se r�alise par les commandes::

    import numpy
    xa=numpy.ravel(ADD.get('Analysis')[-1])
    print 'Analysis:',xa"

La fonction ``numpy.ravel`` assure simplement que la variable ``xa`` contienne
un vrai vecteur unidimensionnel, quels que soient les choix informatiques
pr�c�dents.

Un second exemple (appel� "*AnalysisSaver*" dans les entr�es de type
"*Template*") consiste � enregistrer sur fichier la valeur de l'analyse ou de
l'�tat optimal :math:`\mathbf{x}^a`. Cela se r�alise par les commandes::

    import numpy
    xa=numpy.ravel(ADD.get('Analysis')[-1])
    f='/tmp/analysis.txt'
    print 'Analysis saved in "%s"'%f
    numpy.savetxt(f,xa)"

Le fichier d'enregistrement choisi est un fichier texte ``/tmp/analysis.txt``.

Il est ais� de combiner ces deux exemples pour en construire un troisi�me
(appel� "*AnalysisPrinterAndSaver*" dans les entr�es de type "*Template*"). Il
consiste � simultan�ment afficher dans la sortie standard d'ex�cution et �
enregistrer sur fichier la valeur de :math:`\mathbf{x}^a`. Cela se r�alise par
les commandes::

    import numpy
    xa=numpy.ravel(ADD.get('Analysis')[-1])
    print 'Analysis:',xa
    f='/tmp/analysis.txt'
    print 'Analysis saved in "%s"'%f
    numpy.savetxt(f,xa)

Pour faciliter l'extension de ces exemples selon les besoins utilisateurs, on
rappelle que l'ensemble des fonctions de SALOME sont disponibles au m�me niveau
que ces commandes. L'utilisateur peut en particulier requ�rir des actions de
repr�sentation graphique avec le module PARAVIS [#]_ ou d'autres modules, des
actions de calcul pilot�s par YACS [#]_ ou un autre module, etc.

D'autres exemples d'utilisation sont aussi donn�s en :ref:`section_u_step4` de
la partie :ref:`section_using`, ou en partie :ref:`section_examples`.

Conditionnalit� des informations disponibles en sortie
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: Stored

La disponibilit� des informations apr�s le calcul est conditionn�e par le fait
qu'elles aient �t� calcul�es ou demand�es.

Chaque algorithme ne fournit pas obligatoirement les m�mes informations, et
n'utilise par exemple pas n�cessairement les m�mes quantit�s interm�diaires. Il
y a donc des informations toujours pr�sentes comme l'�tat optimal r�sultant du
calcul. Les autres informations ne sont pr�sentes que pour certains algorithmes
et/ou que si elles ont �t� r�clam�es avant l'ex�cution du calcul.

On rappelle que l'utilisateur peut r�clamer des informations suppl�mentaires
lors de l'�tablissement de son cas ADAO, en utilisant la commande optionnelle
"*AlgorithmParameters*" du cas ADAO. On se reportera � la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande, et � la description de chaque algorithme pour les informations
disponibles par algorithme. On peut aussi demander � conserver certaines
informations en entr�e en changeant le bool�en "*Stored*" qui lui est associ�
dans l'�dition du cas ADAO. 

.. _subsection_r_o_v_Inventaire:

Inventaire des informations potentiellement disponibles en sortie
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

L'ensemble des informations potentiellement disponibles en sortie est indiqu�
ici ind�pendamment des algorithmes, pour inventaire.

L'�tat optimal est une information qui est toujours naturellement disponible
apr�s un calcul d'assimilation de donn�es ou d'optimisation. Il d�sign� par le
mot-cl� suivant:

  Analysis
    *Liste de vecteurs*. Chaque �l�ment est un �tat optimal :math:`\mathbf{x}*`
    en optimisation ou une analyse :math:`\mathbf{x}^a` en assimilation de
    donn�es.

    Exemple : ``Xa = ADD.get("Analysis")[-1]``

Les variables suivantes sont des variables d'entr�e. Elles sont mises �
disposition de l'utilisateur en sortie pour faciliter l'�criture des proc�dures
de post-processing, et sont conditionn�es par une demande utilisateur � l'aide
d'un bool�en "*Stored*" en entr�e.

  Background
    *Vecteur*, dont la disponibilit� est conditionn�e par "*Stored*" en entr�e.
    C'est le vecteur d'�bauche :math:`\mathbf{x}^b`.

    Exemple : ``Xb = ADD.get("Background")``

  BackgroundError
    *Matrice*, dont la disponibilit� est conditionn�e par "*Stored*" en entr�e. 
    C'est la matrice :math:`\mathbf{B}` de covariances des erreurs *a priori*
    de l'�bauche.

    Exemple : ``B = ADD.get("BackgroundError")``

  EvolutionError
    *Matrice*, dont la disponibilit� est conditionn�e par "*Stored*" en entr�e. 
    C'est la matrice :math:`\mathbf{M}` de covariances des erreurs *a priori*
    de l'�volution.

    Exemple : ``M = ADD.get("EvolutionError")``

  Observation
    *Vecteur*, dont la disponibilit� est conditionn�e par "*Stored*" en entr�e. 
    C'est le vecteur d'observation :math:`\mathbf{y}^o`.

    Exemple : ``Yo = ADD.get("Observation")``

  ObservationError
    *Matrice*, dont la disponibilit� est conditionn�e par "*Stored*" en entr�e. 
    C'est la matrice :math:`\mathbf{R}` de covariances des erreurs *a priori*
    de l'observation.

    Exemple : ``R = ADD.get("ObservationError")``

Toutes les autres informations sont conditionn�es par l'algorithme et/ou par la
demande utilisateur de disponibilit�. Ce sont les suivantes, par ordre
alphab�tique:

  APosterioriCovariance
    *Liste de matrices*. Chaque �l�ment est une matrice :math:`\mathbf{A}*` de
    covariances des erreurs *a posteriori* de l'�tat optimal.

    Exemple : ``A = ADD.get("APosterioriCovariance")[-1]``

  BMA
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�cart entre
    l'�bauche et l'�tat optimal.

    Exemple : ``bma = ADD.get("BMA")[-1]``

  CostFunctionJ
    *Liste de valeurs*. Chaque �l�ment est une valeur de fonctionnelle d'�cart
    :math:`J`.

    Exemple : ``J = ADD.get("CostFunctionJ")[:]``

  CostFunctionJb
    *Liste de valeurs*. Chaque �l�ment est une valeur de fonctionnelle d'�cart
    :math:`J^b`, c'est-�-dire de la partie �cart � l'�bauche.

    Exemple : ``Jb = ADD.get("CostFunctionJb")[:]``

  CostFunctionJo
    *Liste de valeurs*. Chaque �l�ment est une valeur de fonctionnelle d'�cart
    :math:`J^o`, c'est-�-dire de la partie �cart � l'observation.

    Exemple : ``Jo = ADD.get("CostFunctionJo")[:]``

  CurrentState
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�tat courant utilis�
    au cours du d�roulement de l'algorithme d'optimisation.

    Exemple : ``Xs = ADD.get("CurrentState")[:]``

  Innovation
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'innovation, qui est
    en statique l'�cart de l'optimum � l'�bauche, et en dynamique l'incr�ment
    d'�volution.

    Exemple : ``d = ADD.get("Innovation")[-1]``

  MahalanobisConsistency
    *Liste de valeurs*. Chaque �l�ment est une valeur de l'indicateur de
    qualit� de Mahalanobis.

    Exemple : ``m = ADD.get("MahalanobisConsistency")[-1]``

  OMA
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�cart entre
    l'observation et l'�tat optimal dans l'espace des observations.

    Exemple : ``oma = ADD.get("OMA")[-1]``

  OMB
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�cart entre
    l'observation et l'�tat d'�bauche dans l'espace des observations.

    Exemple : ``omb = ADD.get("OMB")[-1]``

  SigmaBck2
    *Liste de valeurs*. Chaque �l�ment est une valeur de l'indicateur de
    qualit� :math:`(\sigma^b)^2` de la partie �bauche.

    Exemple : ``sb2 = ADD.get("SigmaBck")[-1]``

  SigmaObs2
    *Liste de valeurs*. Chaque �l�ment est une valeur de l'indicateur de
    qualit� :math:`(\sigma^o)^2` de la partie observation.

    Exemple : ``so2 = ADD.get("SigmaObs")[-1]``

  SimulatedObservationAtBackground
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'observation simul� �
    partir de l'�bauche :math:`\mathbf{x}^b`.

    Exemple : ``hxb = ADD.get("SimulatedObservationAtBackground")[-1]``

  SimulatedObservationAtCurrentState
    *Liste de vecteurs*. Chaque �l�ment est un vecteur observ� � l'�tat courant,
    c'est-�-dire dans l'espace des observations.

    Exemple : ``Ys = ADD.get("SimulatedObservationAtCurrentState")[-1]``

  SimulatedObservationAtOptimum
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'observation simul� �
    partir de l'analyse ou de l'�tat optimal :math:`\mathbf{x}^a`.

    Exemple : ``hxa = ADD.get("SimulatedObservationAtOptimum")[-1]``

  SimulationQuantiles
    *Liste de vecteurs*. Chaque �l�ment est un vecteur correspondant � l'�tat
    observ� qui r�alise le quantile demand�, dans le m�me ordre que les
    quantiles requis par l'utilisateur.

    Exemple : ``sQuantiles = ADD.get("SimulationQuantiles")[:]``

.. [#] Pour de plus amples informations sur PARAVIS, voir le *module PARAVIS* et son aide int�gr�e disponible dans le menu principal *Aide* de l'environnement SALOME.

.. [#] Pour de plus amples informations sur YACS, voir le *module YACS* et son aide int�gr�e disponible dans le menu principal *Aide* de l'environnement SALOME.
