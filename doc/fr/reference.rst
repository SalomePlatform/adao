.. _section_reference:

================================================================================
Description de référence des commandes et mots-clés ADAO
================================================================================

Cette section présente la description de référence des commandes et mots-clés
ADAO disponibles à travers l'interface graphique (GUI) ou à travers des scripts.
Chaque commande ou mot-clé à définir par l'interface graphique (GUI) a des
propriétés particulières. La première propriété est d'être *requise*,
*optionnelle* ou simplement utile, décrivant un type d'entrée. La seconde
propriété est d'être une variable "ouverte" avec un type fixé mais avec
n'importe quelle valeur autorisée par le type, ou une variable "fermée", limitée
à des valeurs spécifiées. L'éditeur graphique EFICAS disposant de capacités
intrinsèques de validation, les propriétés des commandes ou mots-clés données à
l'aide de l'interface graphique sont automatiquement correctes.

Les notations mathématiques utilisées ci-dessous sont expliquées dans la section
:ref:`section_theory`.

Des exemples sur l'usage de ces commandes sont disponibles dans la section
:ref:`section_examples` et dans les fichiers d'exemple installés avec le module
ADAO.

Liste des types d'entrées possibles
-----------------------------------

.. index:: single: Dict
.. index:: single: Function
.. index:: single: Matrix
.. index:: single: ScalarSparseMatrix
.. index:: single: DiagonalSparseMatrix
.. index:: single: String
.. index:: single: Script
.. index:: single: Vector

Chaque variable ADAO présente un pseudo-type qui aide à la remplir et à la
valider. Les différents pseudo-types sont:

**Dict**
    Cela indique une variable qui doit être remplie avec un dictionnaire Python
    ``{"clé":"valeur"...}``, usuellement donné soit par une chaîne de caractères
    soit par un fichier script.

**Function**
    Cela indique une variable qui doit être donnée comme une fonction Python,
    usuellement donnée soit par une chaîne de caractères soit par un fichier
    script.

**Matrix**
    Cela indique une variable qui doit être donnée comme une matrice,
    usuellement donnée soit par une chaîne de caractères soit par un fichier
    script.

**ScalarSparseMatrix**
    Cela indique une variable qui doit être donnée comme un nombre unique (qui
    sera utilisé pour multiplier une matrice identité), usuellement donné soit
    par une chaîne de caractères soit par un fichier script.

