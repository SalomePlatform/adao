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
etc. De plus amples d�tails peuvent �tre trouv�s dans la partie
:ref:`section_theory`.

La documentation de ce module est divis�e en plusieurs parties. La premi�re est
une :ref:`section_intro`. La seconde partie pr�sente :ref:`section_theory`, et �
leurs concepts. La troisi�me partie explique comment :ref:`section_using`.  La
quatri�me partie pr�sente des exemples d'utilisation sous la forme de
:ref:`section_examples`.  La cinqui�me partie d�taille la
:ref:`section_reference`. Les utilisateurs int�ress�s par un acc�s rapide au
module peuvent s'arr�ter avant la lecture de cette partie, mais un usage utile
du module n�cessite de lire et de revenir r�guli�rement aux troisi�me et
cinqui�me parties. La derni�re partie se focalise sur des
:ref:`section_advanced`, sur l'obtention de renseignements suppl�mentaires, ou
sur l'usage par scripts, sans interface utilisateur graphique (GUI). Enfin, pour
respecter les exigences de licence du module, n'oubliez pas de lire la partie
:ref:`section_licence`.

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
   examples
   reference
   advanced
   licence
   glossary
   bibliography

Index et tables
---------------

* :ref:`genindex`
* :ref:`search`
.. * :ref:`section_glossary`
