.. _section_advanced:

================================================================================
Usages avanc�s du module ADAO
================================================================================

Cette section pr�sente des m�thodes avanc�es d'usage du module ADAO, comment
obtenir plus d'information lors d'un calcul, ou comment l'utiliser sans
l'interface graphique (GUI). Cela n�cessite de savoir comment trouver les
fichiers ou les commandes incuses dans l'installation compl�te de SALOME. Tous
les noms � remplacer par l'utilisateur sont indiqu�s par la syntaxe ``<...>``.

Convertir et ex�cuter un fichier de commandes ADAO (JDC) par l'interm�diaire d'un script shell
----------------------------------------------------------------------------------------------

Il est possible de convertir et ex�cuter une fichier de commandes ADAO (JDC, ou
paire de fichiers ".comm/.py", qui se trouvent dans le r�pertoire ``<R�pertoire
du fichier JDC ADAO>``) automatiquement en utilisant un script de commandes
shell "type" contenant toutes les �tapes requises. L'utilisateur doit savoir o�
se trouvent les principaux fichiers de lancement de SALOME, et en particulier le
fichier ``runAppli``. Le r�pertoire dans lequel ce fichier r�side est
symboliquement nomm� ``<R�pertoire principal d'installation de SALOME>`` et doit
�tre remplac� par le bon dans le mod�le "type" de fichier shell.

Lorsqu'un fichier de commande ADAO est construit par l'interface d'�dition
EFICAS d'ADAO et est enregistr�, s'il est nomm� par exemple "EtudeAdao1.comm",
alors un fichier compagnon nomm� "EtudeAdao1.py" est automatiquement cr�� dans
la m�me r�pertoire. Il est nomm� ``<Fichier Python ADAO>`` dans le mod�le
"type", et il est converti vers YACS comme un ``<Sch�ma xml YACS ADAO>``.
Ensuite, il peut �tre ex�cut� en mode console en utilisant la commande standard
en mode console de YACS (voir la documentation YACS pour de plus amples
informations).

Dans l'exemple, on choisit de d�marrer et arr�ter le serveur d'application
SALOME dans le m�me script, ce qui n'est pas n�cessaire, mais utile pour �viter
des sessions SALOME en attente. On choisit aussi de supprimer le fichier de
``<Sch�ma xml YACS ADAO>`` car c'est un fichier g�n�r�. L'utilisateur de ce
script a seulement besoin de remplacer le texte contenu entre les symboles
``<...>``

Le mod�le "type" de ce script de commandes shell est le suivant::

    #!/bin/bash
    export USERDIR=<R�pertoire du fichier JDC ADAO>
    export SALOMEDIR=<R�pertoire principal d'installation de SALOME>
    $SALOMEDIR/runAppli -k -t
    $SALOMEDIR/runSession python \
        $SALOMEDIR/bin/salome/AdaoYacsSchemaCreator.py \
        $USERDIR/<Fichier Python ADAO> $USERDIR/<Sch�ma xml YACS ADAO>
    $SALOMEDIR/runSession driver $USERDIR/<Sch�ma xml YACS ADAO>
    $SALOMEDIR/runSession killSalome.py
    rm -f $USERDIR/<Sch�ma xml YACS ADAO>

Les sorties standard et d'erreur se font � la console.

Ex�cuter un sch�ma de calcul ADAO dans YACS en utilisant le mode "texte" (TUI)
------------------------------------------------------------------------------

Cette section d�crit comment ex�cuter en mode TUI (Text User Interface) un
sch�ma de calcul YACS, obtenu par la fonction "*Exporter vers YACS*" d'ADAO.
Cela utilise le mode texte standard de YACS, qui est rapidement rappel� ici
(voir la documentation YACS pour de plus amples informations) � travers un
exemple simple. Comme d�crit dans la documentation, un sch�ma XML peut �tre
charg� en python. On donne ici une s�quence compl�te de commandes pour tester la
validit� du sch�ma avant de l'ex�cuter, ajoutant des lignes suppl�mentaires
initiales pour charger de mani�re explicite le catalogue de types pour �viter
des difficult�s obscures::

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
ou pour rassembler les r�sultats pour un usage ult�rieur.

