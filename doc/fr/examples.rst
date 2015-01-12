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

.. _section_examples:

================================================================================
**[DocU]** Tutoriaux sur l'utilisation du module ADAO
================================================================================

.. |eficas_new| image:: images/eficas_new.png
   :align: middle
   :scale: 50%
.. |eficas_save| image:: images/eficas_save.png
   :align: middle
   :scale: 50%
.. |eficas_saveas| image:: images/eficas_saveas.png
   :align: middle
   :scale: 50%
.. |eficas_yacs| image:: images/eficas_yacs.png
   :align: middle
   :scale: 50%

Cette section pr�sente quelques exemples d'utilisation du module ADAO dans
SALOME. Le premier montre comment construire un cas simple d'assimilation de
donn�es d�finissant explicitement toutes les donn�es d'entr�e requises � travers
l'interface graphique d'�dition (GUI). Le second montre, sur le m�me cas,
comment d�finir les donn�es d'entr�e � partir de sources externes � travers des
scripts. On pr�sente ici toujours des scripts Python car ils sont directement
ins�rables dans les noeuds de script de YACS, mais les fichiers externes peuvent
utiliser d'autres langages.

Les notations math�matiques utilis�es ci-dessous sont expliqu�es dans la section
:ref:`section_theory`.

Construire un cas d'estimation avec une d�finition explicite des donn�es
------------------------------------------------------------------------

Cet exemple simple est un cas de d�monstration, et il d�crit comment mettre au
point un environnement d'estimation par BLUE de mani�re � obtenir un *�tat
estim� par m�thode de moindres carr�s pond�r�s* d'un syst�me � partir d'une
observation de l'�tat et d'une connaissance *a priori* (ou �bauche) de cet �tat.
En d'autres termes, on cherche l'interm�diaire pond�r� entre les vecteurs
d'observation et d'�bauche. Toutes les valeurs num�riques de cet exemple sont
arbitraires.

Conditions d'exp�rience
+++++++++++++++++++++++

On choisit d'op�rer dans un espace � 3 dimensions. La 3D est choisie de mani�re
� restreindre la taille des objets num�riques � entrer explicitement par
l'utilisateur, mais le probl�me n'est pas d�pendant de la dimension et peut �tre
pos� en dimension 10, 100, 1000... L'observation :math:`\mathbf{y}^o` vaut 1
dans chaque direction, donc::

    Yo = [1 1 1]

L'�bauche :math:`\mathbf{x}^b` de l'�tat , qui repr�sente une connaissance *a
priori* ou une r�gularisation math�matique, vaut 0 dans chaque direction, ce qui
donne donc::

    Xb = [0 0 0]