**DiagonalSparseMatrix**
    Cela indique une variable qui doit , (qui sera
    utilisé pour remplacer la diagonale d'une matrice identité), usuellement
    donné soit par une chaîne de caractères soit par un fichier script.

**Script**
    Cela indique un script donné comme un fichier externe. Il peut être désigné
    par un nom de fichier avec chemin complet ou seulement par un nom de fichier
    sans le chemin. Si le fichier est donné uniquement par un nom sans chemin,
    et si un répertoire d'étude est aussi indiqué, le fichier est recherché dans
    le répertoire d'étude donné.

**String**
    Cela indique une chaîne de caractères fournissant une représentation
    littérale d'une matrice, d'un vecteur ou d'une collection de vecteurs, comme
    par exemple "1 2 ; 3 4" ou "[[1,2],[3,4]]" pour une matrice carrée de taille
    2x2.

**Vector**
    Cela indique une variable qui doit être remplie comme un vecteur,
    usuellement donné soit par une chaîne de caractères soit par un fichier
    script.

**VectorSerie**
    Cela indique une variable qui doit être remplie comme une liste de vecteurs,
    usuellement donnée soit par une chaîne de caractères soit par un fichier
    script.

Lorsqu'une commande ou un mot-clé peut être rempli par un nom de fichier script,
ce script doit présenter une variable ou une méthode que porte le même nom que
la variable à remplir. En d'autres mots, lorsque l'on importe le script dans un
noeud Python de YACS, il doit créer une variable du bon nom dans l'espace de
nommage courant du noeud.

Description de référence pour les cas de calcul ADAO
----------------------------------------------------

Liste des commandes et mots-clés pour un cas de calcul ADAO
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ASSIMILATION_STUDY
.. index:: single: Algorithm
.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: ControlInput
.. index:: single: Debug
.. index:: single: EvolutionError
.. index:: single: EvolutionModel
.. index:: single: InputVariables
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: Observers
.. index:: single: OutputVariables
.. index:: single: Study_name
.. index:: single: Study_repertory
.. index:: single: UserDataInit
.. index:: single: UserPostAnalysis

La première série de commandes est liée à la description d'un cas de calcul, qui
est une procédure d'*Assimilation de Données* ou d'*Optimisation*. Les termes
sont classés par ordre alphabétique, sauf le premier, qui décrit le choix entre
le calcul ou la vérification. Les différentes commandes sont les suivantes:

**ASSIMILATION_STUDY**
    *Commande obligatoire*. C'est la commande générale qui décrit le cas
    d'assimilation de données ou d'optimisation. Elle contient hiérarchiquement
    toutes les autres commandes.

**Algorithm**
    *Commande obligatoire*. C'est une chaîne de caractère qui indique l'algorithme
    d'assimilation de données ou d'optimisation choisi. Les choix sont limités
    et disponibles à travers l'interface graphique. Il existe par exemple le
    "3DVAR", le "Blue"... Voir plus loin la liste des algorithmes et des
    paramètres associés dans la sous-section `Commandes optionnelles et requises
    pour les algorithmes de calcul`_.

**AlgorithmParameters**
    *Commande optionnelle*. Elle permet d'ajouter des paramètres optionnels pour
    contrôler l'algorithme d'assimilation de données ou d'optimisation. Sa
    valeur est définie comme un objet de type "*Dict*". Voir plus loin la liste
    des algorithmes et des paramètres associés dans la sous-section `Commandes
    optionnelles et requises pour les algorithmes de calcul`_.

**Background**
    *Commande obligatoire*. Elle définit le vecteur d'ébauche ou
    d'initialisation, noté précédemment :math:`\mathbf{x}^b`. Sa valeur est
    définie comme un objet de type "*Vector*".

**BackgroundError**
    *Commande obligatoire*. Elle définit la matrice de covariance des erreurs
    d'ébauche, notée précédemment :math:`\mathbf{B}`. Sa valeur est définie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

**ControlInput**
    *Commande optionnelle*. Elle indique le vecteur de contrôle utilisé pour
    forcer le modèle d'évolution à chaque pas, usuellement noté
    :math:`\mathbf{U}`. Sa valeur est définie comme un objet de type "*Vector*"
    ou de type *VectorSerie*. Lorsqu'il n'y a pas de contrôle, sa valeur doit
    être une chaîne vide ''.

**Debug**
    *Commande optionnelle*. Elle définit le niveau de sorties et d'informations
    intermédiaires de débogage. Les choix sont limités entre 0 (pour False) and
    1 (pour True).

**EvolutionError**
    *Commande optionnelle*. Elle définit la matrice de covariance des erreurs
    d'évolution, usuellement notée :math:`\mathbf{Q}`.  Sa valeur est définie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

**EvolutionModel**
    *Commande optionnelle*. Elle indique l'opérateur d'évolution du modèle,
    usuellement noté :math:`M`, qui décrit un pas élémentaire d'évolution. Sa
    valeur est définie comme un objet de type "*Function*". Différentes formes
    fonctionnelles peuvent être utilisées, comme décrit dans la sous-section
    suivante `Exigences pour les fonctions décrivant un opérateur`_. Si un
    contrôle :math:`U` est inclus dans le modèle d'évolution, l'opérateur doit
    être appliqué à une paire :math:`(X,U)`.

**InputVariables**
    *Commande optionnelle*. Elle permet d'indiquer le nom et la taille des
    variables physiques qui sont rassemblées dans le vecteur d'état. Cette
    information est destinée à être utilisée dans le traitement algorithmique
    interne des données.

**Observation**
    *Commande obligatoire*. Elle définit le vecteur d'observation utilisé en
    assimilation de données ou en optimisation, et noté précédemment
    :math:`\mathbf{y}^o`. Sa valeur est définie comme un objet de type "*Vector*"
    ou de type *VectorSerie*".

**ObservationError**
    *Commande obligatoire*. Elle définit la matrice de covariance des erreurs
    d'ébauche, notée précédemment :math:`\mathbf{R}`. Sa valeur est définie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

**ObservationOperator**
    *Commande obligatoire*. Elle indique l'opérateur d'observation, notée
    précédemment :math:`H`, qui transforme les paramètres d'entrée
    :math:`\mathbf{x}` en résultats :math:`\mathbf{y}` qui sont à comparer aux
    observations :math:`\mathbf{y}^o`.  Sa valeur est définie comme un objet de
    type "*Function*". Différentes formes fonctionnelles peuvent être utilisées,
    comme décrit dans la sous-section suivante `Exigences pour les fonctions
    décrivant un opérateur`_. Si un contrôle :math:`U` est inclus dans le modèle
    d'observation, l'opérateur doit être appliqué à une paire :math:`(X,U)`.

**Observers**
    *Commande optionnelle*. Elle permet de définir des observateurs internes,
    qui sont des fonctions liées à une variable particulière, qui sont exécutées
    chaque fois que cette variable est modifiée. C'est une manière pratique de
    suivre des variables d'intérêt durant le processus d'assimilation de données
    ou d'optimisation, en l'affichant ou en la traçant, etc. Des exemples
    courants (squelettes) sont fournis pour aider l'utilisateur ou pour
    faciliter l'élaboration d'un cas.

**OutputVariables**
    *Commande optionnelle*. Elle permet d'indiquer le nom et la taille des 
    variables physiques qui sont rassemblées dans le vecteur d'observation.
    Cette information est destinée à être utilisée dans le traitement
    algorithmique interne des données.

**Study_name**
    *Commande obligatoire*. C'est une chaîne de caractères quelconque pour
    décrire l'étude ADAO par un nom ou une déclaration.

**Study_repertory**
    *Commande optionnelle*. S'il existe, ce répertoire est utilisé comme base
    pour les calculs, et il est utilisé pour trouver les fichiers de script,
    donnés par nom sans répertoire, qui peuvent être utilisés pour définir
    certaines variables.

**UserDataInit**
    *Commande optionnelle*. Elle permet d'initialiser certains paramètres ou
    certaines données automatiquement avant le traitement de données d'entrée
    pour l'assimilation de données ou l'optimisation. Pour cela, elle indique un
    nom de fichier de script à exécuter avant d'entrer dans l'initialisation des
    variables choisies.

**UserPostAnalysis**
    *Commande optionnelle*. Elle permet de traiter des paramètres ou des
    résultats après le déroulement de l'algorithme d'assimilation de données ou
    d'optimisation. Sa valeur est définie comme un fichier script ou une chaîne
    de caractères, permettant de produire directement du code de post-processing
    dans un cas ADAO. Des exemples courants (squelettes) sont fournis pour aider
    l'utilisateur ou pour faciliter l'élaboration d'un cas.

Commandes optionnelles et requises pour les algorithmes de calcul
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: 3DVAR
.. index:: single: Blue
.. index:: single: ExtendedBlue
.. index:: single: EnsembleBlue
.. index:: single: KalmanFilter
.. index:: single: ExtendedKalmanFilter
.. index:: single: UnscentedKalmanFilter
.. index:: single: LinearLeastSquares
.. index:: single: NonLinearLeastSquares
.. index:: single: ParticleSwarmOptimization
.. index:: single: QuantileRegression

.. index:: single: AlgorithmParameters
.. index:: single: Bounds
.. index:: single: CostDecrementTolerance
.. index:: single: GradientNormTolerance
.. index:: single: GroupRecallRate
.. index:: single: MaximumNumberOfSteps
.. index:: single: Minimizer
.. index:: single: NumberOfInsects
.. index:: single: ProjectedGradientTolerance
.. index:: single: QualityCriterion
.. index:: single: Quantile
.. index:: single: SetSeed
.. index:: single: StoreInternalVariables
.. index:: single: StoreSupplementaryCalculations
.. index:: single: SwarmVelocity

Chaque algorithme peut être contrôlé en utilisant des options génériques ou
particulières, données à travers la commande optionnelle "*AlgorithmParameters*"
dans un fichier script ou une chaîne de caractères, à la manière de l'exemple
qui suit dans un fichier::

    AlgorithmParameters = {
        "Minimizer" : "LBFGSB",
        "MaximumNumberOfSteps" : 25,
        "StoreSupplementaryCalculations" : ["APosterioriCovariance","OMA"],
        }

Pour donner les valeurs de la commande "*AlgorithmParameters*" par une chaîne de
caractères, on doit utiliser des guillemets simples pour fournir une définition
standard de dictionnaire, comme par exemple::

    '{"Minimizer":"LBFGSB","MaximumNumberOfSteps":25}'

Cette section décrit les options disponibles algorithme par algorithme. De plus,
pour chaque algorithme, les commandes/mots-clés obligatoires sont indiqués. Si
une option est spécifiée par l'utilisateur pour un algorithme qui ne la supporte
pas, cette option est simplement laissée inutilisée et ne bloque pas le
traitement. La signification des acronymes ou des noms particuliers peut être
trouvée dans l':ref:`genindex` ou dans le :ref:`section_glossary`.

**"Blue"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  StoreInternalVariables
    Cette clé booléenne permet de stocker les variables internes par défaut,
    principalement l'état courant lors d'un processus itératif. Attention, cela
    peut être un choix numériquement coûteux dans certains cas de calculs. La
    valeur par défaut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs coûteux. La valeur par défaut est une liste vide, aucune de ces
    variables n'étant calculée et stockée par défaut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "OMA", "OMB",
    "Innovation", "SigmaBck2", "SigmaObs2", "MahalanobisConsistency"].

**"ExtendedBlue"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  StoreInternalVariables
    Cette clé booléenne permet de stocker les variables internes par défaut,
    principalement l'état courant lors d'un processus itératif. Attention, cela
    peut être un choix numériquement coûteux dans certains cas de calculs. La
    valeur par défaut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs coûteux. La valeur par défaut est une liste vide, aucune de ces
    variables n'étant calculée et stockée par défaut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "OMA", "OMB",
    "Innovation", "SigmaBck2", "SigmaObs2", "MahalanobisConsistency"].

