================================================================================
Documentation ADAO
================================================================================

.. image:: images/ADAO_logo.png
   :align: center
   :width: 20%

Le module ADAO fournit des fonctionnalités d'**assimilation de données et
d'optimisation** dans un contexte SALOME. Il est basé sur l'utilisation d'autres
modules, à savoir YACS et EFICAS, et sur l'utilisation d'une bibliothèque
générique sous-jacente d'assimilation de données.

En bref, l'assimilation de données est un cadre méthodologique pour calculer
l'estimation optimale de la valeur réelle (inaccessible) de l'état d'un système
au cours du temps. Il utilise des informations provenant de mesures
expérimentales, ou observations, et de modèles numériques *a priori*, y compris
des informations sur leurs erreurs. Certaines des méthodes incluses dans ce
cadre sont également connues sous les noms  d'*estimation des paramètres*, de
*problèmes inverses*, d'*estimation bayésienne*, d'*interpolation optimale*,
etc. De plus amples détails peuvent être trouvés dans la partie
:ref:`section_theory`.

La documentation de ce module est divisée en plusieurs parties. La première est
une :ref:`section_intro`. La seconde partie présente :ref:`section_theory`, et à
leurs concepts. La troisième partie explique comment :ref:`section_using`.  La
quatrième partie présente des exemples d'utilisation sous la forme de
:ref:`section_examples`.  La cinquième partie détaille la
:ref:`section_reference`. Les utilisateurs intéressés par un accès rapide au
module peuvent s'arrêter avant la lecture de cette partie, mais un usage utile
du module nécessite de lire et de revenir régulièrement aux troisième et
cinquième parties. La dernière partie se focalise sur des
:ref:`section_advanced`, sur l'obtention de renseignements supplémentaires, ou
sur l'usage par scripts, sans interface utilisateur graphique (GUI). Enfin, pour
respecter les exigences de licence du module, n'oubliez pas de lire la partie
:ref:`section_licence`.

Dans cette documentation, on utilise les notations standards de l'algèbre
linéaire, de l'assimilation de données (comme décrit dans [Ide97]_) et de
l'optimisation. En particulier, les vecteurs sont écrits horizontalement ou
verticalement sans faire la différence. Les matrices sont écrites soit
normalement, ou avec une notation condensée, consistant à utiliser un espace
pour séparer les valeurs, et un "``;``" pour séparer les lignes de la matrice,
de façon continue sur une ligne.

Table des matières
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