Obtenir des informations sur des variables sp�ciales au cours d'un calcul ADAO en YACS
--------------------------------------------------------------------------------------

Certaines variables sp�ciales internes � l'optimisation, utilis�es au cours des
calculs, peuvent �tre surveill�es durant un calcul ADAO en YACS. Ces variables
peuvent �tre affich�es, trac�es, enregistr�es, etc. C'est r�alisable en
utilisant des "*observers*", qui sont des scripts, chacun associ� � une
variable. Pour pouvoir utiliser cette capacit�, l'utilisateur doit construire
des scripts disposant en entr�e standard (i.e. disponible dans l'espace de
nommage) des variables ``var`` et ``info``. La variable ``var`` est � utiliser
de la m�me mani�re que l'objet final ADD, c'est-�-dire comme un objet de type
liste/tuple.

Des mod�les ("templates") sont disponibles lors de l'�dition le cas ADAO dans
l'�diteur EFICAS. Ces scripts simples peuvent �tre adapt�s par l'utilisateur,
soit dans l'�tape EFICAS, ou dans l'�tape d'�dition YACS, pour am�liorer
l'adaptation du calcul ADAO dans YACS.

A titre d'exemple, voici un script tr�s simple (similaire au mod�le
"*ValuePrinter*") utilisable pour afficher la valeur d'une variable surveill�e::

    print "    --->",info," Value =",var[-1]

Stock� comme un fichier Python, ce script peut �tre associ� � chaque variable
pr�sente dans le mot-cl� "*SELECTION*" de la commande "*Observers*":
"*Analysis*", "*CurrentState*", "*CostFunction*"... La valeur courante de la
variable sera affich�e � chaque �tape de l'algorithme d'optimisation ou
d'assimilation. Les "*observers*" peuvent inclure des capacit�s d'affichage
graphique, de stockage, d'affichage complexe, de traitement statistique, etc.

Obtenir plus d'information lors du d�roulement d'un calcul
----------------------------------------------------------

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
prudent dans le stockage de "grosses" variables car cela coute du temps,
quel que soit le niveau de surveillance choisi (c'est-�-dire m�me si ces
variables ne sont pas affich�es).

Passer d'une version d'ADAO � une nouvelle
------------------------------------------

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

Passer de la version 7.2 � la 7.3
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilit� connue pour les fichiers de cas ADAO. La
proc�dure de mont�e en version consiste � lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et de l'enregistrer avec un nouveau nom.

Passer de la version 6.6 � la 7.2
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilit� connue pour les fichiers de cas ADAO. La
proc�dure de mont�e en version consiste � lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et de l'enregistrer avec un nouveau nom.

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

Passer de la version 6.5 � la 6.6
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilit� connue pour les fichiers de cas ADAO. La
proc�dure de mont�e en version consiste � lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et de l'enregistrer avec un nouveau nom.

Il y a une incompatibilit� introduite dans la d�nomination des op�rateurs
�l�mentaires utilis�s pour l'op�rateur d'observation par script. Les nouveaux
noms requis sont "*DirectOperator*", "*TangentOperator*" et "*AdjointOperator*",
comme d�crit dans la quatri�me partie du chapitre :ref:`section_reference`. Les
scripts d'op�rateur doivent �tre modifi�s.

Passer de la version 6.4 � la 6.5
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilit� connue pour les fichiers de cas ADAO. La
proc�dure de mont�e en version consiste � lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et de l'enregistrer avec un nouveau nom.

Passer de la version 6.3 � la 6.4
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilit� connue pour les fichiers de cas ADAO. La
proc�dure de mont�e en version consiste � lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et de l'enregistrer avec un nouveau nom.
