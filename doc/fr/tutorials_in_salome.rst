..
   Copyright (C) 2008-2024 EDF R&D

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

.. _section_tutorials_in_salome:

================================================================================
**[DocU]** Tutoriaux sur l'utilisation du module ADAO dans SALOME
================================================================================

.. |eficas_new| image:: images/eficas_new.png
   :align: middle
   :scale: 75%
.. |eficas_save| image:: images/eficas_save.png
   :align: middle
   :scale: 75%
.. |eficas_saveas| image:: images/eficas_saveas.png
   :align: middle
   :scale: 75%
.. |eficas_totui| image:: images/eficas_totui.png
   :align: middle
   :scale: 50%
.. |eficas_yacs| image:: images/eficas_yacs.png
   :align: middle
   :scale: 75%

Cette section présente quelques exemples d'utilisation du module ADAO dans
SALOME. Le premier montre comment construire un cas très simple d'assimilation
de données définissant explicitement toutes les données d'entrée requises à
travers l'interface utilisateur graphique EFICAS (GUI). Le second montre, sur
le même cas, comment définir les données d'entrée à partir de sources externes
à travers des scripts. On présente ici toujours des scripts Python car ils sont
directement insérables dans les noeuds de script de YACS, mais les fichiers
externes peuvent utiliser d'autres langages.

Ces exemples sont intentionnellement décrits de manière semblable aux
:ref:`section_tutorials_in_python` car ils sont similaires à ceux que l'on peut
traiter dans l'interface textuelle Python (TUI). Les notations mathématiques
utilisées ci-dessous sont expliquées dans la section :ref:`section_theory`.

Construire un cas d'estimation avec une définition explicite des données
------------------------------------------------------------------------

Cet exemple très simple est un cas de démonstration, et il décrit comment
mettre au point un environnement d'estimation par BLUE de manière à obtenir un
*état estimé par méthode de moindres carrés pondérés* d'un système à partir
d'une observation de l'état et d'une connaissance *a priori* (ou ébauche) de
cet état. En d'autres termes, on cherche l'intermédiaire pondéré entre les
vecteurs d'observation et d'ébauche. Toutes les valeurs numériques de cet
exemple sont arbitraires.

Conditions d'expérience
+++++++++++++++++++++++

On choisit d'opérer dans un espace d'observation à 3 dimensions, i.e on dispose
de 3 mesures simples. La dimension 3 est choisie de manière à restreindre la
taille des objets numériques à entrer explicitement par l'utilisateur, mais le
problème n'est pas dépendant de la dimension et peut être posé en dimension
d'observation de 10, 100, 1000... L'observation :math:`\mathbf{y}^o` vaut 1
dans chaque direction, donc :
::

    Yo = [1 1 1]

L'ébauche :math:`\mathbf{x}^b` de l'état , qui représente une connaissance *a
priori* ou une régularisation mathématique, est choisie comme valant 0 dans
chaque cas, ce qui donne donc :
::

    Xb = [0 0 0]

La mise en oeuvre de l'assimilation de données requiert des informations sur
les covariances d'erreur :math:`\mathbf{R}` et :math:`\mathbf{B}`,
respectivement pour les variables d'erreur d'observation et d'ébauche. On
choisit ici des erreurs décorrélées (c'est-à-dire des matrices diagonales) et
d'avoir la même variance de 1 pour toutes les variables (c'est-à-dire des
matrices identité). On pose donc :
::

    B = R = Id = [1 0 0 ; 0 1 0 ; 0 0 1]

Enfin, on a besoin d'un opérateur d'observation :math:`\mathbf{H}` pour
convertir l'état d'ébauche dans l'espace des observations. Ici, comme les
dimensions d'espace sont les mêmes, on peut choisir l'identité comme opérateur
d'observation :
::

    H = Id = [1 0 0 ; 0 1 0 ; 0 0 1]

Avec de tels choix, l'estimateur "Best Linear Unbiased Estimator" (BLUE) sera
le vecteur moyen entre :math:`\mathbf{y}^o` et :math:`\mathbf{x}^b`, nommé
*analysis*, noté :math:`\mathbf{x}^a`, et valant :
::

    Xa = [0.5 0.5 0.5]