**"LinearLeastSquares"**

  *Commandes obligatoires*
    *"Observation", "ObservationError",
    "ObservationOperator"*

  StoreInternalVariables
    Cette clé booléenne permet de stocker les variables internes par défaut,
    principalement l'état courant lors d'un processus itératif. Attention, cela
    peut être un choix numériquement coûteux dans certains cas de calculs. La
    valeur par défaut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs coûteux. La valeur par défaut est une liste vide, aucune de ces
    variables n'étant calculée et stockée par défaut. Les noms possibles sont
    dans la liste suivante : ["OMA"].

**"3DVAR"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  Minimizer
    Cette clé permet de changer le minimiseur pour l'optimiseur. Le choix par
    défaut est "LBFGSB", et les choix possibles sont "LBFGSB" (minimisation non
    linéaire sous contraintes, voir [Byrd95]_, [Morales11]_ et [Zhu97]_), "TNC"
    (minimisation non linéaire sous contraintes), "CG" (minimisation non
    linéaire sans contraintes), "BFGS" (minimisation non linéaire sans
    contraintes), "NCG" (minimisation de type gradient conjugué de Newton). On
    conseille de conserver la valeur par défaut.

  Bounds
    Cette clé permet de définir des bornes supérieure et inférieure pour
    chaque variable d'état optimisée. Les bornes peuvent être données par une
    liste de liste de paires de bornes inférieure/supérieure pour chaque
    variable, avec une valeur ``None`` chaque fois qu'il n'y a pas de borne. Les
    bornes peuvent toujours être spécifiées, mais seuls les optimiseurs sous
    contraintes les prennent en compte.

  MaximumNumberOfSteps
    Cette clé indique le nombre maximum d'itérations possibles en optimisation
    itérative. Le défaut est 15000, qui est très similaire à une absence de
    limite sur les itérations. Il est ainsi recommandé d'adapter ce paramètre
    aux besoins pour des problèmes réels. Pour certains optimiseurs, le nombre
    de pas effectif d'arrêt peut être légèrement différent de la limite à cause
    d'exigences de contrôle interne de l'algorithme.

  CostDecrementTolerance
    Cette clé indique une valeur limite, conduisant à arrêter le processus
    itératif d'optimisation lorsque la fonction coût décroît moins que cette
    tolérance au dernier pas. Le défaut est de 1.e-7, et il est recommandé
    de l'adapter aux besoins pour des problèmes réels.

  ProjectedGradientTolerance
    Cette clé indique une valeur limite, conduisant à arrêter le processus
    itératif d'optimisation lorsque toutes les composantes du gradient projeté
    sont en-dessous de cette limite. C'est utilisé uniquement par les
    optimiseurs sous contraintes. Le défaut est -1, qui désigne le défaut
    interne de chaque optimiseur (usuellement 1.e-5), et il n'est pas recommandé
    de le changer.

  GradientNormTolerance
    Cette clé indique une valeur limite, conduisant à arrêter le processus
    itératif d'optimisation lorsque la norme du gradient est en dessous de cette
    limite. C'est utilisé uniquement par les optimiseurs sans contraintes. Le
    défaut est 1.e-5 et il n'est pas recommandé de le changer.

  StoreInternalVariables
    Cette clé booléenne permet de stocker les variables internes par défaut,
    principalement l'état courant lors d'un processus itératif. Attention, cela
    peut être un choix numériquement coûteux dans certains cas de calculs. La
    valeur par défaut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs coûteux. La valeur par défaut est une liste vide, aucune de ces
    variables n'étant calculée et stockée par défaut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "OMA", "OMB",
    "Innovation", "SigmaObs2", "MahalanobisConsistency"].

**"NonLinearLeastSquares"**

  *Commandes obligatoires*
    *"Background",
    "Observation", "ObservationError",
    "ObservationOperator"*

  Minimizer
    Cette clé permet de changer le minimiseur pour l'optimiseur. Le choix par
    défaut est "LBFGSB", et les choix possibles sont "LBFGSB" (minimisation non
    linéaire sous contraintes, voir [Byrd95]_, [Morales11]_ et [Zhu97]_), "TNC"
    (minimisation non linéaire sous contraintes), "CG" (minimisation non
    linéaire sans contraintes), "BFGS" (minimisation non linéaire sans
    contraintes), "NCG" (minimisation de type gradient conjugué de Newton). On
    conseille de conserver la valeur par défaut.

  Bounds
    Cette clé permet de définir des bornes supérieure et inférieure pour
    chaque variable d'état optimisée. Les bornes peuvent être données par une
    liste de liste de paires de bornes inférieure/supérieure pour chaque
    variable, avec une valeur ``None`` chaque fois qu'il n'y a pas de borne. Les
    bornes peuvent toujours être spécifiées, mais seuls les optimiseurs sous
    contraintes les prennent en compte.

  MaximumNumberOfSteps
    Cette clé indique le nombre maximum d'itérations possibles en optimisation
    itérative. Le défaut est 15000, qui est très similaire à une absence de
    limite sur les itérations. Il est ainsi recommandé d'adapter ce paramètre
    aux besoins pour des problèmes réels. Pour certains optimiseurs, le nombre
    de pas effectif d'arrêt peut être légèrement différent de la limite à cause
    d'exigences de contrôle interne de l'algorithme.

  CostDecrementTolerance
    Cette clé indique une valeur limite, conduisant à arrêter le processus
    itératif d'optimisation lorsque la fonction coût décroît moins que cette
    tolérance au dernier pas. Le défaut est de 1.e-7, et il est recommandé
    de l'adapter aux besoins pour des problèmes réels.

  ProjectedGradientTolerance
    Cette clé indique une valeur limite, conduisant à arrêter le processus
    itératif d'optimisation lorsque toutes les composantes du gradient projeté
    sont en-dessous de cette limite. C'est utilisé uniquement par les
    optimiseurs sous contraintes. Le défaut est -1, qui désigne le défaut
    interne de chaque optimiseur (usuellement 1.e-5), et il n'est pas recommandé
    de le changer.

  GradientNormTolerance
    Cette clé indique une valeur limite, conduisant à arrêter le processus
    itératif d'optimisation lorsque la norme du gradient est en dessous de cette
    limite. C'est utilisé uniquement par les optimiseurs sans contraintes. Le
    défaut est 1.e-5 et il n'est pas recommandé de le changer.

  StoreInternalVariables
    Cette clé booléenne permet de stocker les variables internes par défaut,
    principalement l'état courant lors d'un processus itératif. Attention, cela
    peut être un choix numériquement coûteux dans certains cas de calculs. La
    valeur par défaut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs coûteux. La valeur par défaut est une liste vide, aucune de ces
    variables n'étant calculée et stockée par défaut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "OMA", "OMB",
    "Innovation", "SigmaObs2", "MahalanobisConsistency"].

