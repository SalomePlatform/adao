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

.. index:: single: TUI
.. index:: single: API/TUI
.. _section_tui:

================================================================================
**[DocR]** Interface de programmation textuelle pour l'utilisateur (API/TUI)
================================================================================

.. warning::

  dans sa pr�sente version, cette interface de programmation textuelle (TUI) est
  exp�rimentale, et reste donc susceptible de changements dans les prochaines
  versions.

Cette section pr�sente des m�thodes avanc�es d'usage du module ADAO � l'aide de
son interface de programmation textuelle (API/TUI). Cette interface permet de
cr�er un objet de calcul de mani�re similaire � la construction d'un cas par
l'interface graphique (GUI). Dans le cas o� l'on d�sire r�aliser � la main le
cas de calcul TUI, on recommande de bien s'appuyer sur l'ensemble de la
documentation du module ADAO, et de se reporter si n�cessaire � l'interface
graphique (GUI), pour disposer de l'ensemble des �l�ments permettant de
renseigner correctement les commandes.

.. _subsection_tui_creating:

Cr�ation de cas de calcul TUI ADAO et exemples
----------------------------------------------

.. _subsection_tui_example:

Un exemple simple de cr�ation d'un cas de calcul TUI ADAO
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour introduire l'interface TUI, on commence par un exemple simple mais complet
de cas de calcul ADAO. Toutes les donn�es sont explicitement d�finies dans le
corps du script pour faciliter la lecture. L'ensemble des commandes est le
suivant::

    from numpy import *
    import adaoBuilder
    case = adaoBuilder.New()
    case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
    case.set( 'Background',          Vector=[0, 1, 2] )
    case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
    case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
    case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
    case.set( 'ObservationOperator', Matrix='1 0 0;0 2 0;0 0 3' )
    case.set( 'Observer',            Variable="Analysis", Template="ValuePrinter" )
    case.execute()

Le r�sultat de l'ex�cution de ces commandes dans SALOME (dans le shell SALOME,
dans la console Python de l'interface, ou par le menu d'ex�cution d'un script)
est le suivant::

    Analysis [ 0.25000264  0.79999797  0.94999939]

Cr�ation d�taill�e d'un cas de calcul TUI ADAO
++++++++++++++++++++++++++++++++++++++++++++++

On d�crit ici plus en d�tail les diff�rentes �tapes de cr�ation d'un cas de
calcul TUI ADAO. Les commandes elles-m�mes sont d�taill�es juste apr�s dans
l':ref:`subsection_tui_commands`.

L'initialisation et la cr�ation d'une �tude se fait par les commandes suivantes,
le nom ``case`` de l'objet du cas de calcul TUI ADAO �tant quelconque, au choix
de l'utilisateur::

    from numpy import *
    import adaoBuilder
    case = adaoBuilder.New()

Il est recommand� d'importer par principe le module ``numpy``, sous cette forme
particuli�re ``from ... import *``, pour faciliter ensuite son usage dans les
commandes elle-m�mes.

Ensuite, le cas doit �tre construit par une pr�paration et un enregistrement des
donn�es d�finissant l'�tude. L'ordre de ces commande n'a pas d'importance, il
suffit que les concepts requis par l'algorithme utilis� soient pr�sentes. On se
reportera � :ref:`section_reference` et � ses sous-parties pour avoir le d�tail
des commandes par algorithme. Ici, on d�finit successivement l'algorithme
d'assimilation de donn�es ou d'optimisation choisi et ses param�tres, puis
l'�bauche :math:`\mathbf{x}^b` et sa covariance d'erreurs :math:`\mathbf{B}`, et
enfin l'observation :math:`\mathbf{y}^o` et sa covariance d'erreurs
:math:`\mathbf{R}`::

    case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
    #
    case.set( 'Background',          Vector=[0, 1, 2] )
    case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
    #
    case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
    case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )

On remarque que l'on peut donner en entr�e des quantit�s vectorielles des objets
de type ``list``, ``tuple``, ``array`` ou ``matrix`` de Numpy.

