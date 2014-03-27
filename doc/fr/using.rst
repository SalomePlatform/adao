.. _section_using:

================================================================================
Utiliser le module ADAO
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
.. |yacs_compile| image:: images/yacs_compile.png
   :align: middle
   :scale: 50%

Cette section pr�sente l'usage du module ADAO dans la plateforme SALOME. Il est
compl�t� par la description d�taill�e de l'ensemble des commandes et mots-cl�s
dans la section :ref:`section_reference`, par des proc�dures avanc�es d'usage
dans la section :ref:`section_advanced`, et par des exemples dans la section
:ref:`section_examples`.

Proc�dure logique pour construire un cas ADAO
---------------------------------------------

La construction d'un cas ADAO suit une d�marche simple pour d�finir l'ensemble
des donn�es d'entr�e, et ensuite g�n�rer un diagramme complet d'ex�cution
utilis� dans YACS. De nombreuses variations existent pour la d�finition des
donn�es d'entr�e, mais la s�quence logique reste inchang�e.

De mani�re g�n�rale, l'utilisateur doit conna�tre ses donn�es d'entr�es,
requises pour mettre au point une �tude d'assimilation de donn�es. Ces donn�es
peuvent �tre disponibles dans SALOME ou non.

**Fondamentalement, la proc�dure d'utilisation de ADAO comprend les �tapes
suivantes:**

#.  **Activez le module ADAO et utiliser l'�diteur graphique (GUI),**
#.  **Construire et/ou modifier le cas ADAO et l'enregistrer,**
#.  **Exporter le cas ADAO comme un sch�ma YACS,**
#.  **Compl�ter et modifier le sch�ma YACS, et l'enregistrer,**
#.  **Ex�cutez le cas YACS et obtenir les r�sultats.**

Chaque �tape est d�taill�e dans la section suivante.

�TAPE 1 : Activer le module ADAO et utiliser l'interface graphique d'�dition (GUI)
----------------------------------------------------------------------------------

Comme toujours pour un module, il doit �tre pr�alablement activ� en
s�lectionnant le bouton de module appropri� (ou le menu) dans la barre d'outils
de SALOME. S'il n'existe aucune �tude SALOME charg�e, un menu contextuel
appara�t, permettant de choisir entre la cr�ation d'une nouvelle �tude, ou
l'ouverture d'une �tude d�j� existante:

  .. _adao_activate1:
  .. image:: images/adao_activate.png
    :align: center
  .. centered::
    **Activation du module ADAO dans SALOME**