**"EnsembleBlue"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  SetSeed
    Cette clé permet de donner un nombre entier pour fixer la graine du
    générateur aléatoire utilisé pour générer l'ensemble. Un valeur pratique est
    par exemple 1000. Par défaut, la graine est laissée non initialisée, et elle
    utilise ainsi l'initialisation de l'ordinateur.

**"KalmanFilter"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  EstimationOf
    Cette clé permet de choisir le type d'estimation à réaliser. Cela peut être
    soit une estimation de l'état, avec la valeur "State", ou une estimation de
    paramètres, avec la valeur "Parameters". Le choix par défaut est "State".

  StoreInternalVariables
    Cette clé booléenne permet de stocker les variables internes par défaut,
    principalement l'état courant lors d'un processus itératif. Attention, cela
    peut être un choix numériquement coûteux dans certains cas de calculs. La
    valeur par défaut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs coûteux. La valeur par défaut est une liste vide, aucune de ces
    variables n'étant calculée et stockée par défaut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "Innovation"].

**"ExtendedKalmanFilter"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  Bounds
    Cette clé permet de définir des bornes supérieure et inférieure pour chaque
    variable d'état optimisée. Les bornes peuvent être données par une liste de
    liste de paires de bornes inférieure/supérieure pour chaque variable, avec
    une valeur extrême chaque fois qu'il n'y a pas de borne. Les bornes peuvent
    toujours être spécifiées, mais seuls les optimiseurs sous contraintes les
    prennent en compte.

  ConstrainedBy
    Cette clé permet de définir la méthode pour prendre en compte les bornes. Les
    méthodes possibles sont dans la liste suivante : ["EstimateProjection"].

  EstimationOf
    Cette clé permet de choisir le type d'estimation à réaliser. Cela peut être
    soit une estimation de l'état, avec la valeur "State", ou une estimation de
    paramètres, avec la valeur "Parameters". Le choix par défaut est "State".

  StoreInternalVariables
    Cette clé booléenne permet de stocker les variables internes par défaut,
    principalement l'état courant lors d'un processus itératif. Attention, cela
    peut être un choix numériquement coûteux dans certains cas de calculs. La
    valeur par défaut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs coûteux. La valeur par défaut est une liste vide, aucune de ces
    variables n'étant calculée et stockée par défaut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "Innovation"].

**"UnscentedKalmanFilter"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  Bounds
    Cette clé permet de définir des bornes supérieure et inférieure pour chaque
    variable d'état optimisée. Les bornes peuvent être données par une liste de
    liste de paires de bornes inférieure/supérieure pour chaque variable, avec
    une valeur extrême chaque fois qu'il n'y a pas de borne. Les bornes peuvent
    toujours être spécifiées, mais seuls les optimiseurs sous contraintes les
    prennent en compte.

  ConstrainedBy
    Cette clé permet de définir la méthode pour prendre en compte les bornes. Les
    méthodes possibles sont dans la liste suivante : ["EstimateProjection"].

  EstimationOf
    Cette clé permet de choisir le type d'estimation à réaliser. Cela peut être
    soit une estimation de l'état, avec la valeur "State", ou une estimation de
    paramètres, avec la valeur "Parameters". Le choix par défaut est "State".

  Alpha, Beta, Kappa, Reconditioner
    Ces clés sont des paramètres de mise à l'échelle interne. "Alpha" requiert
    une valeur comprise entre 1.e-4 et 1. "Beta" a une valeur optimale de 2 pour
    une distribution *a priori* gaussienne. "Kappa" requiert une valeur entière,
    dont la bonne valeur par défaut est obtenue en la mettant à 0.
    "Reconditioner" requiert une valeur comprise entre 1.e-3 et 10, son défaut
    étant 1.

  StoreInternalVariables
    Cette clé booléenne permet de stocker les variables internes par défaut,
    principalement l'état courant lors d'un processus itératif. Attention, cela
    peut être un choix numériquement coûteux dans certains cas de calculs. La
    valeur par défaut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs coûteux. La valeur par défaut est une liste vide, aucune de ces
    variables n'étant calculée et stockée par défaut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "Innovation"].

**"ParticleSwarmOptimization"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  MaximumNumberOfSteps
    Cette clé indique le nombre maximum d'itérations possibles en optimisation
    itérative. Le défaut est 50, qui est une limite arbitraire. Il est ainsi
    recommandé d'adapter ce paramètre aux besoins pour des problèmes réels.

  NumberOfInsects
    Cette clé indique le nombre d'insectes ou de particules dans l'essaim. La
    valeur par défaut est 100, qui est une valeur par défaut usuelle pour cet
    algorithme.

  SwarmVelocity
    Cette clé indique la part de la vitesse d'insecte qui est imposée par
    l'essaim. C'est une valeur réelle positive. Le défaut est de 1.

  GroupRecallRate
    Cette clé indique le taux de rappel vers le meilleur insecte de l'essaim.
    C'est une valeur réelle comprise entre 0 et 1. Le défaut est de 0.5.

  QualityCriterion
    Cette clé indique le critère de qualité, qui est minimisé pour trouver
    l'estimation optimale de l'état. Le défaut est le critère usuel de
    l'assimilation de données nommé "DA", qui est le critère de moindres carrés
    pondérés augmentés. Les critères possibles sont dans la liste suivante, dans
    laquelle les noms équivalents sont indiqués par "=" :
    ["AugmentedPonderatedLeastSquares"="APLS"="DA",
    "PonderatedLeastSquares"="PLS", "LeastSquares"="LS"="L2",
    "AbsoluteValue"="L1", "MaximumError"="ME"]

  SetSeed
    Cette clé permet de donner un nombre entier pour fixer la graine du
    générateur aléatoire utilisé pour générer l'ensemble. Un valeur pratique est
    par exemple 1000. Par défaut, la graine est laissée non initialisée, et elle
    utilise ainsi l'initialisation par défaut de l'ordinateur.

  StoreInternalVariables
    Cette clé booléenne permet de stocker les variables internes par défaut,
    principalement l'état courant lors d'un processus itératif. Attention, cela
    peut être un choix numériquement coûteux dans certains cas de calculs. La
    valeur par défaut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs coûteux. La valeur par défaut est une liste vide, aucune de ces
    variables n'étant calculée et stockée par défaut. Les noms possibles sont
    dans la liste suivante : ["BMA", "OMA", "OMB", "Innovation"].