La mise en oeuvre de l'assimilation de donn�es requiert des informations sur les
covariances d'erreur :math:`\mathbf{R}` et :math:`\mathbf{B}`, respectivement
pour les variables d'observation et d'�bauche. On choisit ici des erreurs
d�corr�l�es (c'est-�-dire des matrices diagonales) et d'avoir la m�me variance
de 1 pour toutes les variables (c'est-�-dire des matrices identit�). On pose
donc::

    B = R = [1 0 0 ; 0 1 0 ; 0 0 1]

Enfin, on a besoin d'un op�rateur d'observation :math:`\mathbf{H}` pour
convertir l'�tat d'�bauche dans l'espace des observations. Ici, comme les
dimensions d'espace sont les m�mes, on peut choisir l'identit� comme op�rateur
d'observation::

    H = [1 0 0 ; 0 1 0 ; 0 0 1]

Avec de tels choix, l'estimateur "Best Linear Unbiased Estimator" (BLUE) sera le
vecteur moyen entre :math:`\mathbf{y}^o` et :math:`\mathbf{x}^b`, nomm�
*analysis*, not� :math:`\mathbf{x}^a`, et valant::


    Xa = [0.5 0.5 0.5]

Pour �tendre cet exemple, on peut modifier les variances repr�sent�es par
:math:`\mathbf{B}` ou :math:`\mathbf{R}` ind�pendamment, et l'analyse
:math:`\mathbf{x}^a` se d�placera vers :math:`\mathbf{y}^o` ou vers
:math:`\mathbf{x}^b`, en proportion inverse des variances dans
:math:`\mathbf{B}` et :math:`\mathbf{R}`. Comme autre extension, on peut aussi
dire qu'il est �quivalent de rechercher l'analyse � l'aide d'un algorithme de
BLUE ou d'un algorithme de 3DVAR.

Utiliser l'interface graphique (GUI) pour construire le cas ADAO
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

En premier lieu, il faut activer le module ADAO en choisissant le bouton ou le
menu appropri� de module de SALOME, et on voit :

  .. _adao_activate2:
  .. image:: images/adao_activate.png
    :align: center
    :width: 100%
  .. centered::
    **Activation du module ADAO dans SALOME**

Choisir le bouton "*Nouveau*" dans cette fen�tre. On obtient directement
l'interface EFICAS pour la d�finition de variables, en m�me temps que l'"*Arbre
d'�tude*" de SALOME. On peut alors choisir le bouton "*Nouveau*" |eficas_new|
pour cr�er un nouveau cas ADAO, et on voit :

  .. _adao_viewer:
  .. image:: images/adao_viewer.png
    :align: center
    :width: 100%
  .. centered::
    **L'�diteur EFICAS pour la d�finition de cas dans le module ADAO**

Ensuite, il faut remplir les variables pour construire le cas ADAO en utilisant
les conditions d'exp�rience d�crites ci-dessus. L'ensemble des informations
techniques donn�es au-dessus sont � ins�rer directement dans la d�finition du
cas ADAO, en utilisant le type *String* pour toutes les variables. Lorsque la
d�finition du cas est pr�te, il faut l'enregistrer comme un fichier natif de ype
"*JDC (\*.comm)*" � un endroit quelconque dans l'arborescence de l'utilisateur.
Il faut bien se rappeler que d'autres fichiers seront aussi cr��s � c�t� de ce
premier, donc il est judicieux de faire un r�pertoire sp�cifique pour ce cas, et
d'enregistrer dedans le fichier. Le nom du fichier appara�t dans la fen�tre de
l'"*Arbre d'�tude*", sous le menu "*ADAO*". La d�finition finale du cas
ressemble � :

  .. _adao_jdcexample01:
  .. image:: images/adao_jdcexample01.png
    :align: center
    :width: 100%
  .. centered::
    **D�finition des conditions d'exp�rience choisies pour le cas ADAO**

Pour poursuivre, on a besoin de g�n�rer le sch�ma YACS � partir de la d�finition
du cas ADAO. Pour faire cela, on peut activer le menu contextuel par click droit
sur le nom du cas dans la fen�tre de l'"*Arbre d'�tude*", et choisir le
sous-menu "*Exporter vers YACS*" (ou le bouton "*Exporter vers YACS*"
|eficas_yacs|) comme ci-dessous :

  .. _adao_exporttoyacs00:
  .. image:: images/adao_exporttoyacs.png
    :align: center
    :scale: 75%
  .. centered::
    **Sous-menu contextuel "*Exporter vers YACS*" pour g�n�rer le sch�ma YACS � partir du cas ADAO**

Cette commande conduit � la g�n�ration d'un sch�ma YACS, � l'activation du module
YACS dans SALOME, et � ouvrir le nouveau sch�ma dans l'interface graphique du
module YACS [#]_. Apr�s avoir �ventuellement r�organis� les noeuds en utilisant
le sous-menu contextuel "*arranger les noeuds locaux*" de la vue graphique du
sch�ma YACS, on obtient la repr�sentation suivante du sch�ma ADAO g�n�r� :

  .. _yacs_generatedscheme:
  .. image:: images/yacs_generatedscheme.png
    :align: center
    :width: 100%
  .. centered::
    **Sch�ma YACS g�n�r� � partir du cas ADAO**

Apr�s ce point, toutes les modifications, ex�cutions et post-processing du
sch�ma d'assimilation de donn�es seront effectu�s dans le module YACS. De
mani�re � v�rifier les r�sultats d'une mani�re simple, on cr�e ici un nouveau
noeud YACS en utilisant le sous-menu "*Noeud de script in-line*" dans la vue
graphique de YACS, et on le nomme "*PostProcessing*".

Ce noeud de script va r�cup�rer l'analyse issue de l'assimilation de donn�es
depuis le port de sortie "*algoResults*" du bloc de calcul (qui donne acc�s � un
objet Python SALOME), et va l'afficher � la sortie standard.

Pour obtenir ceci, ce noeud de script doit comporter un port d'entr�e de type
"*pyobj*", nomm� "*results*" par exemple, qui doit �tre reli� graphiquement au
port de sortie "*algoResults*" du bloc de calcul. Ensuite, le code pour remplir
le noeud de script est::

    Xa = results.ADD.get("Analysis")[-1]

    print
    print "Analysis =",Xa
    print

Le sch�ma YACS compl�t� peut �tre enregistr� (en �crasant le sch�ma g�n�r� si la
commande ou le bouton "*Enregistrer*" sont utilis�s, ou sinon avec un nom
nouveau par la commande "*Enregistrer sous*"). De mani�re pratique, la mise au
point d'une telle proc�dure de post-processing peut �tre r�alis�e dans YACS pour
la tester, et ensuite enti�rement enregistr�e dans un script Python qui peut
�tre int�gr� au cas ADAO en utilisant le mot-cl� "*UserPostAnalysis*".

Ensuite, de mani�re classique dans YACS, le sch�ma doit �tre compil�, et ensuite
�tre ex�cut�. Apr�s la fin de l'ex�cution, les affichages sur la sortie standard
sont disponibles dans la fen�tre "*fen�tre de sortie de YACS*" (ou "*YACS
Container Log*"), obtenue par clic droit � l'aide du menu contextuel de la
fen�tre "*proc*" du sch�ma YACS comme montr� ci-dessous:

  .. _yacs_containerlog:
  .. image:: images/yacs_containerlog.png
    :align: center
    :width: 100%
  .. centered::
    **Menu YACS de la fen�tre de sortie, et boite de dialogue montrant la sortie**

On v�rifie que le r�sultat est correct en observant si la fen�tre de sortie
contient la ligne suivante::

    Analysis = [0.5, 0.5, 0.5]

comme montr� dans l'image pr�c�dente.

Pour �tendre cet exemple, on peut remarquer que le m�me probl�me r�solu par un
algorithme de 3DVAR donne le m�me r�sultat. Cet algorithme peut �tre choisi lors
de l'�tape de construction du cas ADAO, avant d'entrer dans l'�tape YACS. Le cas
ADAO en 3DVAR est enti�rement similaire au cas algorithmique du BLUE, comme
montr� dans la figure suivante:

  .. _adao_jdcexample02:
  .. image:: images/adao_jdcexample02.png
    :align: center
    :width: 100%
  .. centered::
    **D�finir un cas ADAO en 3DVAR est enti�rement similaire � un cas en BLUE**

Il n'y a qu'une seule commande qui change, avec "*3DVAR*" dans le champ
"*Algorithm*" � la place de "*Blue*".

Construire un cas d'estimation avec une d�finition de donn�es externes par scripts
----------------------------------------------------------------------------------

Il est utile d'acqu�rir une partie ou la totalit� des donn�es depuis une
d�finition externe, en utilisant des scripts Python pour donner acc�s � ces
donn�es. � titre d'exemple, on construit ici un cas ADAO pr�sentant le m�me
dispositif exp�rimental que dans l'exemple ci-dessus `Construire un cas
d'estimation avec une d�finition explicite des donn�es`_, mais en utilisant des
donn�es issues d'un unique fichier script Python externe.

En premier lieu, on �crit le fichier script suivant, utilisant des noms
conventionnels pour les variables requises. Ici toutes les variables sont
d�finies dans le m�me script, mais l'utilisateur peut choisir de s�parer le
fichier en plusieurs autres, ou de m�langer une d�finition explicite des donn�es
dans l'interface graphique ADAO et une d�finition implicite dans des fichiers
externes. Le fichier script actuel ressemble �::

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

Les noms des variables Python sont obligatoires, de mani�re � d�finir les bonnes
variables dans le cas, mais le script Python peut �tre plus cons�quent et
d�finir des classes, des fonctions, des acc�s � des fichiers ou des bases de
donn�es, etc. avec des noms diff�rents. De plus, le fichier ci-dessus pr�sente
diff�rentes mani�res de d�finir des vecteurs ou des matrices, utilisant des
listes, des cha�nes de caract�res (comme dans Numpy ou Octave), des types
vecteur ou matrice de Numpy, et des fonctions sp�ciales de Numpy. Toutes ces
syntaxes sont valides.

Apr�s avoir enregistr� ce script dans un fichier (nomm� ici "*script.py*" pour
l'exemple) � un endroit quelconque dans l'arborescence de l'utilisateur, on
utilise l'interface graphique (GUI) pour construire le cas ADAO. La proc�dure
pour compl�ter le cas est similaire � celle de l'exemple pr�c�dent � part le
fait que, au lieu de choisir l'option "*String*" pour le mot-cl� "*FROM*" de
chaque variable, on choisit l'option "*Script*". Cela conduit � une entr�e
"*SCRIPT_DATA/SCRIPT_FILE*" dans l'arbre graphique, permettant de choisir un
fichier de la mani�re suivante:

  .. _adao_scriptentry01:
  .. image:: images/adao_scriptentry01.png
    :align: center
    :width: 100%
  .. centered::
    **D�finir une variable d'entr�e en utilisant un fichier script externe**

Les autres �tapes et r�sultats sont exactement les m�mes que dans l'exemple
pr�c�dent `Construire un cas d'estimation avec une d�finition explicite des
donn�es`_.

Dans la pratique, cette d�marche par scripts est la mani�re la plus facile pour
r�cup�rer des information depuis des calculs en ligne ou pr�alables, depuis des
fichiers statiques, depuis des bases de donn�es ou des flux informatiques,
chacun pouvant �tre dans ou hors SALOME. Cela permet aussi de modifier ais�ment
des donn�es d'entr�e, par exemple � des fin de d�bogage ou pour des traitements
r�p�titifs, et c'est la m�thode la plus polyvalente pour param�trer les donn�es
d'entr�e. **Mais attention, la m�thodologie par scripts n'est pas une proc�dure
"s�re", en ce sens que des donn�es erron�es ou des erreurs dans les calculs,
peuvent �tre directement introduites dans l'ex�cution du sch�ma YACS.
L'utilisateur doit v�rifier avec attention le contenu de ses scripts.**

Ajout de param�tres pour contr�ler l'algorithme d'assimilation de donn�es
-------------------------------------------------------------------------

On peut ajouter des param�tres optionnels pour contr�ler le calcul de
l'algorithme d'assimilation de donn�es. Ceci se fait en utilisant le mot-cl�
"*AlgorithmParameters*" dans la d�finition du cas ADAO, qui est un mot-cl� de la
commande g�n�rale "*ASSIMILATION_STUDY*". Ce mot-cl� n�cessite un dictionnaire
Python, contenant des paires cl�/valeur. La liste des param�tres optionnels
possibles sont donn�s dans la section :ref:`section_reference`.

Le dictionnaire doit �tre d�fini, par exemple, dans un fichiers externe de
script Python, en utilisant le nom obligatoire de variable
"*AlgorithmParameters*" pour le dictionnaire. Toutes les cl�s dans le
dictionnaire sont optionnelles, elles disposent toutes d'une valeur par d�faut,
et elles peuvent �tre pr�sentes sans �tre utiles. Par exemple::

    AlgorithmParameters = {
        "Minimizer" : "CG", # Choix possible : "LBFGSB", "TNC", "CG", "BFGS"
        "MaximumNumberOfSteps" : 10,
        }

Si aucune borne n'est requise sur les variables de contr�le, alors on peut
choisir les algorithmes de minimisation "*BFGS*" ou "*CG*" pour tous les
algorithmes variationnels d'assimilation de donn�es ou d'optimisation. Pour
l'optimisation sous contraintes, l'algorithme "*LBFGSB*" est bien souvent plus
robuste, mais le "*TNC*" est parfois plus performant.

Ensuite le script peut �tre ajout� au cas ADAO, dans une entr�e de type fichier
pour le mot-cl� "*AlgorithmParameters*", de la mani�re suivante:

  .. _adao_scriptentry02:
  .. image:: images/adao_scriptentry02.png
    :align: center
    :width: 100%
  .. centered::
    **Ajouter des param�tres pour contr�ler l'algorithme et les sorties**

Les autres �tapes et r�sultats sont exactement les m�mes que dans l'exemple
pr�c�dent `Construire un cas d'estimation avec une d�finition explicite des
donn�es`_. Le dictionnaire peut aussi �tre donn� directement dans le champ
d'entr�e de type cha�ne de caract�res pour le mot-cl�.

Construire un cas complexe avec une d�finition de donn�es externes par scripts
------------------------------------------------------------------------------

Cet exemple plus complexe et complet peut �tre consid�r� comme un cadre de base
pour le traitement des entr�es de l'utilisateur, qui doit ensuite �tre adapt� �
chaque application r�elle. N�anmoins, les squelettes de fichiers sont
suffisamment g�n�raux pour avoir �t� utilis�s pour des applications vari�es en
neutronique, m�canique des fluides... Ici, on ne s'int�resse pas aux r�sultats,
mais plus sur le contr�le de l'utilisateur des entr�es et sorties dans un cas
ADAO. Comme pr�c�demment, toutes les valeurs num�riques de cet exemple sont
arbitraires.

L'objectif est de configurer les entr�es et les sortie d'un probl�me physique
d'estimation par des scripts externes Python, en utilisant un op�rateur
non-lin�aire g�n�ral, en ajoutant un contr�le sur les param�tres et ainsi de
suite... Les scripts complets peuvent �tre trouv�s dans le r�pertoire des
exemples de squelettes ADAO sous le nom de
"*External_data_definition_by_scripts*".

Conditions d'exp�rience
+++++++++++++++++++++++

On continue � op�rer dans un espace � 3 dimensions, afin de limiter la taille de
l'objet num�rique indiqu� dans les scripts, mais le probl�me ne d�pend pas de la
dimension.

On choisit un contexte d'exp�riences jumelles, en utilisant un �tat vrai
:math:`\mathbf{x}^t` connu, mais de valeur arbitraire::

    Xt = [1 2 3]

L'�tat d'�bauche :math:`\mathbf{x}^b`, qui repr�sentent une connaissance *a
priori* de l'�tat vrai, est construit comme une perturbation al�atoire
gaussienne de 20% de l'�tat vrai :math:`\mathbf{x}^t` pour chaque composante,
qui est::

    Xb = Xt + normal(0, 20%*Xt)

Pour d�crire la matrice des covariances d'erreur d'�bauche math:`\mathbf{B}`, on
fait comme pr�c�demment l'hypoth�se d'erreurs d�corr�l�es (c'est-�-dire, une
matrice diagonale, de taille 3x3 parce-que :math:`\mathbf{x}^b` est de taille 3)
et d'avoir la m�me variance de 0,1 pour toutes les variables. On obtient::

    B = 0.1 * diagonal( length(Xb) )

On suppose qu'il existe un op�rateur d'observation :math:`\mathbf{H}`, qui peut
�tre non lin�aire. Dans une proc�dure r�elle de recalage ou de probl�me inverse,
les codes de simulation physique sont int�gr�s dans l'op�rateur d'observation.
On a �galement besoin de conna�tre son gradient par rapport � chaque variable
estim�e, ce qui est une information rarement connu avec les codes industriels.
Mais on verra plus tard comment obtenir un gradient approch� dans ce cas.

�tant en exp�riences jumelles, les observations :math:`\mathbf{y}^o` et leur
matrice de covariances d'erreurs :math:`\mathbf{R}` sont g�n�r�es en utilisant
l'�tat vrai :math:`\mathbf{x}^t` et l'op�rateur d'observation
:math:`\mathbf{H}`::

    Yo = H( Xt )

et, avec un �cart-type arbitraire de 1% sur chaque composante de l'erreur::

    R = 0.0001 * diagonal( lenght(Yo) )

Toutes les informations requises pour l'estimation par assimilation de donn�es
sont maintenant d�finies.

Squelettes des scripts d�crivant les conditions d'exp�rience
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

On donne ici les �l�ments essentiels de chaque script utilis� par la suite pour
construire le cas ADAO. On rappelle que l'utilisation de ces scripts dans de
r�els fichiers Python n�cessite de d�finir correctement le chemin de modules ou
des codes import�s (m�me si le module est dans le m�me r�pertoire que le fichier
Python qui l'importe. On indique le chemin � renseigner en utilisant la mention
``"# INSERT PHYSICAL SCRIPT PATH"``), l'encodage si n�cessaire, etc. Les noms de
fichiers indiqu�s pour les scripts qui suivent sont arbitraires. Des exemples
complets de fichiers scripts sont disponibles dans le r�pertoire standard des
exemples ADAO.

On d�finit en premier lieu l'�tat vrai :math:`\mathbf{x}^t` et une fonction
utiles � la construction de matrices, dans un fichier script Python nomm�
``Physical_data_and_covariance_matrices.py``::

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
            S = numpy.diag( diagonal )
        else:
            S = numpy.matrix(numpy.identity(int(size)))
        return S

On d�finit ensuite l'�tat d'�bauche :math:`\mathbf{x}^b` comme une perturbation
al�atoire de l'�tat vrai, en ajoutant une *variable ADAO requise* � la fin du
script de d�finition, de mani�re � exporter la valeur d�finie. C'est r�alis�
dans un fichier de script Python nomm� ``Script_Background_xb.py``::

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
    # ------------------------------------
    Background = list(xb)

De la m�me mani�re, on d�finit la matrice des covariances de l'erreur d'�bauche
:math:`\mathbf{B}` comme une matrice diagonale, de la m�me longueur de diagonale
que l'�bauche de la valeur vraie, en utilisant la fonction d'aide d�j� d�finie.
C'est r�alis� dans un fichier script Python nomm�
``Script_BackgroundError_B.py``::

    from Physical_data_and_covariance_matrices import True_state, Simple_Matrix
    #
    xt, names = True_state()
    #
    B = 0.1 * Simple_Matrix( size = len(xt) )
    #
    # Creating the required ADAO variable
    # -----------------------------------
    BackgroundError = B

Pour poursuivre, on a besoin de l'op�rateur d'observation :math:`\mathbf{H}`
comme une fonction de l'�tat. Il est ici d�fini dans un fichier externe nomm� 
``"Physical_simulation_functions.py"``, qui doit contenir une fonction appel�e
``"DirectOperator"``. Cette fonction est une une fonction utilisateur,
repr�sentant de mani�re programm�e l'op�rateur :math:`\mathbf{H}`. On suppose
que cette fonction est donn�e par l'utilisateur. Un squelette simple est donn�
ici par facilit�::

    def DirectOperator( XX ):
        """ Direct non-linear simulation operator """
        #
        # --------------------------------------> EXAMPLE TO BE REMOVED
        if type(XX) is type(numpy.matrix([])):  # EXAMPLE TO BE REMOVED
            HX = XX.A1.tolist()                 # EXAMPLE TO BE REMOVED
        elif type(XX) is type(numpy.array([])): # EXAMPLE TO BE REMOVED
            HX = numpy.matrix(XX).A1.tolist()   # EXAMPLE TO BE REMOVED
        else:                                   # EXAMPLE TO BE REMOVED
            HX = XX                             # EXAMPLE TO BE REMOVED
        # --------------------------------------> EXAMPLE TO BE REMOVED
        #
        return numpy.array( HX )

On n'a pas besoin des op�rateurs lin�aires associ�s ``"TangentOperator"`` et
``"AdjointOperator"`` car ils vont �tre approxim�s en utilisant les capacit�s
d'ADAO.

On insiste sur le fait que ces op�rateurs non-lin�aire ``"DirectOperator"``,
lin�aire tangent ``"TangentOperator"`` et lin�aire adjoint ``"AdjointOperator"``
proviennent de la connaissance de la physique, incluant le code de simulation de
r�f�rence physique, et doivent �tre soigneusement mis au point par l'utilisateur
de l'assimilation de donn�es ou de l'optimisation. Les erreurs de simulation ou
d'usage des op�rateurs ne peuvent pas �tre d�tect�s ou corrig�s par
l'environnement seul ADAO d'assimilation de donn�es et d'optimisation.

Dans cet environnement d'exp�riences jumelles, l'observation
:math:`\mathbf{y}^o` et sa matrice des covariances d'erreur :math:`\mathbf{R}`
peuvent �tre g�n�r�es. C'est r�alis� dans deux fichiers de script Python, le
premier �tant nomm� ``Script_Observation_yo.py``::

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

et le second nomm� ``Script_ObservationError_R.py``::

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

Comme dans les exemples pr�c�dents, il peut �tre utile de d�finir certains
param�tres pour l'algorithme d'assimilation de donn�es. Par exemple, si on
utilise l'algorithme standard de "*3DVAR*", les param�tres suivants peuvent �tre
d�finis dans un fichier de script Python nomm�
``Script_AlgorithmParameters.py``::

    # Creating the required ADAO variable
    # -----------------------------------
    AlgorithmParameters = {
        "Minimizer" : "TNC",         # Possible : "LBFGSB", "TNC", "CG", "BFGS"
        "MaximumNumberOfSteps" : 15, # Number of global iterative steps
        "Bounds" : [
            [ None, None ],          # Bound on the first parameter
            [ 0., 4. ],              # Bound on the second parameter
            [ 0., None ],            # Bound on the third parameter
            ],
    }

Enfin, il est courant de post-traiter les r�sultats, en les r�cup�rant apr�s la
phase d'assimilation de donn�es de mani�re � les analyser, les afficher ou les
repr�senter. Cela n�cessite d'utiliser un fichier script Python interm�diaire de
mani�re � extraire ces r�sultats � la fin de la proc�dure d'assimilation de
donn�es ou d'optimisation. L'exemple suivant de fichier script Python, nomm�
``Script_UserPostAnalysis.py``, illustre le fait::

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
    print
    print "xt = %s"%xt
    print "xa = %s"%numpy.array(xa)
    print
    for i in range( len(x_series) ):
        print "Etape %2i : J = %.5e  et  X = %s"%(i, J[i], x_series[i])
    print

Finalement, on obtient la description de l'ensemble des conditions
d'exp�riences � travers la s�rie de fichiers list�e ici:

#.      ``Physical_data_and_covariance_matrices.py``
#.      ``Physical_simulation_functions.py``
#.      ``Script_AlgorithmParameters.py``
#.      ``Script_BackgroundError_B.py``
#.      ``Script_Background_xb.py``
#.      ``Script_ObservationError_R.py``
#.      ``Script_Observation_yo.py``
#.      ``Script_UserPostAnalysis.py``

On insiste ici sur le fait que tous ces scripts sont �crits par l'utilisateur et
ne peuvent �tre test�s automatiquement par ADAO. Ainsi, l'utilisateur est tenu
de v�rifier les scripts (et en particulier leurs entr�es/sorties) afin de
limiter les difficult�s de d�bogage. On rappelle que: **la m�thodologie par
scripts n'est pas une proc�dure "s�re", en ce sens que des donn�es erron�es ou
des erreurs dans les calculs, peuvent �tre directement introduites dans
l'ex�cution du sch�ma YACS.**

Construire la cas avec une d�finition de donn�es externes par scripts
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Tous ces scripts peuvent ensuite �tre utilis�s pour d�finir le cas ADAO avec une
d�finition de donn�es externes par des fichiers de script Python. Cela se
r�alise de mani�re tout � fait similaire � la m�thode d�crite dans la partie
pr�c�dente `Construire un cas d'estimation avec une d�finition de donn�es
externes par scripts`_. Pour chaque variable � d�finir, on s�lectionne l'option
"*Script*"  du mot-cl� "*FROM*", ce qui conduit � une entr�e
"*SCRIPT_DATA/SCRIPT_FILE*" dans l'arbre graphique. Pour le mot-cl�
"*ObservationOperator*", on choisit la forme "*ScriptWithOneFunction*" et on
conserve la valeur par d�faut de l'incr�ment diff�rentiel.

Les autres �tapes pour construire le cas ADAO sont exactement les m�mes que dans
la partie pr�c�dente `Construire un cas d'estimation avec une d�finition
explicite des donn�es`_.

En utilisant l'op�rateur lin�aire simple :math:`\mathbf{H}` du fichier script
Python ``Physical_simulation_functions.py`` disponible dans le r�pertoire
standard des exemples, les r�sultats ressemblent �::

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

L'�tat au premier pas est l'�tat d'�bauche :math:`\mathbf{x}^b` g�n�r�
al�atoirement. Au cours du calcul, ces affichages sur la sortie standard sont
disponibles dans la fen�tre "*fen�tre de sortie de YACS*", que l'on obtient par
clic droit sur la fen�tre "*proc*" du sch�ma YACS ex�cut�.

.. [#] Pour de plus amples informations sur YACS, voir le *Guide utilisateur du module YACS* disponible dans le menu principal *Aide* de l'environnement SALOME.
