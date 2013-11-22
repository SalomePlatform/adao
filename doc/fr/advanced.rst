.. _section_advanced:

================================================================================
Usages avancés du module ADAO
================================================================================

Cette section présente des méthodes avancées d'usage du module ADAO, comment
obtenir plus d'information lors d'un calcul, ou comment l'utiliser sans
l'interface graphique (GUI). Cela nécessite de savoir comment trouver les
fichiers ou les commandes incuses dans l'installation complète de SALOME. Tous
les noms à remplacer par l'utilisateur sont indiqués par la syntaxe ``<...>``.

Convertir et exécuter un fichier de commandes ADAO (JDC) par l'intermédiaire d'un script shell
----------------------------------------------------------------------------------------------

Il est possible de convertir et exécuter une fichier de commandes ADAO (JDC, ou
paire de fichiers ".comm/.py", qui se trouvent dans le répertoire ``<Répertoire
du fichier JDC ADAO>``) automatiquement en utilisant un script de commandes
shell "type" contenant toutes les étapes requises. L'utilisateur doit savoir où
se trouvent les principaux fichiers de lancement de SALOME, et en particulier le
fichier ``runAppli``. Le répertoire dans lequel ce fichier réside est
symboliquement nommé ``<Répertoire principal d'installation de SALOME>`` et doit
être remplacé par le bon dans le modèle "type" de fichier shell.

Lorsqu'un fichier de commande ADAO est construit par l'interface d'édition
EFICAS d'ADAO et est enregistré, s'il est nommé par exemple "EtudeAdao1.comm",
alors un fichier compagnon nommé "EtudeAdao1.py" est automatiquement créé dans
la même répertoire. Il est nommé ``<Fichier Python ADAO>`` dans le modèle
"type", et il est converti vers YACS comme un ``<Schéma xml YACS ADAO>``.
Ensuite, il peut être exécuté en mode console en utilisant la commande standard
en mode console de YACS (voir la documentation YACS pour de plus amples
informations).

Dans l'exemple, on choisit de démarrer et arrêter le serveur d'application
SALOME dans le même script, ce qui n'est pas nécessaire, mais utile pour éviter
des sessions SALOME en attente. On choisit aussi de supprimer le fichier de
``<Schéma xml YACS ADAO>`` car c'est un fichier généré. L'utilisateur de ce
script a seulement besoin de remplacer le texte contenu entre les symboles
``<...>``

Le modèle "type" de ce script de commandes shell est le suivant::

    #!/bin/bash
    export USERDIR=<Répertoire du fichier JDC ADAO>
    export SALOMEDIR=<Répertoire principal d'installation de SALOME>
    $SALOMEDIR/runAppli -k -t
    $SALOMEDIR/runSession python \
        $SALOMEDIR/bin/salome/AdaoYacsSchemaCreator.py \
        $USERDIR/<Fichier Python ADAO> $USERDIR/<Schéma xml YACS ADAO>
    $SALOMEDIR/runSession driver $USERDIR/<Schéma xml YACS ADAO>
    $SALOMEDIR/runSession killSalome.py
    rm -f $USERDIR/<Schéma xml YACS ADAO>

Les sorties standard et d'erreur se font à la console.

Exécuter un schéma de calcul ADAO dans YACS en utilisant le mode "texte" (TUI)
------------------------------------------------------------------------------