**"QuantileRegression"**

  *Commandes obligatoires*
    *"Background",
    "Observation",
    "ObservationOperator"*

  Quantile
    Cette clé permet de définir la valeur réelle du quantile recherché, entre 0
    et 1. La valeur par défaut est 0.5, correspondant à la médiane.

  Minimizer
    Cette clé permet de choisir l'optimiseur pour l'optimisation. Le choix par
    défaut et le seul disponible est "MMQR" (Majorize-Minimize for Quantile
    Regression).

  MaximumNumberOfSteps
    Cette clé indique le nombre maximum d'itérations possibles en optimisation
    itérative. Le défaut est 15000, qui est très similaire à une absence de
    limite sur les itérations. Il est ainsi recommandé d'adapter ce paramètre
    aux besoins pour des problèmes réels.

  CostDecrementTolerance
    Cette clé indique une valeur limite, conduisant à arrêter le processus
    itératif d'optimisation lorsque la fonction coût décroît moins que cette
    tolérance au dernier pas. Le défaut est de 1.e-6, et il est recommandé de
    l'adapter aux besoins pour des problèmes réels.

  StoreInternalVariables
    Cette clé booléenne permet de stocker les variables internes par défaut,
    principalement l'état courant lors d'un processus itératif. Attention, cela
    peut être un choix numériquement coûteux dans certains cas de calculs. La
    valeur par défaut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs coûteux. La valeur par défaut est une liste vide, aucune de ces
    variables n'étant calculée et stockée par défaut. Les noms possibles sont
    dans la liste suivante : ["BMA", "OMA", "OMB", "Innovation"].

Description de référence pour les cas de vérification ADAO
----------------------------------------------------------

Liste des commandes et mots-clés pour un cas de vérification ADAO
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: CHECKING_STUDY
.. index:: single: Algorithm
.. index:: single: AlgorithmParameters
.. index:: single: CheckingPoint
.. index:: single: Debug
.. index:: single: ObservationOperator
.. index:: single: Study_name
.. index:: single: Study_repertory
.. index:: single: UserDataInit

Le second jeu de commandes est liée à la description d'un cas de vérification,
qui est une procédure pour vérifier les propriétés requises ailleurs sur
l'information par un cas de calcul. Les termes sont classés par ordre
alphabétique, sauf le premier, qui décrit le choix entre le calcul ou la
vérification. Les différentes commandes sont les suivantes:

**CHECKING_STUDY**
    *Commande obligatoire*. C'est la commande générale qui décrit le cas de
    vérification. Elle contient hiérarchiquement toutes les autres commandes.

**Algorithm**
    *Commande obligatoire*. C'est une chaîne de caractère qui indique
    l'algorithme de test choisi. Les choix sont limités et disponibles à travers
    l'interface graphique. Il existe par exemple "FunctionTest",
    "AdjointTest"... Voir plus loin la liste des algorithmes et des paramètres
    associés dans la sous-section `Commandes optionnelles et requises pour les
    algorithmes de vérification`_.

**AlgorithmParameters**
    *Commande optionnelle*. Elle permet d'ajouter des paramètres optionnels pour
    contrôler l'algorithme d'assimilation de données ou d'optimisation. Sa
    valeur est définie comme un objet de type "*Dict*". Voir plus loin la liste
    des algorithmes et des paramètres associés dans la sous-section `Commandes
    optionnelles et requises pour les algorithmes de vérification`_.

**CheckingPoint**
    *Commande obligatoire*. Elle définit le vecteur utilisé, noté précédemment
    :math:`\mathbf{x}`. Sa valeur est définie comme un objet de type "*Vector*".

**Debug**
    *Commande optionnelle*. Elle définit le niveau de sorties et d'informations
    intermédiaires de débogage. Les choix sont limités entre 0 (pour False) et
    1 (pour True).

**ObservationOperator**
    *Commande obligatoire*. Elle indique l'opérateur d'observation, notée
    précédemment :math:`H`, qui transforme les paramètres d'entrée
    :math:`\mathbf{x}` en résultats :math:`\mathbf{y}` qui sont à comparer aux
    observations :math:`\mathbf{y}^o`.  Sa valeur est définie comme un objet de
    type "*Function*". Différentes formes fonctionnelles peuvent être utilisées,
    comme décrit dans la sous-section suivante `Exigences pour les fonctions
    décrivant un opérateur`_. Si un contrôle :math:`U` est inclus dans le modèle
    d'observation, l'opérateur doit être appliqué à une paire :math:`(X,U)`.

**Study_name**
    *Commande obligatoire*. C'est une chaîne de caractères quelconque pour
    décrire l'étude ADAO par un nom ou une déclaration.

**Study_repertory**
    *Commande optionnelle*. S'il existe, ce répertoire est utilisé comme base
    pour les calculs, et il est utilisé pour trouver les fichiers de script,
    donnés par nom sans répertoire, qui peuvent être utilisés pour définir
    certaines variables.

**UserDataInit**
    *Commande optionnelle*. Elle permet d'initialiser certains paramètres ou
    certaines données automatiquement avant le traitement de données d'entrée
    pour l'assimilation de données ou l'optimisation. Pour cela, elle indique un
    nom de fichier de script à exécuter avant d'entrer dans l'initialisation des
    variables choisies.

Commandes optionnelles et requises pour les algorithmes de vérification
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: AdjointTest
.. index:: single: FunctionTest
.. index:: single: GradientTest
.. index:: single: LinearityTest

.. index:: single: AlgorithmParameters
.. index:: single: AmplitudeOfInitialDirection
.. index:: single: EpsilonMinimumExponent
.. index:: single: InitialDirection
.. index:: single: ResiduFormula
.. index:: single: SetSeed

On rappelle que chaque algorithme peut être contrôlé en utilisant des options
génériques ou particulières, données à travers la commande optionnelle
"*AlgorithmParameters*", à la manière de l'exemple qui suit dans un fichier::

    AlgorithmParameters = {
        "AmplitudeOfInitialDirection" : 1,
        "EpsilonMinimumExponent" : -8,
        }

Si une option est spécifiée par l'utilisateur pour un algorithme qui ne la
supporte pas, cette option est simplement laissée inutilisée et ne bloque pas le
traitement. La signification des acronymes ou des noms particuliers peut être
trouvée dans l':ref:`genindex` ou dans le :ref:`section_glossary`. De plus, pour
chaque algorithme, les commandes/mots-clés sont donnés, décrits dans `Liste des
commandes et mots-clés pour un cas de vérification ADAO`_.

**"AdjointTest"**

  *Commandes obligatoires*
    *"CheckingPoint",
    "ObservationOperator"*

  AmplitudeOfInitialDirection
    Cette clé indique la mise à l'échelle de la perturbation initiale construite
    comme un vecteur utilisé pour la dérivée directionnelle autour du point
    nominal de vérification. La valeur par défaut est de 1, ce qui signifie pas
    de mise à l'échelle.

  EpsilonMinimumExponent
    Cette clé indique la valeur de l'exposant minimal du coefficient en
    puissance de 10 qui doit être utilisé pour faire décroître le multiplicateur
    de l'incrément. La valeur par défaut est de -8, et elle doit être entre 0 et
    -20. Par exemple, la valeur par défaut conduit à calculer le résidu de la
    formule avec un incrément fixe multiplié par 1.e0 jusqu'à 1.e-8.

  InitialDirection
    Cette clé indique la direction vectorielle utilisée pour la dérivée
    directionnelle autour du point nominal de vérification. Cela doit être un
    vecteur. Si elle n'est pas spécifiée, la direction par défaut est une
    perturbation par défaut autour de zéro de la même taille vectorielle que le
    point de vérification.

  SetSeed
    Cette clé permet de donner un nombre entier pour fixer la graine du
    générateur aléatoire utilisé pour générer l'ensemble. Un valeur pratique est
    par exemple 1000. Par défaut, la graine est laissée non initialisée, et elle
    utilise ainsi l'initialisation par défaut de l'ordinateur.