On doit ensuite d�finir les op�rateurs :math:`H` d'observation et �ventuellement
:math:`M` d'�volution. Dans tous les cas, lin�aire ou non-lin�aire, on peut les
d�finir comme des fonctions. Dans le cas simple d'un op�rateur lin�aire, on peut
aussi le d�finir � l'aide de la matrice qui correspond � l'op�rateur lin�aire.
Dans le cas pr�sent le plus simple d'op�rateur lin�aire, on utilise la syntaxe
suivante pour un op�rateur de :math:`\mathbf{R}^3` sur lui-m�me::

    case.ObservationOperator(Matrix = "1 0 0;0 2 0;0 0 3")

Dans le cas beaucoup plus courant d'un op�rateur non-lin�aire, il doit �tre
pr�alablement disponible sous la forme d'une fonction Python connue dans
l'espace de nommage courant. L'exemple suivant montre une fonction
``simulation`` (qui r�alise ici le m�me op�rateur lin�aire que ci-dessus) et
l'enregistre dans le cas ADAO::

    def simulation(x):
        import numpy
        __x = numpy.matrix(numpy.ravel(numpy.matrix(x))).T
        __H = numpy.matrix("1 0 0;0 2 0;0 0 3")
        return __H * __x
    #
    case.set( 'ObservationOperator',
        OneFunction = simulation,
        Parameters  = {"DifferentialIncrement":0.01},
        )

Pour conna�tre les r�sultats interm�diaire ou finaux du calcul du cas, on peut
ajouter des observers, qui permettent d'associer l'ex�cution d'un script � une
variable interne ou finale du calcul. On se reportera � la description de la
mani�re d':ref:`section_advanced_observer`, et � la :ref:`section_reference`
pour savoir quelles sont les quantit�s observables. Cette association
d'observers avec une quantit� existante se fait de mani�re similaire � la
d�finition des donn�es du calcul::

    case.set( 'Observer', Variable="Analysis", Template="ValuePrinter" )

Enfin, lorsque toutes les informations requises sont disponibles dans le cas
``case`` de calcul ADAO, on peut en demander l'ex�cution de mani�re tr�s
simple dans l'environnement de l'interpr�teur Python::

    case.execute()

Au final, on obtient le script tr�s compact propos� pr�c�demment dans
:ref:`subsection_tui_example`.

Fournir des donn�es de calcul plus complexes
++++++++++++++++++++++++++++++++++++++++++++

Une telle interface s'�crivant en Python, il est possible d'utiliser toute la
puissance du langage pour entrer des donn�es plus complexes qu'une d�claration
explicite.

L'enregistrement des donn�es d'entr�es supporte diff�rents types de variables,
mais surtout, ces entr�es peuvent recevoir des variables courantes disponibles
dans l'espace de nommage du script. Il est donc ais� d'utiliser des variables
calcul�es pr�alablement ou obtenues par l'import de scripts "utilisateur". Si
par exemple les observations sont disponibles sous la forme d'une liste dans un
fichier Python externe nomm� ``observations.py`` sous le nom ``table``, il
suffit de r�aliser les op�rations suivantes pour enregistrer les observations
dans le cas de calcul TUI ADAO::

    from observations import table
    case.set( 'Observation', Vector=table )

La premi�re ligne importe la variable ``table`` depuis le fichier externe, et la
seconde enregistre directement cette table comme la donn�e "*Observation*".

La simplicit� de cet enregistrement montre bien la facilit� d'obtenir les
donn�es de calcul depuis des sources externes, fichiers ou flux informatiques
atteignables en Python. Comme d'habitude, il est recommand� � l'utilisateur de
v�rifier ses donn�es avant de les enregistrer dans le cas de calcul TUI ADAO
pour �viter les erreurs compliqu�es � corriger.

Obtenir et utiliser les r�sultats de calcul de mani�re plus riche
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

De la m�me mani�re, il est possible d'obtenir et traiter les r�sultats de calcul
de mani�re plus riche, pour encha�ner sur des post-traitements apr�s le calcul
en TUI.

