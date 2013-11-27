================================================================================
Documentation ADAO
================================================================================

.. image:: images/ADAO_logo.png
   :align: center
   :width: 20%

Le module ADAO fournit des fonctionnalit�s d'**assimilation de donn�es et
d'optimisation** dans un contexte SALOME. Il est bas� sur l'utilisation d'autres
modules, � savoir YACS et EFICAS, et sur l'utilisation d'une biblioth�que
g�n�rique sous-jacente d'assimilation de donn�es.

En bref, l'assimilation de donn�es est un cadre m�thodologique pour calculer
l'estimation optimale de la valeur r�elle (inaccessible) de l'�tat d'un syst�me
au cours du temps. Il utilise des informations provenant de mesures
exp�rimentales, ou observations, et de mod�les num�riques *a priori*, y compris
des informations sur leurs erreurs. Certaines des m�thodes incluses dans ce
cadre sont �galement connues sous les noms  d'*estimation des param�tres*, de
*probl�mes inverses*, d'*estimation bay�sienne*, d'*interpolation optimale*,
etc. De plus amples d�tails peuvent �tre trouv�s dans la section
:ref:`section_theory`.

La documentation de ce module est divis�e en plusieurs parties. La premi�re
:ref:`section_intro` est une introduction. La deuxi�me partie
:ref:`section_theory` pr�sente bri�vement l'assimilation de donn�es,
l'optimisation et les concepts. La troisi�me partie :ref:`section_using`
explique comment utiliser le module ADAO. La quatri�me partie
:ref:`section_reference` donne une description d�taill�e de toutes les commandes
ADAO et des mots-cl�s. La cinqui�me partie :ref:`section_examples` donne des
exemples sur l'utilisation d'ADAO. Les utilisateurs int�ress�s par une
acc�s rapide au module peuvent sauter cette section, mais un usage utile
du module n�cessite de lire et de revenir r�guli�rement aux troisi�me et
quatri�me parties. La derni�re partie :ref:`section_advanced` se focalise sur
des usages avanc�s du module, sur l'obtention de plus de renseignements, ou sur
l'usage par scripting, sans interface utilisateur graphique (GUI). Enfin,
n'oubliez pas de lire la partie :ref:`section_licence` pour respecter les
exigences de licence du module.

Dans cette documentation, on utilise les notations standards de l'alg�bre
lin�aire, de l'assimilation de donn�es (comme d�crit dans [Ide97]_) et de
l'optimisation. En particulier, les vecteurs sont �crits horizontalement ou
verticalement sans faire la diff�rence. Les matrices sont �crites soit
normalement, ou avec une notation condens�e, consistant � utiliser un espace
pour s�parer les valeurs, et un "``;``" pour s�parer les lignes de la matrice,
de fa�on continue sur une ligne.

Table des mati�res
------------------

.. toctree::
   :maxdepth: 2

   intro
   theory
   using
   reference
   examples
   advanced
   licence
   bibliography

Index et tables
---------------

* :ref:`genindex`
* :ref:`search`
* :ref:`section_glossary`