**"FunctionTest"**

  *Commandes obligatoires*
    *"CheckingPoint",
    "ObservationOperator"*

  NumberOfPrintedDigits
    Cette clé indique le nombre de décimales de précision pour les affichages de
    valeurs réelles. La valeur par défaut est de 5, avec un minimum de 0.

  NumberOfRepetition
    Cette clé indique le nombre de fois où répéter l'évaluation de la fonction.
    La valeur vaut 1.
  
  SetDebug
    Cette clé requiert l'activation, ou pas, du mode de débogage durant
    l'évaluation de la fonction. La valeur par défaut est "True", les choix sont
    "True" ou "False".

**"GradientTest"**

  *Commandes obligatoires*
    *"CheckingPoint",
    "ObservationOperator"*

  AmplitudeOfInitialDirection
    Cette clé indique la mise à l'échelle de la perturbation initiale construite
    comme un vecteur utilisé pour la dérivée directionnelle autour du point
    nominal de vérification. La valeur par défaut est de 1, ce qui signifie pas
    de mise à l'échelle.

  EpsilonMinimumExponent
    Cette clé indique la valeur de l'exposant minimal du coefficient en
    puissance de 10 qui doit être utilisé pour faire décroître le multiplicateur
    de l'incrément. La valeur par défaut est de -8, et elle doit être entre 0 et
    -20. Par exemple, la valeur par défaut conduit à calculer le résidu de la
    formule avec un incrément fixe multiplié par 1.e0 jusqu'à 1.e-8.

  InitialDirection
    Cette clé indique la direction vectorielle utilisée pour la dérivée
    directionnelle autour du point nominal de vérification. Cela doit être un
    vecteur. Si elle n'est pas spécifiée, la direction par défaut est une
    perturbation par défaut autour de zéro de la même taille vectorielle que le
    point de vérification.

  ResiduFormula
    Cette clé indique la formule de résidu qui doit être utilisée pour le test.
    Le choix par défaut est "Taylor", et les choix possibles sont "Taylor"
    (résidu du développement de Taylor de l'opérateur, qui doit décroître comme
    le carré de la perturbation) et "Norm" (résidu obtenu en prenant la norme du
    développement de Taylor à l'ordre 0, qui approxime le gradient, et qui doit
    rester constant).
  
  SetSeed
    Cette clé permet de donner un nombre entier pour fixer la graine du
    générateur aléatoire utilisé pour générer l'ensemble. Un valeur pratique est
    par exemple 1000. Par défaut, la graine est laissée non initialisée, et elle
    utilise ainsi l'initialisation par défaut de l'ordinateur.

**"LinearityTest"**

  *Commandes obligatoires*
    *"CheckingPoint",
    "ObservationOperator"*

  AmplitudeOfInitialDirection
    Cette clé indique la mise à l'échelle de la perturbation initiale construite
    comme un vecteur utilisé pour la dérivée directionnelle autour du point
    nominal de vérification. La valeur par défaut est de 1, ce qui signifie pas
    de mise à l'échelle.

  EpsilonMinimumExponent
    Cette clé indique la valeur de l'exposant minimal du coefficient en
    puissance de 10 qui doit être utilisé pour faire décroître le multiplicateur
    de l'incrément. La valeur par défaut est de -8, et elle doit être entre 0 et
    -20. Par exemple, la valeur par défaut conduit à calculer le résidu de la
    formule avec un incrément fixe multiplié par 1.e0 jusqu'à 1.e-8.

  InitialDirection
    Cette clé indique la direction vectorielle utilisée pour la dérivée
    directionnelle autour du point nominal de vérification. Cela doit être un
    vecteur. Si elle n'est pas spécifiée, la direction par défaut est une
    perturbation par défaut autour de zero de la même taille vectorielle que le
    point de vérification.

  ResiduFormula
    Cette clé indique la formule de résidu qui doit être utilisée pour le test.
    Le choix par défaut est "CenteredDL", et les choix possibles sont
    "CenteredDL" (résidu de la différence entre la fonction au point nominal et
    ses valeurs avec des incréments positif et négatif, qui doit rester très
    faible), "Taylor" (résidu du développement de Taylor de l'opérateur
    normalisé par sa valeur nominal, qui doit rester très faible),
    "NominalTaylor" (résidu de l'approximation à l'ordre 1 de l'opérateur,
    normalisé au point nominal, qui doit rester proche de 1), et
    "NominalTaylorRMS" (résidu de l'approximation à l'ordre 1 de l'opérateur,
    normalisé par l'écart quadratique moyen (RMS) au point nominal, qui doit
    rester proche de 0).

  SetSeed
    Cette clé permet de donner un nombre entier pour fixer la graine du
    générateur aléatoire utilisé pour générer l'ensemble. Un valeur pratique est
    par exemple 1000. Par défaut, la graine est laissée non initialisée, et elle
    utilise ainsi l'initialisation par défaut de l'ordinateur.

Exigences pour les fonctions décrivant un opérateur
---------------------------------------------------

Les opérateurs d'observation et d'évolution sont nécessaires pour mettre en
oeuvre les procédures d'assimilation de données ou d'optimisation. Ils
comprennent la simulation physique par des calculs numériques, mais aussi le
filtrage et de restriction pour comparer la simulation à l'observation.
L'opérateur d'évolution est ici considéré dans sa forme incrémentale, qui
représente la transition entre deux états successifs, et il est alors similaire
à l'opérateur d'observation.

Schématiquement, un opérateur doit donner une solution étant donné les
paramètres d'entrée. Une partie des paramètres d'entrée peut être modifiée au
cours de la procédure d'optimisation. Ainsi, la représentation mathématique d'un
tel processus est une fonction. Il a été brièvement décrit dans la section
:ref:`section_theory` et il est généralisée ici par la relation:

.. math:: \mathbf{y} = O( \mathbf{x} )

entre les pseudo-observations :math:`\mathbf{y}` et les paramètres
:math:`\mathbf{x}` en utilisant l'opérateur d'observation ou d'évolution
:math:`O`. La même représentation fonctionnelle peut être utilisée pour le
modèle linéaire tangent :math:`\mathbf{O}` de :math:`O` et son adjoint
:math:`\mathbf{O}^*`, qui sont aussi requis par certains algorithmes
d'assimilation de données ou d'optimisation.

En entrée et en sortie de ces opérateurs, les variables :math:`\mathbf{x}` et
:math:`\mathbf{y}` ou leurs incréments sont mathématiquement des vecteurs, et
ils sont donc passés comme des vecteurs non-orientés (de type liste ou vecteur
Numpy) ou orientés (de type matrice Numpy).

Ensuite, **pour décrire complètement un opérateur, l'utilisateur n'a qu'à
fournir une fonction qui réalise uniquement l'opération fonctionnelle de manière
complète**.