En choisissant le bouton "*Nouveau*", un �diteur int�gr� de cas EFICAS [#]_ sera
ouvert, en m�me temps que le "*navigateur d'objets*" standard. On peut alors
cliquer sur le bouton "*Nouveau*"(ou choisir l'entr�e "*Nouveau*"  dans le dans
le menu principal "*ADAO*") pour cr�er un nouveau cas ADAO, et on obtient :

  .. _adao_viewer:
  .. image:: images/adao_viewer.png
    :align: center
    :width: 100%
  .. centered::
    **L'�diteur EFICAS pour la d�finition des cas dans le module ADAO**

�TAPE 2 : Cr�er et modifier le cas ADAO, et l'enregistrer
---------------------------------------------------------

Pour construire un cas en utilisant EFICAS, on doit passer par une s�rie de
sous-�tapes, en choisissant, � chaque �tape, un mot-cl� puis en remplissant ses
valeurs. On note que c'est dans cette �tape qu'il faut, entre autres, d�finir
l'**appel au code de simulation** utilis� dans les op�rateurs d'observation ou
d'�volution d�crivant le probl�me [#]_.

L'�diteur structur� indique des types hi�rarchiques, des valeurs ou des
mots-cl�s autoris�s. Les mots-cl�s incomplets ou incorrects sont identifi�s par
un indicateur d'erreur visuel rouge. Les valeurs possibles sont indiqu�es pour
les mots-cl�s par la d�finition d'une liste limit�e de valeurs, et les entr�es
adapt�es sont donn�es pour les autres mots-cl�s. Des messages d'aide sont 
fournis de mani�re contextuelle aux places r�serv�es de l'�diteur.

Un nouveau cas est mis en place avec la liste minimale des commandes. Toutes les
commandes ou les mots-cl�s obligatoires sont d�j� pr�sents, aucun d'eux ne peut
�tre supprim�. Des mots-cl�s optionnels peuvent �tre ajout�s en les choisissant
dans une liste de suggestions de ceux autoris�s pour la commande principale, par
exemple la commande "*ASSIMILATION_STUDY*". � titre d'exemple, on peut ajouter
un mot-cl� "*AlgorithmParameters*", comme d�crit dans la derni�re partie de la
section :ref:`section_examples`.

A la fin de ces actions, lorsque tous les champs ou les mots-cl�s ont �t�
correctement d�finis, chaque ligne de l'arborescence des commandes doit
pr�senter un drapeau vert. Cela signifie que l'ensemble du cas est valide et
d�ment rempli (et qu'il peut �tre sauvegard�).

  .. _adao_jdcexample00:
  .. image:: images/adao_jdcexample01.png
    :align: center
    :scale: 75%
  .. centered::
    **Exemple d'un cas ADAO valide**

Au final, il faut enregistrer le cas ADAO en utilisant le bouton "*Enregistrer*"
|eficas_save|, ou le bouton "*Enregistrer sous*" |eficas_saveas|, ou en
choisissant l'entr�e "*Enregistrer/ Enregistrer sous*" dans le menu "*ADAO*". Il
est alors demand� un emplacement, � choisir dans l'arborescence des fichiers, et
un nom, qui sera compl�t� par l'extension "*.comm*" utilis�e pour les fichiers
JDC d'EFICAS. Cette action va g�n�rer une paire de fichiers d�crivant le cas
ADAO, avec le m�me nom de base, le premier pr�sentant une extension "*.comm*" et
le second une extension "*.py*" [#]_.

�TAPE 3 : Exporter le cas ADAO comme un sch�ma YACS
---------------------------------------------------

Lorsque le cas ADAO est compl�t�, il doit �tre converti ou export� sous la forme
d'un sch�ma YACS  [#]_ pour pouvoir ex�cuter le calcul d'assimilation de
donn�es. Cela peut �tre r�alis� facilement en utilisant le bouton "*Exporter
vers YACS*" |eficas_yacs|, ou de mani�re �quivalente en choisissant l'entr�e
"*Exporter vers YACS*" dans le menu principal "*ADAO*", ou dans le menu
contextuel du cas dans le navigateur d'objets SALOME.

  .. _adao_exporttoyacs01:
  .. image:: images/adao_exporttoyacs.png
    :align: center
    :scale: 75%
  .. centered::
    **Sous-menu "Exporter vers YACS" pour g�n�rer le sch�ma YACS � partir d'un cas ADAO**

Cela conduit � g�n�rer automatiquement un sch�ma YACS, et � activer le module
YACS sur ce sch�ma. Le fichier YACS, associ� au sch�ma, est stock� dans le m�me
r�pertoire et avec le m�me nom de base de fichier que le cas ADAO enregistr�,
changeant simplement son extension en "*.xml*". Attention, *si le nom de fichier
XML existe d�j�, le fichier est �cras� sans avertissement sur le remplacement du
fichier XML*.

�TAPE 4 : Compl�ter et modifier le sch�ma YACS, et l'enregistrer
----------------------------------------------------------------

.. index:: single: Analysis

Lorsque le sch�ma YACS est g�n�r� et ouvert dans SALOME � travers le l'interface
graphique du module YACS, on peut modifier ou compl�ter le sch�ma comme tout
sch�ma YACS standard. Des noeuds ou des blocs peuvent �tre ajout�s, copi�s ou
modifi�s pour �laborer une analyse complexe, ou pour ins�rer des capacit�s
d'assimilation de donn�es ou d'optimisation dans des sch�mas de calculs YACS
plus complexes.

Le principal compl�ment n�cessaire dans un sch�ma YACS est une �tape de
post-processing. L'�valuation du r�sultat doit �tre r�alis� dans le contexte
physique de simulation utilis� par la proc�dure d'assimilation de donn�es. Le
post-processing peut �tre fournit � travers le mot-cl� "*UserPostAnalysis*"
d'ADAO sous la forme d'un fichier de script ou d'une cha�ne de caract�res, par
des patrons ("templates"), ou peut �tre construit comme des noeuds YACS. Ces
deux mani�res de construire le post-processing peuvent utiliser toutes les
capacit�s de SALOME.

Dans le d�tail, le sch�ma YACS dispose d'un port de sortie "*algoResults*" dans
le bloc de calcul, qui donne acc�s � un objet de type "*pyobj*" nomm� ci-apr�s
"*ADD*", qui contient tous les r�sultats de calcul. Ces r�sultats peuvent �tre
obtenus en r�cup�rant les variables nomm�es stock�es au cours des calculs.
L'information principale est la variable "*Analysis*", qui peut �tre obtenue par
une commande python (par exemple dans un noeud script int�gr� ("in-line script
node") ou un script fourni � travers le mot-cl� "*UserPostAnalysis*"::

    Analysis = ADD.get("Analysis")[:]

"*Analysis*" est un objet complexe, similaire � une liste de valeurs calcul�es �
chaque �tape du calcul d'assimilation. Pour obtenir et afficher l'�valuation
optimale de l'�tat par assimilation de donn�es, dans un script fournit par
l'interm�diaire du mot-cl� "*UserPostAnalysis*", on peut utiliser::

    Xa = ADD.get("Analysis")[-1]
    print "Optimal state:", Xa
    print

Cette variable ``Xa`` est un vecteur de valeurs, qui repr�sente la solution du
probl�me d'�valuation par assimilation de donn�es ou par optimisation, not�e
:math:`\mathbf{x}^a` dans la section :ref:`section_theory`.

Une telle m�thode peut �tre utilis�e pour imprimer les r�sultats, ou pour les
convertir dans des structures qui peuvent �tre n�cessaires � un post-processing
natif ou externe � SALOME. Un exemple simple est disponible dans la section
:ref:`section_examples`.

�TAPE 5 : Ex�cuter le sch�ma YACS et obtenir les r�sultats
----------------------------------------------------------

Le sch�ma YACS est maintenant complet et peut �tre ex�cut�. La param�trisation
et l'ex�cution de ce cas YACS est enti�rement compatible avec la mani�re
standard de traiter un sch�ma YACS, comme d�crit dans le *Guide de l'utilisateur
du module YACS*.

Pour rappeler la mani�re la plus simple de proc�der, le sch�ma YACS doit �tre
compil� en utilisant le bouton |yacs_compile|, ou l'entr�e �quivalente du menu
YACS, pour pr�parer le sch�ma � son ex�cution. Ensuite, le sch�ma compil� peut
�tre d�marr�, ex�cut� pas � pas ou en utilisant des points d'arr�t, etc.

La sortie standard est restitu�e dans la "*fen�tre de sortie de YACS*" (ou
"*YACS Container Log*"), � laquelle on acc�de par un clic droit sur la fen�tre
"*proc*" dans l'interface graphique YACS. Les erreurs sont pr�sent�es soit
dans la "*fen�tre de sortie de YACS*", ou � la ligne de commande dans la fen�tre
de commandes (si l'environnement SALOME a �t� lanc� par une commande explicite,
et non par un menu ou une ic�ne de bureau). Par exemple, la sortie de l'exemple
simple ci-dessus est de la forme suivante::

   Entering in the assimilation study
   Name is set to........: Test
   Algorithm is set to...: Blue
   Launching the analyse

   Optimal state: [0.5, 0.5, 0.5]

pr�sent�e dans la "*fen�tre de sortie de YACS*".

L'ex�cution peut aussi �tre conduite en utilisant un script de commandes shell,
comme d�crit dans la section :ref:`section_advanced`.

.. [#] Pour de plus amples informations sur EFICAS, voir le *module EFICAS* et son aide disponible dans l'environnement SALOME.

.. [#] L'utilisation du code de simulation physique dans les op�rateurs de base de l'assimilation de donn�es est illustr�e ou d�crite dans les parties principales qui suivent.

.. [#] Pour de plus amples informations sur YACS, voir le *Guide utilisateur du module YACS* disponible dans le menu principal *Aide* de l'environnement SALOME.

.. [#] Ce fichier python interm�diaire peut aussi �tre utilis� comme d�crit dans la section :ref:`section_advanced`.
