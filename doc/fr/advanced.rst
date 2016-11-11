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

.. _section_advanced:

================================================================================
**[DocU]** Usages avanc�s du module ADAO
================================================================================

Cette section pr�sente des m�thodes avanc�es d'usage du module ADAO, comment
obtenir plus d'information lors d'un calcul, ou comment l'utiliser sans
l'interface graphique (GUI). Cela n�cessite de savoir comment trouver les
fichiers ou les commandes incluses dans l'installation compl�te de SALOME. Tous
les noms � remplacer par l'utilisateur sont indiqu�s par la syntaxe ``<...>``.

Convertir et ex�cuter un fichier de commandes ADAO (JDC) par l'interm�diaire d'un script Shell
----------------------------------------------------------------------------------------------

Il est possible de convertir et ex�cuter une fichier de commandes ADAO (JDC, ou
paire de fichiers ".comm/.py", qui se trouvent dans le r�pertoire ``<R�pertoire
du fichier JDC ADAO>``) automatiquement en utilisant un script de commandes
Shell "type" contenant toutes les �tapes requises. Si la commande principale de
lancement de SALOME, nomm�e ``salome``, n'est pas couramment accessible dans un
terminal courant, l'utilisateur doit savoir o� se trouvent les principaux
fichiers de lancement de SALOME, et en particulier ce fichier ``salome``. Le
r�pertoire dans lequel ce fichier r�side est symboliquement nomm� ``<R�pertoire
principal d'installation de SALOME>`` et doit �tre remplac� par le bon dans le
mod�le "type" de fichier Shell.

Lorsqu'un fichier de commande ADAO est construit par l'interface d'�dition
graphique d'ADAO et est enregistr�, s'il est nomm� par exemple
"EtudeAdao1.comm", alors un fichier compagnon nomm� "EtudeAdao1.py" est
automatiquement cr�� dans la m�me r�pertoire. Il est nomm� ``<Fichier Python
ADAO>`` dans le mod�le "type", et il est converti vers YACS comme un ``<Sch�ma
xml YACS ADAO>`` sous la forme d'un fichier en ".xml" nomm� "EtudeAdao1.xml".
Ensuite, ce dernier peut �tre ex�cut� en mode console en utilisant l'ordre
standard du mode console de YACS (voir la documentation YACS pour de plus amples
informations).

Dans tous les exemples de fichiers de commandes Shell de lancement, on choisit
de d�marrer et arr�ter le serveur d'application SALOME dans le m�me script. Ce
n'est pas indispensable, mais c'est utile pour �viter des sessions SALOME en
attente.

L'exemple le plus simple consiste uniquement � lancer l'ex�cution d'un sch�ma
YACS donn�, qui a pr�alablement �t� g�n�r� par l'utilisateur en interface
graphique. Dans ce cas, en ayant pris soin de remplacer les textes contenus
entre les symboles ``<...>``, il suffit d'enregistrer le script de commandes
Shell suivant::

    #!/bin/bash
    USERDIR="<R�pertoire du fichier JDC ADAO>"
    SALOMEDIR="<R�pertoire principal d'installation de SALOME>"
    $SALOMEDIR/salome start -k -t
    $SALOMEDIR/salome shell -- "driver $USERDIR/<Sch�ma xml YACS ADAO>"
    $SALOMEDIR/salome shell killSalome.py

Il faut ensuite le rendre ex�cutable pour l'ex�cuter.