Pour étendre cet exemple, on peut modifier les variances représentées par
:math:`\mathbf{B}` ou :math:`\mathbf{R}` indépendamment, et l'analyse
:math:`\mathbf{x}^a` se déplacera vers :math:`\mathbf{y}^o` ou vers
:math:`\mathbf{x}^b`, en proportion inverse des variances dans
:math:`\mathbf{B}` et :math:`\mathbf{R}`. Comme autre extension, on peut aussi
dire qu'il est équivalent de rechercher l'analyse à l'aide d'un algorithme de
BLUE ou d'un algorithme de 3DVAR.

Utiliser l'interface graphique (GUI) pour construire le cas ADAO
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

En premier lieu, il faut activer le module ADAO en choisissant le bouton ou le
menu approprié de module de SALOME, et on voit :

  .. _adao_activate2:
  .. image:: images/adao_activate.png
    :align: center
    :width: 100%
  .. centered::
    **Activation du module ADAO dans SALOME**

Choisir le bouton "*Nouveau*" dans cette fenêtre. On obtient directement
l'interface de l'éditeur intégré de cas pour la définition de variables, en
même temps que l'"*Arbre d'étude*" de SALOME. On peut alors choisir le bouton
"*Nouveau*" |eficas_new| pour créer un nouveau cas ADAO, et on voit :

  .. _adao_viewer:
  .. image:: images/adao_viewer.png
    :align: center
    :width: 100%
  .. centered::
    **L'éditeur intégré pour la définition de cas dans le module ADAO**

Ensuite, il faut remplir les variables pour construire le cas ADAO en utilisant
les conditions d'expérience décrites ci-dessus. L'ensemble des informations
techniques données au-dessus sont à insérer directement dans la définition du
cas ADAO, en utilisant le type *String* pour chaque variable. Lorsque la
définition du cas est prête, il faut l'enregistrer comme un fichier natif de
type "*JDC (\*.comm)*" à un endroit quelconque dans l'arborescence de
l'utilisateur. Il faut bien se rappeler que d'autres fichiers seront aussi
créés à côté de ce premier, donc il est judicieux de faire un répertoire
spécifique pour ce cas, et d'enregistrer dedans le fichier. Le nom du fichier
apparaît dans la fenêtre de l'"*Arbre d'étude*", sous le menu "*ADAO*". La
définition finale du cas ressemble à :

  .. _adao_jdcexample01:
  .. image:: images/adao_jdcexample01.png
    :align: center
    :width: 100%
  .. centered::
    **Définition des conditions d'expérience choisies pour le cas ADAO**