Cette fonction est généralement donnée comme un script qui peut être exécuté
dans un noeud YACS. Ce script peut aussi, sans différences, lancer des codes
externes ou utiliser des appels et des méthodes internes SALOME. Si l'algorithme
nécessite les 3 aspects de l'opérateur (forme directe, forme tangente et forme
adjointe), l'utilisateur doit donner les 3 fonctions ou les approximer.

Il existe 3 méthodes effectives pour l'utilisateur de fournir une représentation
fonctionnelle de l'opérateur. Ces méthodes sont choisies dans le champ "*FROM*"
de chaque opérateur ayant une valeur "*Function*" comme "*INPUT_TYPE*", comme le
montre la figure suivante:

  .. eficas_operator_function:
  .. image:: images/eficas_operator_function.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir une représentation fonctionnelle de l'opérateur**

Première forme fonctionnelle : utiliser "*ScriptWithOneFunction*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithOneFunction
.. index:: single: DirectOperator
.. index:: single: DifferentialIncrement
.. index:: single: CenteredFiniteDifference

La première consiste à ne fournir qu'une seule fonction potentiellement non
linéaire, et d'approximer les opérateurs tangent et adjoint. Ceci est fait en
utilisant le mot-clé "*ScriptWithOneFunction*" pour la description de
l'opérateur choisi dans l'interface graphique ADAO. L'utilisateur doit fournir
la fonction dans un script, avec un nom obligatoire "*DirectOperator*". Par
exemple, le script peut suivre le modèle suivant::

    def DirectOperator( X ):
        """ Opérateur direct de simulation non-linéaire """
        ...
        ...
        ...
        return Y=O(X)

Dans ce cas, l'utilisateur doit aussi fournir une valeur pour l'incrément
différentiel (ou conserver la valeur par défaut), en utilisant dans l'interface
graphique (GUI) le mot-clé "*DifferentialIncrement*", qui a une valeur par
défaut de 1%. Ce coefficient est utilisé dans l'approximation différences finies
pour construire les opérateurs tangent et adjoint. L'ordre de l'approximation
différences finies peut aussi être choisi à travers l'interface, en utilisant le
mot-clé "*CenteredFiniteDifference*", avec 0 pour un schéma non centré du
premier ordre (qui est la valeur par défaut), et avec 1 pour un schéma centré du
second ordre (qui coûte numériquement deux fois plus cher que le premier ordre).

Cette première forme de définition de l'opérateur permet aisément de tester la
forme fonctionnelle avant son usage dans un cas ADAO, réduisant notablement la
complexité de l'implémentation de l'opérateur.

**Avertissement important :** le nom "*DirectOperator*" est obligatoire, et le
type de l'argument X peut être une liste, un vecteur ou une matrice Numpy.
L'utilisateur doit traiter ces cas dans sa fonction.

Seconde forme fonctionnelle : utiliser "*ScriptWithFunctions*"
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithFunctions
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

**En général, il est recommandé d'utiliser la première forme fonctionnelle
plutôt que la seconde. Un petit accroissement de performances n'est pas une
bonne raison pour utiliser l'implémentation détaillée de cette seconde forme
fonctionnelle.**

La seconde consiste à fournir directement les trois opérateurs liés :math:`O`,
:math:`\mathbf{O}` et :math:`\mathbf{O}^*`. C'est effectué en utilisant le
mot-clé "*ScriptWithFunctions*" pour la description de l'opérateur choisi dans
l'interface graphique (GUI) d'ADAO. L'utilisateur doit fournir trois fonctions
dans un script, avec trois noms obligatoires "*DirectOperator*",
"*TangentOperator*" et "*AdjointOperator*". Par exemple, le script peut suivre
le squelette suivant::

    def DirectOperator( X ):
        """ Opérateur direct de simulation non-linéaire """
        ...
        ...
        ...
        return quelque chose comme Y

    def TangentOperator( (X, dX) ):
        """ Opérateur linéaire tangent, autour de X, appliqué à dX """
        ...
        ...
        ...
        return quelque chose comme Y

    def AdjointOperator( (X, Y) ):
        """ Opérateur adjoint, autour de X, appliqué à Y """
        ...
        ...
        ...
        return quelque chose comme X

Un nouvelle fois, cette seconde définition d'opérateur permet aisément de tester
les formes fonctionnelles avant de les utiliser dans le cas ADAO, réduisant la
complexité de l'implémentation de l'opérateur.

Pour certains algorithmes, il faut que les fonctions tangente et adjointe puisse
renvoyer les matrices équivalentes à l'opérateur linéaire. Dans ce cas, lorsque,
respectivement, les arguments ``dX`` ou ``Y`` valent ``None``, l'utilisateur
doit renvoyer la matrice associée.

**Avertissement important :** les noms "*DirectOperator*", "*TangentOperator*"
et "*AdjointOperator*" sont obligatoires, et le type des arguments ``X``,
``Y``, ``dX`` peut être une liste, un vecteur ou une matrice Numpy.
L'utilisateur doit traiter ces cas dans ses fonctions.

Troisième forme fonctionnelle : utiliser "*ScriptWithSwitch*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithSwitch
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

**Il est recommandé de ne pas utiliser cette troisième forme fonctionnelle sans
une solide raison numérique ou physique. Un accroissement de performances n'est
pas une bonne raison pour utiliser la complexité de cette troisième forme
fonctionnelle. Seule une impossibilité à utiliser les première ou seconde formes
justifie l'usage de la troisième.**

La troisième forme donne de plus grandes possibilités de contrôle de l'exécution
des trois fonctions représentant l'opérateur, permettant un usage et un contrôle
avancés sur chaque exécution du code de simulation. C'est réalisable en
utilisant le mot-clé "*ScriptWithSwitch*" pour la description de l'opérateur à
travers l'interface graphique (GUI) d'ADAO. L'utilisateur doit fournir un script
unique aiguillant, selon un contrôle, l'exécution des formes directe, tangente
et adjointe du code de simulation. L'utilisateur peut alors, par exemple,
utiliser des approximations pour les codes tangent et adjoint, ou introduire une
plus grande complexité du traitement des arguments des fonctions. Mais cette
démarche sera plus difficile à implémenter et à déboguer.

