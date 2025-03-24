La compatibilité du module est en plus vérifiée par rapport à diverses versions
de Python ainsi que des modules support comme Numpy et Scipy. L'étendue des
versions atteintes lors des tests dépend de leur disponibilité, et les tests ne
sont pas systématiques sur toutes les versions intermédiaires. Pour toutes les
versions testées, le module ADAO se comporte de manière identique (dans la
mesure de modifications liées aux outils support). Il est fortement déconseillé
(ou impossible) d'utiliser ADAO avec une version inférieure à la version
minimale, et il n'y a pas de limitation explicite à l'utilisation du module
ADAO au-delà de la version atteinte (mais cela reste sans garantie). Si une
erreur inhabituelle est rencontrée pour des calculs fonctionnant précédemment,
il est fortement conseillé de revenir à des versions d'outils supports
comprises dans l'étendue décrite ci-dessous.

.. csv-table:: Intervalles de version de vérification des outils support pour ADAO
   :header: "Outil", "Version minimale", "Version atteinte"
   :widths: 20, 10, 10
   :align: center

   Python,     3.6.5,    3.13.2
   Numpy,      1.14.3,    2.2.4
   Scipy,      0.19.1,    1.15.2
   MatplotLib, 2.2.2,    3.10.1
   GnuplotPy,  1.8,    1.8
   NLopt,      2.4.2,    2.10.0
   FMPy,       0.3.20,    0.3.20