Cette section décrit comment exécuter en mode TUI (Text User Interface) un
schéma de calcul YACS, obtenu par la fonction "*Exporter vers YACS*" d'ADAO.
Cela utilise le mode texte standard de YACS, qui est rapidement rappelé ici
(voir la documentation YACS pour de plus amples informations) à travers un
exemple simple. Comme décrit dans la documentation, un schéma XML peut être
chargé en python. On donne ici une séquence complète de commandes pour tester la
validité du schéma avant de l'exécuter, ajoutant des lignes supplémentaires
initiales pour charger de manière explicite le catalogue de types pour éviter
des difficultés obscures::

    #-*-coding:iso-8859-1-*-
    import pilot
    import SALOMERuntime
    import loader
    SALOMERuntime.RuntimeSALOME_setRuntime()

    r = pilot.getRuntime()
    xmlLoader = loader.YACSLoader()
    xmlLoader.registerProcCataLoader()
    try:
     catalogAd = r.loadCatalog("proc", "<Schéma xml YACS ADAO>")
    except:
      pass
    r.addCatalog(catalogAd)

    try:
        p = xmlLoader.load("<Schéma xml YACS ADAO>")
    except IOError,ex:
        print "IO exception:",ex

    logger = p.getLogger("parser")
    if not logger.isEmpty():
        print "The imported file has errors :"
        print logger.getStr()

    if not p.isValid():
        print "Le schéma n'est pas valide et ne peut pas être exécuté"
        print p.getErrorReport()

    info=pilot.LinkInfo(pilot.LinkInfo.ALL_DONT_STOP)
    p.checkConsistency(info)
    if info.areWarningsOrErrors():
        print "Le schéma n'est pas cohérent et ne peut pas être exécuté"
        print info.getGlobalRepr()

    e = pilot.ExecutorSwig()
    e.RunW(p)
    if p.getEffectiveState() != pilot.DONE:
        print p.getErrorReport()

Cette démarche permet par exemple d'éditer le schéma YACS XML en mode texte TUI,
ou pour rassembler les résultats pour un usage ultérieur.

Obtenir des informations sur des variables spéciales au cours d'un calcul ADAO en YACS
--------------------------------------------------------------------------------------

Certaines variables spéciales internes à l'optimisation, utilisées au cours des
calculs, peuvent être surveillées durant un calcul ADAO en YACS. Ces variables
peuvent être affichées, tracées, enregistrées, etc. C'est réalisable en
utilisant des "*observers*", qui sont des scripts, chacun associé à une
variable. Pour pouvoir utiliser cette capacité, l'utilisateur doit construire
des scripts disposant en entrée standard (i.e. disponible dans l'espace de
nommage) des variables ``var`` et ``info``. La variable ``var`` est à utiliser
de la même manière que l'objet final ADD, c'est-à-dire comme un objet de type
liste/tuple.

Des modèles ("templates") sont disponibles lors de l'édition le cas ADAO dans
l'éditeur EFICAS. Ces scripts simples peuvent être adaptés par l'utilisateur,
soit dans l'étape EFICAS, ou dans l'étape d'édition YACS, pour améliorer
l'adaptation du calcul ADAO dans YACS.

A titre d'exemple, voici un script trés simple (similaire au modèle
"*ValuePrinter*") utilisable pour afficher la valeur d'une variable surveillée::

    print "    --->",info," Value =",var[-1]

Stocké comme un fichier Python, ce script peut être associé à chaque variable
présente dans le mot-clé "*SELECTION*" de la commande "*Observers*":
"*Analysis*", "*CurrentState*", "*CostFunction*"... La valeur courante de la
variable sera affichée à chaque étape de l'algorithme d'optimisation ou
d'assimilation. Les "*observers*" peuvent inclure des capacités d'affichage
graphique, de stockage, d'affichage complexe, de traitement statistique, etc.

Obtenir plus d'information lors du déroulement d'un calcul
----------------------------------------------------------

Lors du déroulement d'un calcul, des données et messages utiles sont
disponibles. Il y a deux manières d'obtenir ces informations.

La première, et la manière préférentielle, est d'utiliser la variable interne
"*Debug*" disponible dans chaque cas ADAO. Elle est atteignable dans l'interface
graphique d'édition du module. La mettre à "*1*" permet d'envoyer des messages
dans la fenêtre de sortie de l'exécution dans YACS ("*YACS Container Log*").