Toutefois, si vous souhaitez utiliser cette troisième forme, on recommande de se
baser sur le modèle suivant pour le script d'aiguillage. Il nécessite un fichier
script ou un code externe nommé ici "*Physical_simulation_functions.py*",
contenant trois fonctions nommées "*DirectOperator*", "*TangentOperator*" and
"*AdjointOperator*" comme précédemment. Voici le squelette d'aiguillage::

    import Physical_simulation_functions
    import numpy, logging
    #
    method = ""
    for param in computation["specificParameters"]:
        if param["name"] == "method":
            method = param["value"]
    if method not in ["Direct", "Tangent", "Adjoint"]:
        raise ValueError("No valid computation method is given")
    logging.info("Found method is \'%s\'"%method)
    #
    logging.info("Loading operator functions")
    Function = Physical_simulation_functions.DirectOperator
    Tangent  = Physical_simulation_functions.TangentOperator
    Adjoint  = Physical_simulation_functions.AdjointOperator
    #
    logging.info("Executing the possible computations")
    data = []
    if method == "Direct":
        logging.info("Direct computation")
        Xcurrent = computation["inputValues"][0][0][0]
        data = Function(numpy.matrix( Xcurrent ).T)
    if method == "Tangent":
        logging.info("Tangent computation")
        Xcurrent  = computation["inputValues"][0][0][0]
        dXcurrent = computation["inputValues"][0][0][1]
        data = Tangent(numpy.matrix(Xcurrent).T, numpy.matrix(dXcurrent).T)
    if method == "Adjoint":
        logging.info("Adjoint computation")
        Xcurrent = computation["inputValues"][0][0][0]
        Ycurrent = computation["inputValues"][0][0][1]
        data = Adjoint((numpy.matrix(Xcurrent).T, numpy.matrix(Ycurrent).T))
    #
    logging.info("Formatting the output")
    it = numpy.ravel(data)
    outputValues = [[[[]]]]
    for val in it:
      outputValues[0][0][0].append(val)
    #
    result = {}
    result["outputValues"]        = outputValues
    result["specificOutputInfos"] = []
    result["returnCode"]          = 0
    result["errorMessage"]        = ""

Toutes les modifications envisageables peuvent être faites à partir de cette
hypothèse de squelette.

Cas spécial d'un opérateur d'évolution avec contrôle
++++++++++++++++++++++++++++++++++++++++++++++++++++

Dans certains cas, l'opérateur d'évolution ou d'observation doit être contrôlé
par un contrôle d'entrée externe, qui est donné *a priori*. Dans ce cas, la
forme générique du modèle incrémental est légèrement modifié comme suit:

.. math:: \mathbf{y} = O( \mathbf{x}, \mathbf{u})

où :math:`\mathbf{u}` est le contrôle sur l'incrément d'état. Dans ce cas,
l'opérateur direct doit être appliqué à une paire de variables :math:`(X,U)`.
Schématiquement, l'opérateur doit être constuit comme suit::

    def DirectOperator( (X, U) ):
        """ Opérateur direct de simulation non-linéaire """
        ...
        ...
        ...
        return quelque chose comme X(n+1) (évolution) ou Y(n+1) (observation)

Les opérateurs tangent et adjoint ont la même signature que précédemment, en
notant que les dérivées doivent être faites seulement partiellement par rapport
à :math:`\mathbf{x}`. Dans un tel cas de contrôle explicite, seule la deuxième
forme fonctionnelle (en utilisant "*ScriptWithFunctions*") et la troisième forme
fonctionnelle (en utilisant "*ScriptWithSwitch*") peuvent être utilisées.

Exigences pour décrire les matrices de covariance
-------------------------------------------------

De multiples matrices de covariance sont nécessaires pour mettre en oeuvre des
procédures d'assimilation de données ou d'optimisation. Les principales sont la
matrice de covariance des erreurs d'ébauche, notée :math:`\mathbf{B}`, et la
matrice de covariance des erreurs d'observation, notée :math:`\mathbf{R}`. Une
telle matrice doit être une matrice carré symétrique semi-définie positive.

Il y a 3 méthodes pratiques pour l'utilisateur pour fournir une matrice de
covariance. Ces méthodes sont choisies à l'aide du mot-clé "*INPUT_TYPE*" de
chaque matrice de covariance, comme montré dans la figure qui suit :

  .. eficas_covariance_matrix:
  .. image:: images/eficas_covariance_matrix.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir la représentation d'une matrice de covariance**

Première forme matricielle : utiliser la représentation "*Matrix*"
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Matrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

La première forme est le défaut et la plus générale. La matrice de covariance
:math:`\mathbf{M}` doit être entièrement spécifiée. Même si la matrice est
symétrique par nature, la totalité de la matrice :math:`\mathbf{M}` doit être
donnée.

.. math:: \mathbf{M} =  \begin{pmatrix}
    m_{11} & m_{12} & \cdots   & m_{1n} \\
    m_{21} & m_{22} & \cdots   & m_{2n} \\
    \vdots & \vdots & \vdots   & \vdots \\
    m_{n1} & \cdots & m_{nn-1} & m_{nn}
    \end{pmatrix}


Cela peut être réalisé soit par un vecteur ou une matrice Numpy, soit par une
liste de listes de valeurs (c'est-à-dire une liste de lignes). Par exemple, une
matrice simple diagonale unitaire de covariances des erreurs d'ébauche
:math:`\mathbf{B}` peut être décrite dans un fichier de script Python par::

    BackgroundError = [[1, 0 ... 0], [0, 1 ... 0] ... [0, 0 ... 1]]

ou::

    BackgroundError = numpy.eye(...)

Seconde forme matricielle : utiliser la représentation "*ScalarSparseMatrix*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScalarSparseMatrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

Au contraire, la seconde forme matricielle est une méthode très simplifiée pour
définir une matrice. La matrice de covariance :math:`\mathbf{M}` est supposée
être un multiple positif de la matrice identité. Cette matrice peut alors être
spécifiée de manière unique par le multiplicateur :math:`m`:

.. math:: \mathbf{M} =  m \times \begin{pmatrix}
    1       & 0      & \cdots   & 0      \\
    0       & 1      & \cdots   & 0      \\
    \vdots  & \vdots & \vdots   & \vdots \\
    0       & \cdots & 0        & 1
    \end{pmatrix}

Le multiplicateur :math:`m` doit être un nombre réel ou entier positif (s'il
est négatif, ce qui est impossible car une matrice de covariance est positive,
il est convertit en nombre positif). Par exemple, une simple matrice diagonale
unitaire de covariances des erreurs d'ébauche :math:`\mathbf{B}` peut être
décrite dans un fichier de script Python par::

    BackgroundError = 1.

ou, mieux, par un "*String*" directement dans le cas ADAO.

Troisième forme matricielle : utiliser la représentation "*DiagonalSparseMatrix*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: DiagonalSparseMatrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

La troisième forme est aussi une méthode simplifiée pour fournir la matrice,
mais un peu plus puissante que la seconde. La matrice de covariance
:math:`\mathbf{M}` est toujours considérée comme diagonale, mais l'utilisateur
doit spécifier toutes les valeurs positives situées sur la diagonale. La matrice
peut alors être définie uniquement par un vecteur :math:`\mathbf{V}` qui se
retrouve ensuite sur la diagonale:

.. math:: \mathbf{M} =  \begin{pmatrix}
    v_{1}  & 0      & \cdots   & 0      \\
    0      & v_{2}  & \cdots   & 0      \\
    \vdots & \vdots & \vdots   & \vdots \\
    0      & \cdots & 0        & v_{n}
    \end{pmatrix}

Cela peut être réalisé soit par vecteur ou une matrice Numpy, soit par
une liste, soit par une liste de listes de valeurs positives (dans tous les cas,
si certaines valeurs sont négatives, elles sont converties en valeurs
positives). Par exemple, un matrice simple diagonale unitaire des covariances
des erreurs d'ébauche :math:`\mathbf{B}` peut être décrite dans un fichier de
script Python par::

    BackgroundError = [1, 1 ... 1]

ou::

    BackgroundError = numpy.ones(...)
