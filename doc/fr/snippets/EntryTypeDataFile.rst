.. index:: single: DataFile
.. index:: single: ColNames
.. index:: single: ColMajor

**DataFile**, **ColNames**, **ColMajor**
    Cela indique des données fournies dans un fichier externe. Il peut être
    désigné par un nom de fichier avec chemin complet ou seulement par un nom
    de fichier sans le chemin. Si le fichier est donné uniquement par un nom
    sans chemin, et si un répertoire d'étude est aussi indiqué, le fichier est
    recherché dans le répertoire d'étude donné. Le contenu du fichier peut
    être :

    - en format texte (texte simple dans un fichier à extension ".txt" ou
      ".dat", texte à séparateur virgule ou point-virgule dans un fichier à
      extension ".csv", texte à séparateur tabulation dans un fichier à
      extension ".tsv")
    - en format binaire (mono-variable dans un fichier Numpy à extension
      ".npy", multi-variables dans un fichier NumpyZ à extension ".npz").

    Par défaut, les valeurs d'une variable doivent être rangées en colonnes
    pour être acquises ligne d'enregistrement par ligne d'enregistrement
    ("ColMajor=False"), mais elles peuvent aussi être rangées en lignes pour
    être acquises colonne d'enregistrement par colonne d'enregistrement
    ("ColMajor=True").

    Sans précision ou avec une liste vide pour les noms de variables, on
    utilise les valeurs toutes les variables, mais on peut aussi sélectionner
    uniquement celles des variables indiquées dans la liste de noms fournie
    dans "ColNames". Les noms de variable sont toujours en entête de colonne.

    Exemple de fichier CSV pour la variable "*Observation*" en "*DataFile*" ::

        # Fichier CSV à séparateur ";" ou ","
        # ===================================
        # Ligne de commentaires débutant par #
        # La ligne suivante est réservée au nommage des variables
        Alpha1;Observation;Alpha2
        0.1234;5.6789;9.0123
        1.2345;2.3456;3.
        2.3456;3.4567;4.56
        3.;4.;5.
        4;5;6
        5.123;6.789;7.8

    Exemple de fichier TXT pour la variable "*Observation*" en "*DataFile*" ::

        # Fichier TXT à séparateur espace
        # ===============================
        # Ligne de commentaires débutant par #
        # La ligne suivante est réservée au nommage des variables
        Alpha1 Observation Alpha2
        0.1234 5.6789 9.0123
        1.2345 2.3456 3.
        2.3456 3.4567 4.56
        3.     4.     5.
        4      5      6
        5.123  6.789  7.8

.. warning::

    Il est recommandé de vérifier les fichiers textes ou binaires, avant de les
    utiliser en entrée de ce type. Diverses vérifications sont effectuées au
    chargement, mais la variété des erreurs potentielles est grande. Dans la
    pratique, en respectant les exigences de nommage des variables et de
    commentaires, des fichiers textes issus de programmes ou de tableurs sont
    (la plupart du temps) compatibles.