La seconde consiste à utiliser le module Python natif "*logging*" (voir la
documentation Python http://docs.python.org/library/logging.html pour de plus
amples informations sur ce module). Dans l'ensemble du schéma YACS,
principalement à travers les entrées sous forme de scripts, l'utilisateur peut
fixer le niveau de logging en accord avec les besoins d'informations détaillées.
Les différents niveaux de logging sont : "*DEBUG*", "*INFO*", "*WARNING*",
"*ERROR*", "*CRITICAL*". Toutes les informations associées à un niveau sont
affichées à tous les niveaux au-dessus de celui-ci (inclut). La méthode la plus
facile consiste à changer le niveau de surveillance en utilisant les lignes
Python suivantes::

    import logging
    logging.getLogger().setLevel(logging.DEBUG)

Le niveau par défaut standard de surveillance par logging est "*WARNING*", le
niveau par défaut dans le module ADAO est "*INFO*".

Il est aussi recommandé d'inclure de la surveillance par logging ou des
mécanismes de débogage dans le code de simulation, et de les utiliser en
conjonction avec les deux méthodes précédentes. Néanmoins, il convient d'être
prudent dans le stockage de "grosses" variables car cela coute du temps,
quel que soit le niveau de surveillance choisi (c'est-à-dire même si ces
variables ne sont pas affichées).

Passer d'une version d'ADAO à une nouvelle
------------------------------------------

Le module ADAO et ses fichiers de cas ".comm" sont identifiés par des versions,
avec des caractéristiques "Major", "Minor" et "Revision". Une version
particulière est numérotée "Major.Minor.Revision", avec un lien fort avec la
numérotation de la plateforme SALOME.

Chaque version "Major.Minor.Revision" du module ADAO peut lire les fichiers de
cas ADAO de la précédente version mineure "Major.Minor-1.*". En général, elle
peut aussi lire les fichiers de cas de toutes les versions mineures "Major.*.*"
d'une branche majeure, mais ce n'est pas obligatoirement vrai pour toutes les
commandes ou tous les mots-clés. En général aussi, un fichier de cas ADAO d'une
version ne peut pas être lu par une précédente version mineure ou majeure du
module ADAO.

Passer de la version 7.2 à la 7.3
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilité connue pour les fichiers de cas ADAO. La
procédure de montée en version consiste à lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et de l'enregistrer avec un nouveau nom.

Passer de la version 6.6 à la 7.2
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilité connue pour les fichiers de cas ADAO. La
procédure de montée en version consiste à lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et de l'enregistrer avec un nouveau nom.

Il y a une incompatibilité introduite dans les fichiers de script de
post-processing ou d'observers. L'ancienne syntaxe pour interroger un objet
résultat, comme celui d'analyse "*Analysis*" (fourni dans un script à travers le
mot-clé "*UserPostAnalysis*"), était par exemple::

    Analysis = ADD.get("Analysis").valueserie(-1)
    Analysis = ADD.get("Analysis").valueserie()

La nouvelle syntaxe est entièrement compatible avec celle (classique) pour les
objets de type liste ou tuple::

    Analysis = ADD.get("Analysis")[-1]
    Analysis = ADD.get("Analysis")[:]

Les scripts de post-processing doivent être modifiés.

Passer de la version 6.5 à la 6.6
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilité connue pour les fichiers de cas ADAO. La
procédure de montée en version consiste à lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et de l'enregistrer avec un nouveau nom.

Il y a une incompatibilité introduite dans la dénomination des opérateurs
élémentaires utilisés pour l'opérateur d'observation par script. Les nouveaux
noms requis sont "*DirectOperator*", "*TangentOperator*" et "*AdjointOperator*",
comme décrit dans la quatrième partie du chapitre :ref:`section_reference`. Les
scripts d'opérateur doivent être modifiés.

Passer de la version 6.4 à la 6.5
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilité connue pour les fichiers de cas ADAO. La
procédure de montée en version consiste à lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et de l'enregistrer avec un nouveau nom.

Passer de la version 6.3 à la 6.4
+++++++++++++++++++++++++++++++++

Il n'y a pas d'incompatibilité connue pour les fichiers de cas ADAO. La
procédure de montée en version consiste à lire l'ancien fichier de cas ADAO avec
le nouveau module SALOME/ADAO, et de l'enregistrer avec un nouveau nom.