Les variables de r�sultats de calcul, ou les variables internes issues de
l'optimisation sont disponible � travers la m�thode ``get`` du cas de calcul TUI
ADAO, qui renvoie un objet de type liste de la variable demand�e. On se
reportera aux :ref:`section_ref_output_variables` pour une description d�taill�e
sur ce sujet.

A titre d'exemple, on donne quelques lignes de script qui permettent d'obtenir
le nombre d'it�rations de l'optimisation et la valeur optimale ainsi que sa
taille::

    print
    print "    Nombre d'iterations :",len(case.get("CostFunctionJ"))
    Xa = case.get("Analysis")
    print "    Analyse optimale  :",Xa[-1]
    print "    Taille de l'analyse :",len(Xa[-1])
    print

Ces lignes peuvent �tre tr�s simplement additionn�es � l'exemple initial de cas
de calcul TUI ADAO propos� dans :ref:`subsection_tui_example`.

De m�me que pour l'entr�e des donn�es, la simplicit� de r�cup�ration des
r�sultats permet d'envisager ais�ment des post-traitements encha�n�s, pour
utiliser par exemple de la visualisation avec MatPlotLib ou PARAVIS [PARAVIS]_,
de l'adaptation de maillage avec HOMARD [HOMARD]_, ou pour d'autres calculs.

.. _subsection_tui_commands:

Ensemble des commandes disponibles en interface textuelle TUI
-------------------------------------------------------------

Dans l'interface TUI du module ADAO, on suit les conventions et recommandations
courantes en Python pour la distinction entre ce qui est public, et ce qui est
priv� ou r�serv� car relevant des d�tails d'impl�mentation. De mani�re pratique,
tout nom d'objet ou de fonction commen�ant par au moins un signe "_" est priv�
au sens courant de programmation ("*private*"). N�anmoins, l'absence d'un tel
signe au d�but d'un nom ne le d�signe pas comme public. De mani�re g�n�rale, en
Python, et contrairement � d'autres langages, on peut acc�der aux objets ou aux
fonction priv�s. Cela peut parfois �tre utile, mais un tel usage dans vos codes
conduira � des plantages sans avertissement lors de futures versions. Il est
donc fortement recommand� de ne pas le faire.

Pour clarifier et faciliter l'utilisation du module pour du script, **cette
section d�finit donc l'interface de programmation (API) textuelle publique pour
l'utilisateur (TUI) de mani�re compl�te et limitative**. L'usage en script
d'objets ou fonctions ADAO autres que ceux qui sont d�finis ici est fortement
d�conseill�, car cela conduira vraisemblablement � des plantages sans
avertissement lors de futures versions.

Syntaxes d'appel �quivalentes pour les commandes TUI
++++++++++++++++++++++++++++++++++++++++++++++++++++

La d�finition des donn�es lors de la cr�ation de cas de calcul TUI ADAO supporte
**deux syntaxes enti�rement �quivalentes**. On peut :

- soit utiliser la commande ``set`` et comme premier argument le concept
  ``XXXXX`` sur laquelle appliquer la commande dont les arguments suivent,
- soit utiliser la commande ``setXXXXX`` contenant les arguments de la commande
  � appliquer.

Pour illustrer cette �quivalence, on prend l'exemple des deux commandes
suivantes qui conduisent au m�me r�sultat::

    case.set( 'Background', Vector=[0, 1, 2] )

et::

    case.setBackground( Vector=[0, 1, 2] )

Le choix de l'une ou l'autre des syntaxes est librement laiss� � l'utilisateur,
selon son contexte d'usage. Dans la suite, par souci de clart�, on d�finit les
commandes selon la seconde syntaxe.

D�finir les donn�es de calcul
+++++++++++++++++++++++++++++

Les commandes qui suivent permettent de d�finir les donn�es d'un cas de calcul
TUI ADAO. Le pseudo-type des arguments est similaire et compatible avec ceux des
entr�es en interface GUI, d�crits dans la section des
:ref:`section_reference_entry` et en particulier par la
:ref:`section_ref_entry_types`. La v�rification de l'ad�quation des grandeurs se
fait soit lors de leur d�finition, soit lors de l'ex�cution.