Un exemple une peu plus complet consiste � lancer l'ex�cution d'un sch�ma YACS
indiqu� par l'utilisateur, en ayant pr�alablement v�rifi� sa disponibilit�. Pour
cela, en rempla�ant le texte ``<R�pertoire principal d'installation de
SALOME>``, il suffit d'enregistrer le script de commandes Shell suivant::

    #!/bin/bash
    if (test $# != 1)
    then
      echo -e "\nUsage: $0 <Sch�ma xml YACS ADAO>\n"
      exit
    else
      USERFILE="$1"
    fi
    if (test ! -e $USERFILE)
    then
      echo -e "\nErreur : le fichier XML nomm� $USERFILE n'existe pas.\n"
      exit
    else
      SALOMEDIR="<R�pertoire principal d'installation de SALOME>"
      $SALOMEDIR/salome start -k -t
      $SALOMEDIR/salome shell -- "driver $USERFILE"
      $SALOMEDIR/salome shell killSalome.py
    fi

Un autre exemple de script consiste � ajouter la conversion du fichier de
commandes ADAO (JDC, ou paire de fichiers ".comm/.py") en un sch�ma YACS associ�
(fichier ".xml"). A la fin du script, on choisit aussi de supprimer le fichier
de ``<Sch�ma xml YACS ADAO>`` car c'est un fichier g�n�r�. Pour cela, en ayant
bien pris soin de remplacer le texte ``<R�pertoire principal d'installation de
SALOME>``, il suffit d'enregistrer le script de commandes Shell suivant::

    #!/bin/bash
    if (test $# != 1)
    then
      echo -e "\nUsage: $0 <Cas .comm/.py ADAO>\n"
      exit
    else
      D=`dirname $1`
      F=`basename -s .comm $1`
      F=`basename -s .py $F`
      USERFILE="$D/$F"
    fi
    if (test ! -e $USERFILE.py)
    then
      echo -e "\nErreur : le fichier PY nomm� $USERFILE.py n'existe pas.\n"
      exit
    else
      SALOMEDIR="<R�pertoire principal d'installation de SALOME>"
      $SALOMEDIR/salome start -k -t
      $SALOMEDIR/salome shell -- "python $SALOMEDIR/bin/salome/AdaoYacsSchemaCreator.py $USERFILE.py $USERFILE.xml"
      $SALOMEDIR/salome shell -- "driver $USERFILE.xml"
      $SALOMEDIR/salome shell killSalome.py
      rm -f $USERFILE.xml
    fi

Dans tous les cas, les sorties standard et d'erreur se font dans le terminal de
lancement.

Ex�cuter un sch�ma de calcul ADAO dans YACS en utilisant le mode "texte" (TUI YACS)
-----------------------------------------------------------------------------------

Cette section d�crit comment ex�cuter en mode TUI (Text User Interface) YACS un
sch�ma de calcul YACS, obtenu dans l'interface graphique par la fonction
"*Exporter vers YACS*" d'ADAO. Cela utilise le mode texte standard de YACS, qui
est rapidement rappel� ici (voir la documentation YACS pour de plus amples
informations) � travers un exemple simple. Comme d�crit dans la documentation,
un sch�ma XML peut �tre charg� en python. On donne ici une s�quence compl�te de
commandes pour tester la validit� du sch�ma avant de l'ex�cuter, ajoutant des
lignes suppl�mentaires initiales pour charger de mani�re explicite le catalogue
de types pour �viter d'obscures difficult�s::

    #-*-coding:iso-8859-1-*-
    import pilot
    import SALOMERuntime
    import loader
    SALOMERuntime.RuntimeSALOME_setRuntime()

    r = pilot.getRuntime()
    xmlLoader = loader.YACSLoader()
    xmlLoader.registerProcCataLoader()
    try:
     catalogAd = r.loadCatalog("proc", "<Sch�ma xml YACS ADAO>")
    except:
      pass
    r.addCatalog(catalogAd)

    try:
        p = xmlLoader.load("<Sch�ma xml YACS ADAO>")
    except IOError,ex:
        print "IO exception:",ex

    logger = p.getLogger("parser")
    if not logger.isEmpty():
        print "The imported file has errors :"
        print logger.getStr()

    if not p.isValid():
        print "Le sch�ma n'est pas valide et ne peut pas �tre ex�cut�"
        print p.getErrorReport()

    info=pilot.LinkInfo(pilot.LinkInfo.ALL_DONT_STOP)
    p.checkConsistency(info)
    if info.areWarningsOrErrors():
        print "Le sch�ma n'est pas coh�rent et ne peut pas �tre ex�cut�"
        print info.getGlobalRepr()

    e = pilot.ExecutorSwig()
    e.RunW(p)
    if p.getEffectiveState() != pilot.DONE:
        print p.getErrorReport()

Cette d�marche permet par exemple d'�diter le sch�ma YACS XML en mode texte TUI,
ou de rassembler les r�sultats pour un usage ult�rieur.

.. _section_advanced_R:

Ex�cuter un calcul ADAO en environnement R en utilisant l'interface TUI ADAO
----------------------------------------------------------------------------

.. index:: single: R
.. index:: single: rPython

Pour �tendre les possibilit�s d'analyse et de traitement, il est possible
d'utiliser les calculs ADAO dans l'environnement **R** (voir [R]_ pour plus de
d�tails). Ce dernier est disponible dans SALOME en lan�ant l'interpr�teur R dans
le shell "``salome shell``". Il faut de plus disposer, en R, du package
"*rPython*", qui peut si n�cessaire �tre install� par l'utilisateur � l'aide de
la commande R suivante::

    #-*-coding:iso-8859-1-*-
    #
    # IMPORTANT : � ex�cuter dans l'interpr�teur R
    # --------------------------------------------
    install.packages("rPython")

On se reportera � la documentation [GilBellosta15]_ pour de plus amples
renseignements sur ce package.

Les calculs ADAO d�finis en interface textuelle (API/TUI, voir la
:ref:`section_tui`) peuvent alors �tre interpr�t�s depuis l'environnement R, en
utilisant des donn�es et des informations depuis R. La d�marche est illustr�e
sur :ref:`subsection_tui_example`, propos� dans la description de l'interface
API/TUI. Dans l'interpr�teur R, on peut ex�cuter les commandes suivantes,
directement issues de l'exemple simple::

    #-*-coding:iso-8859-1-*-
    #
    # IMPORTANT : � ex�cuter dans l'interpr�teur R
    # --------------------------------------------
    library(rPython)
    python.exec("
        from numpy import array
        import adaoBuilder
        case = adaoBuilder.New()
        case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
        case.set( 'Background',          Vector=[0, 1, 2] )
        case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
        case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
        case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
        case.set( 'ObservationOperator', Matrix='1 0 0;0 2 0;0 0 3' )
        case.set( 'Observer',            Variable='Analysis', Template='ValuePrinter' )
        case.execute()
    ")

dont le r�sultat est::

    Analysis [ 0.25000264  0.79999797  0.94999939]

Dans la r�daction des calculs ADAO ex�cut�s depuis R, il convient d'�tre tr�s
attentif au bon usage des guillemets simples et doubles, qui ne doivent pas
collisionner entre les deux langages.

Les donn�es peuvent venir l'environnement R et doivent �tre rang�es dans des
variables correctement assign�es, pour �tre utilis�es ensuite en Python pour
ADAO. On se reportera � la documentation [GilBellosta15]_ pour la mise en
oeuvre. On peut transformer l'exemple ci-dessus pour utiliser des donn�es
provenant de R pour alimenter les trois variables d'�bauche, d'observation et
d'op�rateur d'observation. On r�cup�re � la fin l'�tat optimal dans une variable
R aussi. Les autres lignes sont identiques. L'exemple devient ainsi::

    #-*-coding:iso-8859-1-*-
    #
    # IMPORTANT : � ex�cuter dans l'interpr�teur R
    # --------------------------------------------
    #
    # Variables R
    # -----------
    xb <- 0:2
    yo <- c(0.5, 1.5, 2.5)
    h <- '1 0 0;0 2 0;0 0 3'
    #
    # Code Python
    # -----------
    library(rPython)
    python.assign( "xb",  xb )
    python.assign( "yo",  yo )
    python.assign( "h",  h )
    python.exec("
        from numpy import array
        import adaoBuilder
        case = adaoBuilder.New()
        case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
        case.set( 'Background',          Vector=xb )
        case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
        case.set( 'Observation',         Vector=array(yo) )
        case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
        case.set( 'ObservationOperator', Matrix=str(h) )
        case.set( 'Observer',            Variable='Analysis', Template='ValuePrinter' )
        case.execute()
        xa = list(case.get('Analysis')[-1])
    ")
    #
    # Variables R
    # -----------
    xa <- python.get("xa")

On remarquera les conversions explicite de type ``str`` et ``list`` pour
s'assurer que les donn�es sont bien transmises en type standards connus du
package "*rPython*". De plus, ce sont les donn�es qui peuvent �tre transf�r�es
entre les deux langages, et pas des fonctions ou m�thodes. Il convient donc
d'�laborer en Python de mani�re g�n�rique les fonctions d'ex�cution requises par
ADAO, et de leur transmettre ensuite de mani�re correcte les donn�es disponibles
en R.

Les cas plus complets, propos�s dans les :ref:`subsection_tui_advanced`, peuvent
�tre ex�cut�s de la m�me mani�re, et ils donnent le m�me r�sultat que dans
l'interface API/TUI en Python standard.

.. _section_advanced_observer:

Obtenir des informations sur des variables sp�ciales au cours d'un calcul ADAO en YACS
--------------------------------------------------------------------------------------

.. index:: single: Observer
.. index:: single: Observer Template

Certaines variables sp�ciales internes � l'optimisation, utilis�es au cours des
calculs, peuvent �tre surveill�es durant un calcul ADAO. Ces variables peuvent
�tre affich�es, trac�es, enregistr�es, etc. C'est r�alisable en utilisant des
"*observer*", qui sont des scripts, chacun associ� � une variable.

Des mod�les ("templates") sont disponibles lors de l'�dition le cas ADAO dans
l'�diteur graphique. Ces scripts simples peuvent �tre adapt�s par l'utilisateur,
soit dans l'�tape d'�dition int�gr�e, ou dans l'�tape d'�dition avant
l'ex�cution, pour am�liorer l'adaptation du calcul ADAO dans le superviseur
d'ex�cution de SALOME.

Pour mettre en oeuvre ces "*observer*" de mani�re efficace, on se reportera aux
:ref:`ref_observers_requirements`.

Obtenir plus d'information lors du d�roulement d'un calcul
----------------------------------------------------------

.. index:: single: Logging

Lors du d�roulement d'un calcul, des donn�es et messages utiles sont
disponibles. Il y a deux mani�res d'obtenir ces informations.

La premi�re, et la mani�re pr�f�rentielle, est d'utiliser la variable interne
"*Debug*" disponible dans chaque cas ADAO. Elle est atteignable dans l'interface
graphique d'�dition du module. La mettre � "*1*" permet d'envoyer des messages
dans la fen�tre de sortie de l'ex�cution dans YACS ("*YACS Container Log*").

La seconde consiste � utiliser le module Python natif "*logging*" (voir la
documentation Python http://docs.python.org/library/logging.html pour de plus
amples informations sur ce module). Dans l'ensemble du sch�ma YACS,
principalement � travers les entr�es sous forme de scripts, l'utilisateur peut
fixer le niveau de logging en accord avec les besoins d'informations d�taill�es.
Les diff�rents niveaux de logging sont : "*DEBUG*", "*INFO*", "*WARNING*",
"*ERROR*", "*CRITICAL*". Toutes les informations associ�es � un niveau sont
affich�es � tous les niveaux au-dessus de celui-ci (inclut). La m�thode la plus
facile consiste � changer le niveau de surveillance en utilisant les lignes
Python suivantes::

    import logging
    logging.getLogger().setLevel(logging.DEBUG)

Le niveau par d�faut standard de surveillance par logging est "*WARNING*", le
niveau par d�faut dans le module ADAO est "*INFO*".

Il est aussi recommand� d'inclure de la surveillance par logging ou des
m�canismes de d�bogage dans le code de simulation, et de les utiliser en
conjonction avec les deux m�thodes pr�c�dentes. N�anmoins, il convient d'�tre
prudent dans le stockage de "grosses" variables car cela co�te du temps,
quel que soit le niveau de surveillance choisi (c'est-�-dire m�me si ces
variables ne sont pas affich�es).

.. _subsection_ref_parallel_df:

Acc�l�rer les calculs de d�riv�es num�riques en utilisant un mode parall�le
---------------------------------------------------------------------------

.. index:: single: EnableMultiProcessing
.. index:: single: NumberOfProcesses

Lors de la d�finition d'un op�rateur, comme d�crit dans le chapitre des
:ref:`section_ref_operator_requirements`, l'utilisateur peut choisir la forme
fonctionnelle "*ScriptWithOneFunction*". Cette forme conduit explicitement �
approximer les op�rateurs tangent et adjoint par un calcul par diff�rences
finies. Il requiert de nombreux appels � l'op�rateur direct (fonction d�finie
par l'utilisateur), au moins autant de fois que la dimension du vecteur d'�tat.
Ce sont ces appels qui peuvent �tre potentiellement ex�cut�s en parall�le.

Sous certaines conditions, il est alors possible d'acc�l�rer les calculs de
d�riv�es num�riques en utilisant un mode parall�le pour l'approximation par
diff�rences finies. Lors de la d�finition d'un cas ADAO, c'est effectu� en
ajoutant le mot-cl� optionnel "*EnableMultiProcessing*", mis � "1", de la
commande "*SCRIPTWITHONEFUNCTION*" dans la d�finition de l'op�rateur. Le mode
parall�le utilise uniquement des ressources locales (� la fois multi-coeurs ou
multi-processeurs) de l'ordinateur sur lequel SALOME est en train de tourner,
demandant autant de ressources que disponible. Si n�cessaire, on peut r�duire
les ressources disponibles en limitant le nombre possible de processus
parall�les gr�ce au mot-cl� optionnel "*NumberOfProcesses*", que l'on met au
maximum souhait� (ou � "0" pour le contr�le automatique, qui est la valeur par
d�faut). Par d�faut, ce mode parall�le est d�sactiv�
("*EnableMultiProcessing=0*").

Les principales conditions pour r�aliser ces calculs parall�les viennent de la
fonction d�finie par l'utilisateur, qui repr�sente l'op�rateur direct. Cette
fonction doit au moins �tre "thread safe" pour �tre ex�cut�e dans un
environnement Python parall�le (notions au-del� du cadre de ce paragraphe). Il
n'est pas �vident de donner des r�gles g�n�rales, donc il est recommand�, �
l'utilisateur qui active ce parall�lisme interne, de v�rifier soigneusement sa
fonction et les r�sultats obtenus.

D'un point de vue utilisateur, certaines conditions, qui doivent �tre r�unies
pour mettre en place des calculs parall�les pour les approximations des
op�rateurs tangent et adjoint, sont les suivantes :

#. La dimension du vecteur d'�tat est sup�rieure � 2 ou 3.
#. Le calcul unitaire de la fonction utilisateur directe "dure un certain temps", c'est-�-dire plus que quelques minutes.
#. La fonction utilisateur directe n'utilise pas d�j� du parall�lisme (ou l'ex�cution parall�le est d�sactiv�e dans le calcul de l'utilisateur).
#. La fonction utilisateur directe n'effectue pas d'acc�s en lecture/�criture � des ressources communes, principalement des donn�es stock�es, des fichiers de sortie ou des espaces m�moire.
#. Les "*observer*" ajout�s par l'utilisateur n'effectuent pas d'acc�s en lecture/�criture � des ressources communes, comme des fichiers ou des espaces m�moire.

Si ces conditions sont satisfaites, l'utilisateur peut choisir d'activer le
parall�lisme interne pour le calcul des d�riv�es num�riques. Malgr� la
simplicit� d'activation, obtenue en d�finissant une variable seulement,
l'utilisateur est fortement invit� � v�rifier les r�sultats de ses calculs. Il
faut au moins les effectuer une fois avec le parall�lisme activ�, et une autre
fois avec le parall�lisme d�sactiv�, pour comparer les r�sultats. Si cette mise
en oeuvre �choue � un moment ou � un autre, il faut savoir que ce sch�ma de
parall�lisme fonctionne pour des codes complexes, comme *Code_Aster* dans
*SalomeMeca* [SalomeMeca]_ par exemple. Donc, si cela ne marche pas dans votre
cas, v�rifiez bien votre fonction d'op�rateur avant et pendant l'activation du
parall�lisme...

.. warning::

  en cas de doute, il est recommand� de NE PAS ACTIVER ce parall�lisme.

On rappelle aussi qu'il faut choisir dans YACS un container par d�faut de type
"*multi*" pour le lancement du sch�ma, pour permettre une ex�cution
v�ritablement parall�le.

Passer d'une version d'ADAO � une nouvelle
------------------------------------------

.. index:: single: Version

Le module ADAO et ses fichiers de cas ".comm" sont identifi�s par des versions,
avec des caract�ristiques "Major", "Minor" et "Revision". Une version
particuli�re est num�rot�e "Major.Minor.Revision", avec un lien fort avec la
num�rotation de la plateforme SALOME.

Chaque version "Major.Minor.Revision" du module ADAO peut lire les fichiers de
cas ADAO de la pr�c�dente version mineure "Major.Minor-1.*". En g�n�ral, elle
peut aussi lire les fichiers de cas de toutes les versions mineures "Major.*.*"
d'une branche majeure, mais ce n'est pas obligatoirement vrai pour toutes les
commandes ou tous les mots-cl�s. En g�n�ral aussi, un fichier de cas ADAO d'une
version ne peut pas �tre lu par une pr�c�dente version mineure ou majeure du
module ADAO.

Passer de la version 8.x � la 8.y avec x < y
++++++++++++++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilit� connue pour les fichiers de cas ADAO. La
proc�dure de mont�e en version consiste � lire l'ancien fichier de cas ADAO
avec le nouveau module SALOME/ADAO, et � l'enregistrer avec un nouveau nom.

Passer de la version 7.8 � la 8.1
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilit� connue pour les fichiers de cas ADAO. La
proc�dure de mont�e en version consiste � lire l'ancien fichier de cas ADAO
avec le nouveau module SALOME/ADAO, et � l'enregistrer avec un nouveau nom.

Passer de la version 7.x � la 7.y avec x < y
++++++++++++++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilit� connue pour les fichiers de cas ADAO. La
proc�dure de mont�e en version consiste � lire l'ancien fichier de cas ADAO
avec le nouveau module SALOME/ADAO, et � l'enregistrer avec un nouveau nom.

Passer de la version 6.6 � la 7.2
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilit� connue pour les fichiers de cas ADAO. La
proc�dure de mont�e en version consiste � lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et � l'enregistrer avec un nouveau nom.

Il y a une incompatibilit� introduite dans les fichiers de script de
post-processing ou d'observers. L'ancienne syntaxe pour interroger un objet
r�sultat, comme celui d'analyse "*Analysis*" (fourni dans un script � travers le
mot-cl� "*UserPostAnalysis*"), �tait par exemple::

    Analysis = ADD.get("Analysis").valueserie(-1)
    Analysis = ADD.get("Analysis").valueserie()

La nouvelle syntaxe est enti�rement compatible avec celle (classique) pour les
objets de type liste ou tuple::

    Analysis = ADD.get("Analysis")[-1]
    Analysis = ADD.get("Analysis")[:]

Les scripts de post-processing doivent �tre modifi�s.

Passer de la version 6.x � la 6.y avec x < y
++++++++++++++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilit� connue pour les fichiers de cas ADAO. La
proc�dure de mont�e en version consiste � lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et � l'enregistrer avec un nouveau nom.

Il y a une incompatibilit� introduite dans les fichiers de script d'op�rateur,
lors de la d�nomination des op�rateurs �l�mentaires utilis�s pour l'op�rateur
d'observation par script. Les nouveaux noms requis sont "*DirectOperator*",
"*TangentOperator*" et "*AdjointOperator*", comme d�crit dans la quatri�me
partie du chapitre :ref:`section_reference`. Les fichiers de script d'op�rateur
doivent �tre modifi�s.