Pour poursuivre, on a besoin de générer le schéma YACS à partir de la
définition du cas ADAO. Pour faire cela, on peut activer le menu contextuel par
clic droit sur le nom du cas dans la fenêtre de l'"*Arbre d'étude*", et
choisir le sous-menu "*Exporter vers YACS*" (ou le bouton "*Exporter vers
YACS*" |eficas_yacs|) comme ci-dessous :

  .. _adao_exporttoyacs00:
  .. image:: images/adao_exporttoyacs.png
    :align: center
    :scale: 75%
  .. centered::
    **Sous-menu contextuel "*Exporter vers YACS*" pour générer le schéma YACS à partir du cas ADAO**

Cette commande conduit à la génération d'un schéma YACS, à l'activation du
module YACS dans SALOME, et à ouvrir le nouveau schéma dans l'interface
graphique du module YACS [#]_. Après avoir éventuellement réorganisé les noeuds
en utilisant le sous-menu contextuel "*arranger les noeuds locaux*" de la vue
graphique du schéma YACS, on obtient la représentation suivante du schéma ADAO
généré :

  .. _yacs_generatedscheme:
  .. image:: images/yacs_generatedscheme.png
    :align: center
    :width: 100%
  .. centered::
    **Schéma YACS généré à partir du cas ADAO**

Après ce point, toutes les modifications, exécutions et post-processing du
schéma d'assimilation de données seront effectués dans le module YACS. De façon
à vérifier les résultats d'une manière simple, on peut utiliser le noeud
"*UserPostAnalysis*" (ou on crée un nouveau noeud YACS par le sous-menu "*Noeud
de script in-line*" dans la vue graphique de YACS).

Ce noeud de script va récupérer l'analyse issue de l'assimilation de données
depuis le port de sortie "*algoResults*" du bloc de calcul (qui donne accés à
un objet Python SALOME), et va l'afficher à la sortie standard.

Pour obtenir ceci, ce noeud de script doit comporter un port d'entrée de type
"*pyobj*", nommé "*Study*" par exemple, qui doit être relié graphiquement au
port de sortie "*algoResults*" du bloc de calcul. Ensuite, le code pour remplir
le noeud de script est :
::

    Xa = Study.getResults().get("Analysis")[-1]

    print()
    print("Analysis =",Xa)
    print()

Le schéma YACS (initial ou complété) peut être enregistré (en écrasant le
schéma généré si la commande ou le bouton "*Enregistrer*" sont utilisés, ou
sinon avec un nom nouveau par la commande "*Enregistrer sous*"). De manière
pratique, la mise au point d'une telle procédure de post-processing peut être
réalisée dans YACS pour la tester, et ensuite entièrement enregistrée dans un
script Python qui peut être intégré au cas ADAO en utilisant le mot-clé
"*UserPostAnalysis*".

Ensuite, de manière classique dans YACS, le schéma doit être compilé, et être
exécuté. Après la fin de l'exécution, les affichages sur la sortie standard
sont disponibles dans la fenêtre "*fenêtre de sortie de YACS*" (ou "*YACS
Container Log*"), obtenue par clic droit à l'aide du menu contextuel de la
fenêtre "*proc*" du schéma YACS comme montré ci-dessous :

  .. _yacs_containerlog:
  .. image:: images/yacs_containerlog.png
    :align: center
    :width: 100%
  .. centered::
    **Menu YACS de la fenêtre de sortie, et boite de dialogue montrant la sortie**

On vérifie que le résultat est correct en observant si la fenêtre de sortie
contient des informations identiques à la ligne suivante :
::

    Analysis = [0.5, 0.5, 0.5]

comme montré dans l'image précédente.

Pour étendre cet exemple, on peut remarquer que le même problème résolu par un
algorithme de 3DVAR donne le même résultat. Cet algorithme peut être choisi
lors de l'étape de construction du cas ADAO, avant d'entrer dans l'étape YACS.
Le cas ADAO en 3DVAR est entièrement similaire au cas algorithmique du BLUE,
comme montré dans la figure suivante :

  .. _adao_jdcexample02:
  .. image:: images/adao_jdcexample02.png
    :align: center
    :width: 100%
  .. centered::
    **Définir un cas ADAO en 3DVAR est entièrement similaire à un cas en BLUE**

Il n'y a qu'une seule commande qui change, avec "*3DVAR*" dans le champ
"*Algorithm*" à la place de "*Blue*".

Construire un cas d'estimation avec une définition de données externes par scripts
----------------------------------------------------------------------------------

Il est utile d'acquérir une partie ou la totalité des données du cas ADAO
depuis une définition externe, en utilisant des scripts Python pour donner
accès à ces données. À titre d'exemple, on construit ici un cas ADAO présentant
le même dispositif expérimental que dans l'exemple ci-dessus `Construire un cas
d'estimation avec une définition explicite des données`_, mais en utilisant des
données issues d'un unique fichier script Python externe.

En premier lieu, on écrit le fichier script suivant, utilisant des noms
conventionnels pour les variables requises. Ici toutes les variables sont
définies dans le même script, mais l'utilisateur peut choisir de séparer le
fichier en plusieurs autres, ou de mélanger une définition explicite des
données dans l'interface graphique ADAO et une définition implicite dans des
fichiers externes. Le fichier script actuel ressemble à :
::

    import numpy
    #
    # Definition of the Background as a vector
    # ----------------------------------------
    Background = [0, 0, 0]
    #
    # Definition of the Observation as a vector
    # -----------------------------------------
    Observation = "1 1 1"
    #
    # Definition of the Background Error covariance as a matrix
    # ---------------------------------------------------------
    BackgroundError = numpy.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
    #
    # Definition of the Observation Error covariance as a matrix
    # ----------------------------------------------------------
    ObservationError = numpy.matrix("1 0 0 ; 0 1 0 ; 0 0 1")
    #
    # Definition of the Observation Operator as a matrix
    # --------------------------------------------------
    ObservationOperator = numpy.identity(3)

Les noms des variables Python sont obligatoires, de manière à définir les
bonnes variables dans le cas ADAO, mais le script Python peut être plus
conséquent et définir des classes, des fonctions, des accès à des fichiers ou
des bases de données, etc. avec des noms différents. De plus, le fichier
ci-dessus présente différentes manières de définir des vecteurs ou des
matrices, utilisant des listes, des chaînes de caractères (comme dans Numpy ou
Octave), des types vecteur ou matrice de Numpy, et des fonctions spéciales de
Numpy. Toutes ces syntaxes sont valides.

Après avoir enregistré ce script dans un fichier (nommé ici "*script.py*" pour
l'exemple) à un endroit quelconque dans l'arborescence de l'utilisateur, on
utilise l'interface graphique (GUI) pour construire le cas ADAO. La procédure
pour compléter le cas est similaire à celle de l'exemple précédent à part le
fait que, au lieu de choisir l'option "*String*" pour le mot-clé "*FROM*" de
chaque variable, on choisit l'option "*Script*". Cela conduit à une entrée
"*SCRIPT_DATA/SCRIPT_FILE*" dans l'arbre graphique, permettant de choisir un
fichier de la manière suivante :

  .. _adao_scriptentry01:
  .. image:: images/adao_scriptentry01.png
    :align: center
    :width: 100%
  .. centered::
    **Définir une variable d'entrée en utilisant un fichier script externe**

Les autres étapes et résultats sont exactement les mêmes que dans l'exemple
précédent `Construire un cas d'estimation avec une définition explicite des
données`_.

Dans la pratique, cette démarche par scripts est la manière la plus facile pour
récupérer des informations depuis des calculs en ligne ou préalables, depuis
des fichiers statiques, depuis des bases de données ou des flux informatiques,
chacun pouvant être dans ou hors SALOME. Cela permet aussi de modifier aisément
des données d'entrée, par exemple à des fins de débogage ou pour des
traitements répétitifs, et c'est la méthode la plus polyvalente pour paramétrer
les données d'entrée. **Mais attention, la méthodologie par scripts n'est pas
une procédure "sûre", en ce sens que des données erronées ou des erreurs dans
les calculs, peuvent être directement introduites dans l'exécution du cas ADAO.
L'utilisateur doit vérifier avec attention le contenu de ses scripts.**

Ajout de paramètres pour contrôler l'algorithme d'assimilation de données
-------------------------------------------------------------------------

On peut ajouter des paramètres optionnels pour contrôler le calcul de
l'algorithme d'assimilation de données. Ceci se fait en utilisant les
paramètres optionnels dans la commande "*AlgorithmParameters*" de la définition
du cas ADAO, qui est un mot-clé de la commande générale de cas (à choisir entre
"*ASSIMILATION_STUDY*", "*OPTIMIZATION_STUDY*" ou "*REDUCTION_STUDY*"). Ce
mot-clé nécessite une définition explicite des valeurs à partir de valeurs par
défaut, ou à partir d'un dictionnaire Python, contenant des paires clé/valeur.
La liste des paramètres optionnels possibles est donnée dans la section
:ref:`section_reference` et ses sous-sections. On recommande d'utiliser la
définition explicite de valeurs à partir de la liste par défaut de paramètres
optionnels, comme ici avec le "*MaximumNumberOfIterations*" :

  .. _adao_scriptentry02:
  .. image:: images/adao_scriptentry02.png
    :align: center
    :width: 100%
  .. centered::
    **Ajouter des paramètres pour contrôler l'algorithme et les sorties**

Le dictionnaire peut être défini, par exemple, dans un fichier externe de
script Python, en utilisant le nom obligatoire de variable
"*AlgorithmParameters*" pour le dictionnaire. Toutes les clés dans le
dictionnaire sont optionnelles, elles disposent toutes d'une valeur par défaut,
et elles peuvent être présentes sans être utiles. Par exemple :
::

    AlgorithmParameters = {
        "Minimizer" : "LBFGSB", # Recommended
        "MaximumNumberOfIterations" : 10,
        }

Si aucune borne n'est requise sur les variables de contrôle, alors on peut
choisir les algorithmes de minimisation "*BFGS*" ou "*CG*" pour tous les
algorithmes variationnels d'assimilation de données ou d'optimisation. Pour
l'optimisation sous contraintes, l'algorithme "*LBFGSB*" est bien souvent plus
robuste, mais le "*TNC*" est parfois plus performant. De manière générale, le
choix de l'algorithme "*LBFGSB*" est recommandé. Ensuite le script peut être
ajouté au cas ADAO, dans une entrée de type fichier associé au format "*Dict*"
dans le mot-clé "*Parameters*".

Les autres étapes et résultats sont exactement les mêmes que dans l'exemple
précédent `Construire un cas d'estimation avec une définition explicite des
données`_. Le dictionnaire peut aussi être donné directement dans le champ
d'entrée de type chaîne de caractères pour le mot-clé.

Construire un cas complexe avec une définition de données externes par scripts
------------------------------------------------------------------------------

Cet exemple plus complexe et complet peut être considéré comme un cadre de base
pour le traitement des entrées de l'utilisateur, qui doit ensuite être adapté à
chaque application réelle. Néanmoins, les squelettes de fichiers sont
suffisamment généraux pour avoir été utilisés pour des applications variées en
neutronique, mécanique des fluides... Ici, on ne s'intéresse pas aux résultats,
mais plus sur le contrôle de l'utilisateur des entrées et sorties dans un cas
ADAO. Comme précédemment, toutes les valeurs numériques de cet exemple sont
arbitraires.

L'objectif est de configurer les entrées et les sortie d'un problème physique
d'estimation par des scripts externes Python, en utilisant un opérateur
non-linéaire général, en ajoutant un contrôle sur les paramètres et ainsi de
suite... Les scripts complets peuvent être trouvés dans le répertoire des
exemples de squelettes ADAO sous le nom de
"*External_data_definition_by_scripts*".

Conditions d'expérience
+++++++++++++++++++++++

On continue à opérer dans un espace à 3 dimensions, afin de limiter la taille
de l'objet numérique indiqué dans les scripts, mais le problème ne dépend pas
de la dimension.

On choisit un contexte d'expériences jumelles (voir la démarche
:ref:`section_methodology_twin`), en utilisant un état vrai
:math:`\mathbf{x}^t` connu, mais de valeur arbitraire :
::

    Xt = [1 2 3]

L'état d'ébauche :math:`\mathbf{x}^b`, qui représente une connaissance *a
priori* de l'état vrai, est construit comme une perturbation aléatoire
gaussienne de 20% de l'état vrai :math:`\mathbf{x}^t` pour chaque composante,
qui est :
::

    Xb = Xt + normal(0, 20%*Xt)

Pour décrire la matrice des covariances d'erreur d'ébauche :math:`\mathbf{B}`,
on fait comme précédemment l'hypothèse d'erreurs décorrélées (c'est-à-dire, une
matrice diagonale, de taille 3x3 parce-que :math:`\mathbf{x}^b` est de taille
3) et d'avoir la même variance de 0,1 pour toutes les variables. On obtient :
::

    B = 0.1 * diagonal( length(Xb) )

On suppose qu'il existe un opérateur d'observation :math:`\mathbf{H}`, qui peut
être non linéaire. Dans une procédure réelle de recalage ou de problème
inverse, les codes de simulation physique sont intégrés dans l'opérateur
d'observation. On a également besoin de connaître son gradient par rapport à
chaque variable estimée, ce qui est une information rarement connue avec les
codes industriels. Mais on verra plus tard comment obtenir un gradient approché
dans ce cas.

Étant en expériences jumelles, les observations :math:`\mathbf{y}^o` et leur
matrice de covariances d'erreurs :math:`\mathbf{R}` sont générées en utilisant
l'état vrai :math:`\mathbf{x}^t` et l'opérateur d'observation
:math:`\mathbf{H}` :
::

    Yo = H( Xt )

et, avec un écart-type arbitraire de 1% sur chaque composante de l'erreur :
::

    R = 0.0001 * diagonal( length(Yo) )

Toutes les informations requises pour l'estimation par assimilation de données
sont maintenant définies.

Squelettes des scripts décrivant les conditions d'expérience
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

On donne ici les éléments essentiels de chaque script utilisé par la suite pour
construire le cas ADAO. On rappelle que l'utilisation de ces scripts dans de
réels fichiers Python nécessite de définir correctement le chemin de modules ou
des codes importés (même si le module est dans le même répertoire que le
fichier Python qui l'importe. On doit aussi indiquer l'encodage si nécessaire,
etc. Les noms de fichiers indiqués pour les scripts qui suivent sont
arbitraires. Des exemples complets de fichiers scripts sont disponibles dans le
répertoire standard des exemples ADAO.

On définit en premier lieu l'état vrai :math:`\mathbf{x}^t` et une fonction
utiles à la construction de matrices, dans un fichier script Python nommé
``Physical_data_and_covariance_matrices.py`` :
::

    import numpy
    #
    def True_state():
        """
        Arbitrary values and names, as a tuple of two series of same length
        """
        return (numpy.array([1, 2, 3]), ['Para1', 'Para2', 'Para3'])
    #
    def Simple_Matrix( size, diagonal=None ):
        """
        Diagonal matrix, with either 1 or a given vector on the diagonal
        """
        if diagonal is not None:
            S = numpy.diagflat( diagonal )
        else:
            S = numpy.identity(int(size))
        return S

On définit ensuite l'état d'ébauche :math:`\mathbf{x}^b` comme une perturbation
aléatoire de l'état vrai, en ajoutant une *variable ADAO requise* à la fin du
script de définition, de manière à exporter la valeur définie. C'est réalisé
dans un fichier de script Python nommé ``Script_Background_xb.py`` :
::

    from Physical_data_and_covariance_matrices import True_state
    import numpy
    #
    xt, names = True_state()
    #
    Standard_deviation = 0.2*xt # 20% for each variable
    #
    xb = xt + abs(numpy.random.normal(0.,Standard_deviation,size=(len(xt),)))
    #
    # Creating the required ADAO variable
    # -----------------------------------
    Background = list(xb)

De la même manière, on définit la matrice des covariances de l'erreur d'ébauche
:math:`\mathbf{B}` comme une matrice diagonale, de la même longueur de
diagonale que l'ébauche de la valeur vraie, en utilisant la fonction d'aide
déjà définie. C'est réalisé dans un fichier script Python nommé
``Script_BackgroundError_B.py`` :
::

    from Physical_data_and_covariance_matrices import True_state, Simple_Matrix
    #
    xt, names = True_state()
    #
    B = 0.1 * Simple_Matrix( size = len(xt) )
    #
    # Creating the required ADAO variable
    # -----------------------------------
    BackgroundError = B

Pour poursuivre, on a besoin de l'opérateur d'observation :math:`\mathbf{H}`
comme une fonction de l'état. Il est ici défini dans un fichier externe nommé
``"Physical_simulation_functions.py"``, qui doit contenir une fonction appelée
``"DirectOperator"``. Cette fonction est une fonction utilisateur, représentant
de manière programmée l'opérateur :math:`\mathbf{H}`. On suppose que cette
fonction est donnée par l'utilisateur. Un squelette simple est donné ici par
facilité :
::

    def DirectOperator( XX ):
        import numpy
        """ Direct non-linear simulation operator """
        #
        # --------------------------------------> EXAMPLE TO BE REMOVED
        HX = 1. * numpy.ravel( XX )             # EXAMPLE TO BE REMOVED
        # --------------------------------------> EXAMPLE TO BE REMOVED
        #
        return HX

On n'a pas besoin des opérateurs linéaires associés ``"TangentOperator"`` et
``"AdjointOperator"`` car ils vont être approximés en utilisant les capacités
d'ADAO. Des informations détaillées sur ces opérateurs peuvent être trouvées
dans les :ref:`section_ref_operator_requirements`.

On insiste sur le fait que ces opérateurs non-linéaire ``"DirectOperator"``,
linéaire tangent ``"TangentOperator"`` et linéaire adjoint
``"AdjointOperator"`` proviennent de la connaissance de la physique, incluant
le code de simulation de référence physique, et doivent être soigneusement mis
au point par l'utilisateur de l'assimilation de données ou de l'optimisation.
Les erreurs de simulation ou d'usage des opérateurs ne peuvent pas être
détectées ou corrigées uniquement par l'environnement ADAO d'assimilation de
données et d'optimisation.

Dans cet environnement d'expériences jumelles, l'observation
:math:`\mathbf{y}^o` et sa matrice des covariances d'erreur :math:`\mathbf{R}`
peuvent être générées. C'est réalisé dans deux fichiers de script Python, le
premier étant nommé ``Script_Observation_yo.py`` :
::

    from Physical_data_and_covariance_matrices import True_state
    from Physical_simulation_functions import DirectOperator
    #
    xt, noms = True_state()
    #
    yo = DirectOperator( xt )
    #
    # Creating the required ADAO variable
    # -----------------------------------
    Observation = list(yo)

et le second nommé ``Script_ObservationError_R.py`` :
::

    from Physical_data_and_covariance_matrices import True_state, Simple_Matrix
    from Physical_simulation_functions import DirectOperator
    #
    xt, names = True_state()
    #
    yo = DirectOperator( xt )
    #
    R  = 0.0001 * Simple_Matrix( size = len(yo) )
    #
    # Creating the required ADAO variable
    # -----------------------------------
    ObservationError = R

Comme dans les exemples précédents, il peut être utile de définir certains
paramètres pour l'algorithme d'assimilation de données. Par exemple, si on
utilise l'algorithme standard de "*3DVAR*", les paramètres suivants peuvent être
définis dans un fichier de script Python nommé
``Script_AlgorithmParameters.py`` :
::

    # Creating the required ADAO variable
    # -----------------------------------
    AlgorithmParameters = {
        "Minimizer" : "LBFGSB",           # Recommended
        "MaximumNumberOfIterations" : 15, # Number of global iterative steps
        "Bounds" : [
            [ None, None ],               # Bound on the first parameter
            [ 0., 4. ],                   # Bound on the second parameter
            [ 0., None ],                 # Bound on the third parameter
            ],
        "StoreSupplementaryCalculations" : [
            "CurrentState",
            "CostFunctionJ",
            ],
    }

Enfin, il est courant de post-traiter les résultats, en les récupérant aprés la
phase d'assimilation de données de manière à les analyser, les afficher ou les
représenter. Cela nécessite d'utiliser un fichier script Python intermédiaire de
manière à extraire ces résultats à la fin de la procédure d'assimilation de
données ou d'optimisation. L'exemple suivant de fichier script Python, nommé
``Script_UserPostAnalysis.py``, illustre le fait :
::

    from Physical_data_and_covariance_matrices import True_state
    import numpy
    #
    xt, names   = True_state()
    xa          = ADD.get("Analysis")[-1]
    x_series    = ADD.get("CurrentState")[:]
    J           = ADD.get("CostFunctionJ")[:]
    #
    # Verifying the results by printing
    # ---------------------------------
    print()
    print("xt = %s"%xt)
    print("xa = %s"%numpy.array(xa))
    print()
    for i in range( len(x_series) ):
        print("Etape %2i : J = %.5e  et  X = %s"%(i, J[i], x_series[i]))
    print()

Finalement, on obtient la description de l'ensemble des conditions
d'expériences à travers la série de fichiers listée ici :

#.      ``Physical_data_and_covariance_matrices.py``
#.      ``Physical_simulation_functions.py``
#.      ``Script_AlgorithmParameters.py``
#.      ``Script_BackgroundError_B.py``
#.      ``Script_Background_xb.py``
#.      ``Script_ObservationError_R.py``
#.      ``Script_Observation_yo.py``
#.      ``Script_UserPostAnalysis.py``

On insiste ici sur le fait que tous ces scripts sont écrits par l'utilisateur et
ne peuvent être testés automatiquement par ADAO. Ainsi, l'utilisateur est tenu
de vérifier les scripts (et en particulier leurs entrées/sorties) afin de
limiter les difficultés de débogage. On rappelle que : **la méthodologie par
scripts n'est pas une procédure "sûre", en ce sens que des données erronées ou
des erreurs dans les calculs, peuvent être directement introduites dans
l'exécution du schéma YACS.**

Construire le cas avec une définition de données externes par scripts
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Tous ces scripts peuvent ensuite être utilisés pour définir le cas ADAO avec une
définition de données externes par des fichiers de script Python. Cela se
réalise de manière tout à fait similaire à la méthode décrite dans la partie
précédente `Construire un cas d'estimation avec une définition de données
externes par scripts`_. Pour chaque variable à définir, on sélectionne l'option
"*Script*"  du mot-clé "*FROM*", ce qui conduit à une entrée
"*SCRIPT_DATA/SCRIPT_FILE*" dans l'arbre graphique. Pour le mot-clé
"*ObservationOperator*", on choisit la forme "*ScriptWithOneFunction*" et on
conserve la valeur par défaut de l'incrément différentiel.

Les autres étapes pour construire le cas ADAO sont exactement les mêmes que dans
la partie précédente `Construire un cas d'estimation avec une définition
explicite des données`_.

En utilisant l'opérateur linéaire simple :math:`\mathbf{H}` du fichier script
Python ``Physical_simulation_functions.py`` disponible dans le répertoire
standard des exemples, les résultats ressemblent à (cela peut dépendre du
système) :
::

    xt = [1 2 3]
    xa = [ 1.000014    2.000458  3.000390]

    Etape  0 : J = 1.81750e+03  et  X = [1.014011, 2.459175, 3.390462]
    Etape  1 : J = 1.81750e+03  et  X = [1.014011, 2.459175, 3.390462]
    Etape  2 : J = 1.79734e+01  et  X = [1.010771, 2.040342, 2.961378]
    Etape  3 : J = 1.79734e+01  et  X = [1.010771, 2.040342, 2.961378]
    Etape  4 : J = 1.81909e+00  et  X = [1.000826, 2.000352, 3.000487]
    Etape  5 : J = 1.81909e+00  et  X = [1.000826, 2.000352, 3.000487]
    Etape  6 : J = 1.81641e+00  et  X = [1.000247, 2.000651, 3.000156]
    Etape  7 : J = 1.81641e+00  et  X = [1.000247, 2.000651, 3.000156]
    Etape  8 : J = 1.81569e+00  et  X = [1.000015, 2.000432, 3.000364]
    Etape  9 : J = 1.81569e+00  et  X = [1.000015, 2.000432, 3.000364]
    Etape 10 : J = 1.81568e+00  et  X = [1.000013, 2.000458, 3.000390]
    ...

L'état au premier pas est l'état d'ébauche :math:`\mathbf{x}^b` généré
aléatoirement. Au cours du calcul, ces affichages sur la sortie standard sont
disponibles dans la fenêtre "*fenêtre de sortie de YACS*", que l'on obtient par
clic droit sur la fenêtre "*proc*" du schéma YACS exécuté.

.. [#] Pour de plus amples informations sur YACS, voir le *module YACS* et son aide intégrée disponible dans le menu principal *Aide* de l'environnement SALOME.