Dans chaque commande, le mot-cl� bool�en "*Stored*" permet d'indiquer si l'on
veut �ventuellement la stocker la grandeur d�finie pour en disposer en en cours
de calcul ou en sortie. Le choix par d�faut est de ne pas stocker, et il est
recommand� de conserver cette valeur par d�faut. En effet, pour un cas de calcul
TUI, on dispose d�j� souvent des grandeurs donn�es en entr�es qui sont pr�sentes
dans l'espace de nommage courant du cas.

Les commandes disponibles sont les suivantes :

.. index:: single: setBackground

**setBackground** (*Vector, VectorSerie, Script, Stored*)
    Cette commande permet de d�finir l'�bauche :math:`\mathbf{x}^b`. Selon les
    algorithmes, on peut le d�finir comme un vecteur simple par "*Vector*", ou
    comme une liste de vecteurs par "*VectorSerie*". Si on le d�finit par un
    script dans "*Script*", le vecteur est de type "*Vector*" (par d�faut) ou
    "*VectorSerie*" selon que l'une de ces variables est plac�e � "*True*".

.. index:: single: setBackgroundError

**setBackgroundError** (*Matrix, ScalarSparseMatrix, DiagonalSparseMatrix, Script, Stored*)
    Cette commande permet de d�finir la matrice :math:`\mathbf{B}` des
    covariance des erreurs d'�bauche. La matrice peut �tre d�finie de mani�re
    compl�te par "*Matrix*", ou de mani�re parcimonieuse comme une matrice
    diagonale dont on donne la variance unique sur la diagonale par
    "*ScalarSparseMatrix*", ou comme une matrice diagonale dont on donne le
    vecteur des variances situ� sur la diagonale par "*DiagonalSparseMatrix*".
    Si on la d�finit par un script dans "*Script*", la matrice est de type
    "*Matrix*" (par d�faut), "*ScalarSparseMatrix*" ou "*DiagonalSparseMatrix*"
    selon que l'une de ces variables est plac�e � "*True*".

.. index:: single: setCheckingPoint

**setCheckingPoint** (*Vector, VectorSerie, Script, Stored*)
    Cette commande permet de d�finir un point courant :math:`\mathbf{x}` utilis�
    pour un algorithme de v�rification. Selon les algorithmes, on peut le
    d�finir comme un vecteur simple par "*Vector*", ou comme une liste de
    vecteurs par "*VectorSerie*". Si on le d�finit par un script dans
    "*Script*", le vecteur est de type "*Vector*" (par d�faut) ou
    "*VectorSerie*" selon que l'une de ces variables est plac�e � "*True*".

.. index:: single: setControlModel

**setControlModel** (*Matrix, OneFunction, ThreeFunctions, Parameters, Script, Stored*)
    Cette commande permet de d�finir l'op�rateur de contr�le :math:`O`, qui
    d�crit un contr�le d'entr�e lin�aire externe de l'op�rateur d'�volution ou
    d'observation. On se reportera :ref:`section_ref_operator_control`. Sa
    valeur est d�finie comme un objet de type fonction ou de type "*Matrix*".
    Dans le cas d'une fonction, diff�rentes formes fonctionnelles peuvent �tre
    utilis�es, comme d�crit dans la section
    :ref:`section_ref_operator_requirements`, et entr�es par "*OneFunction*" ou
    "*ThreeFunctions*". Dans le cas d'une d�finition par "*Script*", l'op�rateur
    est de type "*Matrix*", "*OneFunction*" ou "*ThreeFunctions*" selon que
    l'une de ces variables est plac�e � "*True*". Les param�tres de contr�le de
    l'approximation num�rique de l'op�rateur adjoint, dans le cas
    "*OneFunction*", peuvent �tre renseign�s par un dictionnaire dans
    "*Parameters*". Les entr�es potentielles de ce dictionnaire de param�tres
    sont "*DifferentialIncrement*", "*CenteredFiniteDifference*" (similaires �
    celles de l'interface graphique).

.. index:: single: setControlInput

**setControlInput** (*Vector, VectorSerie, Script, Stored*)
    Cette commande permet de d�finir le vecteur de contr�le :math:`\mathbf{u}`.
    Selon les algorithmes, on peut le d�finir comme un vecteur simple par
    "*Vector*", ou comme une liste de vecteurs par "*VectorSerie*". Si on le
    d�finit par un script dans "*Script*", le vecteur est de type "*Vector*"
    (par d�faut) ou "*VectorSerie*" selon que l'une de ces variables est plac�e
    � "*True*".

.. index:: single: setEvolutionError

**setEvolutionError** (*Matrix, ScalarSparseMatrix, DiagonalSparseMatrix, Script, Stored*)
    Cette commande permet de d�finir la matrice :math:`\mathbf{Q}` des
    covariance des erreurs d'�volution. La matrice peut �tre d�finie de mani�re
    compl�te par "*Matrix*", ou de mani�re parcimonieuse comme une matrice
    diagonale dont on donne la variance unique sur la diagonale par
    "*ScalarSparseMatrix*", ou comme une matrice diagonale dont on donne le
    vecteur des variances situ� sur la diagonale par "*DiagonalSparseMatrix*".
    Si on la d�finit par un script dans "*Script*", la matrice est de type
    "*Matrix*" (par d�faut), "*ScalarSparseMatrix*" ou "*DiagonalSparseMatrix*"
    selon que l'une de ces variables est plac�e � "*True*".

.. index:: single: setEvolutionModel

**setEvolutionModel** (*Matrix, OneFunction, ThreeFunctions, Parameters, Script, Stored*)
    Cette commande permet de d�finir l'op�rateur d'evolution :math:`M`, qui
    d�crit un pas �l�mentaire d'�volution. Sa valeur est d�finie comme un objet
    de type fonction ou de type "*Matrix*". Dans le cas d'une fonction,
    diff�rentes formes fonctionnelles peuvent �tre utilis�es, comme d�crit dans
    la section :ref:`section_ref_operator_requirements`, et entr�es par
    "*OneFunction*" ou "*ThreeFunctions*". Dans le cas d'une d�finition par
    "*Script*", l'op�rateur est de type "*Matrix*", "*OneFunction*" ou
    "*ThreeFunctions*" selon que l'une de ces variables est plac�e � "*True*".
    Les param�tres de contr�le de l'approximation num�rique de l'op�rateur
    adjoint, dans le cas "*OneFunction*", peuvent �tre renseign�s par un
    dictionnaire dans "*Parameters*". Les entr�es potentielles de ce
    dictionnaire de param�tres sont "*DifferentialIncrement*",
    "*CenteredFiniteDifference*", "*EnableMultiProcessing*",
    "*NumberOfProcesses*" (similaires � celles de l'interface graphique).

.. index:: single: setObservation

**setObservation** (*Vector, VectorSerie, Script, Stored*)
    Cette commande permet de d�finir le vecteur d'observation
    :math:`\mathbf{y}^o`. Selon les algorithmes, on peut le d�finir comme un
    vecteur simple par "*Vector*", ou comme une liste de vecteurs par
    "*VectorSerie*". Si on le d�finit par un script dans "*Script*", le vecteur
    est de type "*Vector*" (par d�faut) ou "*VectorSerie*" selon que l'une de
    ces variables est plac�e � "*True*".

.. index:: single: setObservationError

**setObservationError** (*Matrix, ScalarSparseMatrix, DiagonalSparseMatrix, Script, Stored*)
    Cette commande permet de d�finir la matrice :math:`\mathbf{R}` des
    covariance des erreurs d'observation. La matrice peut �tre d�finie de
    mani�re compl�te par "*Matrix*", ou de mani�re parcimonieuse comme une
    matrice diagonale dont on donne la variance unique sur la diagonale par
    "*ScalarSparseMatrix*", ou comme une matrice diagonale dont on donne le
    vecteur des variances situ� sur la diagonale par "*DiagonalSparseMatrix*".
    Si on la d�finit par un script dans "*Script*", la matrice est de type
    "*Matrix*" (par d�faut), "*ScalarSparseMatrix*" ou "*DiagonalSparseMatrix*"
    selon que l'une de ces variables est plac�e � "*True*".

.. index:: single: setObservationOperator

**setObservationOperator** (*Matrix, OneFunction, ThreeFunctions, Parameters, Script, Stored*)
    Cette commande permet de d�finir l'op�rateur d'observation :math:`H`, qui
    transforme les param�tres d'entr�e :math:`\mathbf{x}` en r�sultats
    :math:`\mathbf{y}` qui sont � comparer aux observations
    :math:`\mathbf{y}^o`. Sa valeur est d�finie comme un objet de type fonction
    ou de type "*Matrix*". Dans le cas d'une fonction, diff�rentes formes
    fonctionnelles peuvent �tre utilis�es, comme d�crit dans la section
    :ref:`section_ref_operator_requirements`, et entr�es par "*OneFunction*" ou
    "*ThreeFunctions*". Dans le cas d'une d�finition par "*Script*", l'op�rateur
    est de type "*Matrix*", "*OneFunction*" ou "*ThreeFunctions*" selon que
    l'une de ces variables est plac�e � "*True*". Les param�tres de contr�le de
    l'approximation num�rique de l'op�rateur adjoint, dans le cas
    "*OneFunction*", peuvent �tre renseign�s par un dictionnaire dans
    "*Parameters*". Les entr�es potentielles de ce dictionnaire de param�tres
    sont "*DifferentialIncrement*", "*CenteredFiniteDifference*",
    "*EnableMultiProcessing*", "*NumberOfProcesses*" (similaires � celles de
    l'interface graphique).

.. index:: single: set

**set** (*Concept,...*)
    Cette commande permet de disposer d'une syntaxe �quivalente pour toutes les
    commandes de ce paragraphe. Son premier argument est le nom du concept �
    d�finir (par exemple "*Background*" ou "*ObservationOperator*"), sur lequel
    s'applique ensuite les arguments qui suivent, qui sont les m�mes que dans
    les commandes individuelles pr�c�dentes. Lors de l'usage de cette commande,
    il est indispensable de nommer les arguments (par exemple "*Vector=...*").

Param�trer le calcul, les sorties, etc.
+++++++++++++++++++++++++++++++++++++++

.. index:: single: setAlgorithmParameters

**setAlgorithmParameters** (*Algorithm, Parameters*)
    Cette commande permet de choisir l'algorithme de calcul ou de v�rification
    par l'argument "*Algorithm*" sous la forme d'un nom d'algorithme (on se
    reportera utilement aux listes des :ref:`section_reference_assimilation` et
    des :ref:`section_reference_checking`), et de d�finir les param�tres de
    calcul par l'argument "*Parameters*".

.. index:: single: setDebug

**setDebug** ()
    Cette commande permet d'activer le mode d'information d�taill� lors de
    l'ex�cution.

.. index:: single: setNoDebug

**setNoDebug** ()
    Cette commande permet de d�sactiver le mode d'information d�taill� lors de
    l'ex�cution.

.. index:: single: setObserver

**setObserver** (*Variable, Template, String, Info*)
    Cette commande permet de d�finir un observer sur une variable courante ou
    finale du calcul.  On se reportera � la description de la mani�re
    d':ref:`section_advanced_observer`, et � la :ref:`section_reference` pour
    savoir quelles sont les quantit�s observables. On d�finit par "*String*" le
    corps de l'observer par une chaine de caract�res incluant si n�cessaire des
    sauts de lignes. On recommande d'utiliser les patrons disponibles par
    l'argument "*Template*". On dispose des patrons simples suivants :
    "*ValuePrinter*", "*ValueSeriePrinter*", "*ValueSaver*",
    "*ValueSerieSaver*", "*ValuePrinterAndSaver*",
    "*ValueSeriePrinterAndSaver*", "*ValueGnuPlotter*",
    "*ValueSerieGnuPlotter*".

Effectuer le calcul 
+++++++++++++++++++

.. index:: single: executePythonScheme

**executePythonScheme** ()
    Cette commande lance le calcul complet dans l'environnement de
    l'interpr�teur Python courant, sans interaction avec YACS. Les sorties
    standard et d'erreur sont celles de l'interpr�teur Python. On dispose si
    n�cessaire du parall�lisme interne des algorithmes dans ADAO et du
    parall�lisme interne du ou des codes de simulation utilis�.

.. index:: single: generateYACSscheme

**executeYACSScheme** (*File*)
    Cete commande g�n�re le sch�ma YACS [YACS]_ du cas de calcul dans le fichier
    requis "*File*", et en lance l'ex�cution dans l'interpr�teur YACS, comme on
    peut le r�aliser en utilisant l'�diteur standard de cas ADAO. Les sorties
    standard et d'erreur sont celles de l'interpr�teur YACS. On dispose si
    n�cessaire du parall�lisme de noeuds et blocs dans YACS, du parall�lisme
    interne des algorithmes dans ADAO et du parall�lisme interne du ou des codes
    de simulation utilis�.

.. index:: single: execute

**execute** ()
    Cette commande est un raccourci utilisateur pour "*executePythonScheme*".

Obtenir s�par�ment les r�sultats de calcul
++++++++++++++++++++++++++++++++++++++++++

.. index:: single: get

**get** (*Concept*)
    Cette commande permet d'extraire explicitement les variables disponibles en
    sortie du cas de calcul TUI ADAO pour les utiliser dans la suite du
    scripting, par exemple en visualisation. Elle a pour argument le nom d'un
    variable dans "*Concept*", et renvoie en retour la grandeur sous la forme
    d'une liste (m�me s'il n'y en a qu'un exemplaire) de cette variable de
    base. Pour conna�tre la liste des variables et les utiliser, on se
    reportera � l':ref:`subsection_r_o_v_Inventaire`, et plus g�n�ralement � la
    fois aux :ref:`section_ref_output_variables` et aux documentations
    individuelles des algorithmes.

Exemples plus avanc�s de cas de calcul TUI ADAO
-----------------------------------------------

On propose ici des exemples plus complets de cas de calcul TUI ADAO, en donnant
l'objectif de l'exemple et un jeu de commandes qui permet de parvenir � cet
objectif.

Exploitation ind�pendante des r�sultats d'un cas de calcul
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

L'objectif est d'effectuer en TUI la mise en donn�es d'un cas de calcul ADAO,
son ex�cution, puis la r�cup�ration des r�sultats pour ensuite encha�ner sur une
exploitation ind�pendante de ces r�sultats (cette derni�re n'�tant pas d�crite
ici, puisque d�pendante de l'utilisateur).

Les hypoth�ses du cas utilisateur sont les suivantes. On suppose :

#.      que l'on veut recaler 3 param�tres ``alpha``, ``beta`` et ``gamma`` dans un domaine born�,
#.      que l'on dispose d'observations nomm�es ``observations``,
#.      que l'utilisateur dispose en Python d'une fonction de simulation physique appell�e ``simulation`` pr�alablement test�e, qui transforme les 3 param�tres en r�sultats similaires aux observations,
#.      que l'exploitation ind�pendante, que l'utilisateur veut faire, est repr�sent�e ici par l'affichage simple de l'�tat initial, de l'�tat optimal, de la simulation en ce point, des �tats interm�diaires et du nombre d'it�rations d'optimisation.

Pour effectuer de mani�re simple cet essai de cas de calcul TUI, on se donne par
exemple les entr�es suivantes, parfaitement arbitraires, en construisant les
observations par simulation pour se placer dans un cas d'exp�riences jumelles::

    #
    # Construction artificielle d'un exemple de donn�es utilisateur
    # -------------------------------------------------------------
    alpha = 5.
    beta = 7
    gamma = 9.0
    #
    alphamin, alphamax = 0., 10.
    betamin,  betamax  = 3, 13
    gammamin, gammamax = 1.5, 15.5
    #
    def simulation(x):
        import numpy
        __x = numpy.matrix(numpy.ravel(numpy.matrix(x))).T
        __H = numpy.matrix("1 0 0;0 2 0;0 0 3; 1 2 3")
        return __H * __x
    #
    # Observations obtenues par simulation
    # ------------------------------------
    observations = simulation((2, 3, 4))

Le jeu de commandes que l'on peut utiliser est le suivant::

    import numpy
    import adaoBuilder
    #
    # Mise en forme des entr�es
    # -------------------------
    Xb = (alpha, beta, gamma)
    Bounds = (
        (alphamin, alphamax),
        (betamin,  betamax ),
        (gammamin, gammamax))
    #
    # TUI ADAO
    # --------
    case = adaoBuilder.New()
    case.set( 'AlgorithmParameters',
        Algorithm = '3DVAR',
        Parameters = {
            "Bounds":Bounds,
            "MaximumNumberOfSteps":100,
            "StoreSupplementaryCalculations":[
                "CostFunctionJ",
                "CurrentState",
                "SimulatedObservationAtOptimum",
                ],
            }
        )
    case.set( 'Background', Vector = numpy.array(Xb), Stored = True )
    case.set( 'Observation', Vector = numpy.array(observations) )
    case.set( 'BackgroundError', ScalarSparseMatrix = 1.0e10 )
    case.set( 'ObservationError', ScalarSparseMatrix = 1.0 )
    case.set( 'ObservationOperator',
        OneFunction = simulation,
        Parameters  = {"DifferentialIncrement":0.0001},
        )
    case.set( 'Observer', Variable="CurrentState", Template="ValuePrinter" )
    case.execute()
    #
    # Exploitation ind�pendante
    # -------------------------
    Xbackground   = case.get("Background")
    Xoptimum      = case.get("Analysis")[-1]
    FX_at_optimum = case.get("SimulatedObservationAtOptimum")[-1]
    J_values      = case.get("CostFunctionJ")[:]
    print
    print "Nombre d'it�rations internes...: %i"%len(J_values)
    print "Etat initial...................:",numpy.ravel(Xbackground)
    print "Etat optimal...................:",numpy.ravel(Xoptimum)
    print "Simulation � l'�tat optimal....:",numpy.ravel(FX_at_optimum)
    print

L'ex�cution de jeu de commandes donne le r�sultat suivant::

    CurrentState [ 5.  7.  9.]
    CurrentState [ 0.   3.   1.5]
    CurrentState [ 1.40006418  3.86705307  3.7061137 ]
    CurrentState [ 1.42580231  3.68474804  3.81008738]
    CurrentState [ 1.60220353  3.0677108   4.06146069]
    CurrentState [ 1.72517855  3.03296953  4.04915706]
    CurrentState [ 2.00010755  3.          4.00055409]
    CurrentState [ 1.99995528  3.          3.99996367]
    CurrentState [ 2.00000007  3.          4.00000011]
    CurrentState [ 2.  3.  4.]

    Nombre d'it�rations internes...: 10
    Etat initial...................: [ 5.  7.  9.]
    Etat optimal...................: [ 2.  3.  4.]
    Simulation � l'�tat optimal....: [  2.   6.  12.  20.]

Comme il se doit en exp�riences jumelles, on constate que l'on retouve bien les
param�tres qui ont servi � construire artificiellement les observations.

.. R�conciliation de courbes � l'aide de MedCoupling
.. +++++++++++++++++++++++++++++++++++++++++++++++++

.. Utilisation de fonctions de surveillance de type "observer"
.. +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Suivre d'un recalage � l'aide de MatPlotLib
.. +++++++++++++++++++++++++++++++++++++++++++

.. Equivalences entre l'interface graphique (GUI) et l'interface textuelle (TUI)
.. -----------------------------------------------------------------------------

.. [HOMARD] Pour de plus amples informations sur HOMARD, voir le *module HOMARD* et son aide int�gr�e disponible dans le menu principal *Aide* de l'environnement SALOME.

.. [PARAVIS] Pour de plus amples informations sur PARAVIS, voir le *module PARAVIS* et son aide int�gr�e disponible dans le menu principal *Aide* de l'environnement SALOME.

.. [YACS] Pour de plus amples informations sur YACS, voir le *module YACS* et son aide int�gr�e disponible dans le menu principal *Aide* de l'environnement SALOME.
