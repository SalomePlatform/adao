.. _section_reference:

================================================================================
Description de r�f�rence des commandes et mots-cl�s ADAO
================================================================================

Cette section pr�sente la description de r�f�rence des commandes et mots-cl�s
ADAO disponibles � travers l'interface graphique (GUI) ou � travers des scripts.
Chaque commande ou mot-cl� � d�finir par l'interface graphique (GUI) a des
propri�t�s particuli�res. La premi�re propri�t� est d'�tre *requise*,
*optionnelle* ou simplement utile, d�crivant un type d'entr�e. La seconde
propri�t� est d'�tre une variable "ouverte" avec un type fix� mais avec
n'importe quelle valeur autoris�e par le type, ou une variable "ferm�e", limit�e
� des valeurs sp�cifi�es. L'�diteur graphique EFICAS disposant de capacit�s
intrins�ques de validation, les propri�t�s des commandes ou mots-cl�s donn�es �
l'aide de l'interface graphique sont automatiquement correctes.

Les notations math�matiques utilis�es ci-dessous sont expliqu�es dans la section
:ref:`section_theory`.

Des exemples sur l'usage de ces commandes sont disponibles dans la section
:ref:`section_examples` et dans les fichiers d'exemple install�s avec le module
ADAO.

Liste des types d'entr�es possibles
-----------------------------------

.. index:: single: Dict
.. index:: single: Function
.. index:: single: Matrix
.. index:: single: ScalarSparseMatrix
.. index:: single: DiagonalSparseMatrix
.. index:: single: String
.. index:: single: Script
.. index:: single: Vector

Chaque variable ADAO pr�sente un pseudo-type qui aide � la remplir et � la
valider. Les diff�rents pseudo-types sont:

**Dict**
    Cela indique une variable qui doit �tre remplie avec un dictionnaire Python
    ``{"cl�":"valeur"...}``, usuellement donn� soit par une cha�ne de caract�res
    soit par un fichier script.

**Function**
    Cela indique une variable qui doit �tre donn�e comme une fonction Python,
    usuellement donn�e soit par une cha�ne de caract�res soit par un fichier
    script.

**Matrix**
    Cela indique une variable qui doit �tre donn�e comme une matrice,
    usuellement donn�e soit par une cha�ne de caract�res soit par un fichier
    script.

**ScalarSparseMatrix**
    Cela indique une variable qui doit �tre donn�e comme un nombre unique (qui
    sera utilis� pour multiplier une matrice identit�), usuellement donn� soit
    par une cha�ne de caract�res soit par un fichier script.

**DiagonalSparseMatrix**
    Cela indique une variable qui doit , (qui sera
    utilis� pour remplacer la diagonale d'une matrice identit�), usuellement
    donn� soit par une cha�ne de caract�res soit par un fichier script.

**Script**
    Cela indique un script donn� comme un fichier externe. Il peut �tre d�sign�
    par un nom de fichier avec chemin complet ou seulement par un nom de fichier
    sans le chemin. Si le fichier est donn� uniquement par un nom sans chemin,
    et si un r�pertoire d'�tude est aussi indiqu�, le fichier est recherch� dans
    le r�pertoire d'�tude donn�.

**String**
    Cela indique une cha�ne de caract�res fournissant une repr�sentation
    litt�rale d'une matrice, d'un vecteur ou d'une collection de vecteurs, comme
    par exemple "1 2 ; 3 4" ou "[[1,2],[3,4]]" pour une matrice carr�e de taille
    2x2.

**Vector**
    Cela indique une variable qui doit �tre remplie comme un vecteur,
    usuellement donn� soit par une cha�ne de caract�res soit par un fichier
    script.

**VectorSerie**
    Cela indique une variable qui doit �tre remplie comme une liste de vecteurs,
    usuellement donn�e soit par une cha�ne de caract�res soit par un fichier
    script.

Lorsqu'une commande ou un mot-cl� peut �tre rempli par un nom de fichier script,
ce script doit pr�senter une variable ou une m�thode que porte le m�me nom que
la variable � remplir. En d'autres mots, lorsque l'on importe le script dans un
noeud Python de YACS, il doit cr�er une variable du bon nom dans l'espace de
nommage courant du noeud.

Description de r�f�rence pour les cas de calcul ADAO
----------------------------------------------------

Liste des commandes et mots-cl�s pour un cas de calcul ADAO
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

La premi�re s�rie de commandes est li�e � la description d'un cas de calcul, qui
est une proc�dure d'*Assimilation de Donn�es* ou d'*Optimisation*. Les termes
sont class�s par ordre alphab�tique, sauf le premier, qui d�crit le choix entre
le calcul ou la v�rification. Les diff�rentes commandes sont les suivantes:

**ASSIMILATION_STUDY**
    *Commande obligatoire*. C'est la commande g�n�rale qui d�crit le cas
    d'assimilation de donn�es ou d'optimisation. Elle contient hi�rarchiquement
    toutes les autres commandes.

**Algorithm**
    *Commande obligatoire*. C'est une cha�ne de caract�re qui indique l'algorithme
    d'assimilation de donn�es ou d'optimisation choisi. Les choix sont limit�s
    et disponibles � travers l'interface graphique. Il existe par exemple le
    "3DVAR", le "Blue"... Voir plus loin la liste des algorithmes et des
    param�tres associ�s dans la sous-section `Commandes optionnelles et requises
    pour les algorithmes de calcul`_.

**AlgorithmParameters**
    *Commande optionnelle*. Elle permet d'ajouter des param�tres optionnels pour
    contr�ler l'algorithme d'assimilation de donn�es ou d'optimisation. Sa
    valeur est d�finie comme un objet de type "*Dict*". Voir plus loin la liste
    des algorithmes et des param�tres associ�s dans la sous-section `Commandes
    optionnelles et requises pour les algorithmes de calcul`_.

**Background**
    *Commande obligatoire*. Elle d�finit le vecteur d'�bauche ou
    d'initialisation, not� pr�c�demment :math:`\mathbf{x}^b`. Sa valeur est
    d�finie comme un objet de type "*Vector*".

**BackgroundError**
    *Commande obligatoire*. Elle d�finit la matrice de covariance des erreurs
    d'�bauche, not�e pr�c�demment :math:`\mathbf{B}`. Sa valeur est d�finie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

**ControlInput**
    *Commande optionnelle*. Elle indique le vecteur de contr�le utilis� pour
    forcer le mod�le d'�volution � chaque pas, usuellement not�
    :math:`\mathbf{U}`. Sa valeur est d�finie comme un objet de type "*Vector*"
    ou de type *VectorSerie*. Lorsqu'il n'y a pas de contr�le, sa valeur doit
    �tre une cha�ne vide ''.

**Debug**
    *Commande optionnelle*. Elle d�finit le niveau de sorties et d'informations
    interm�diaires de d�bogage. Les choix sont limit�s entre 0 (pour False) and
    1 (pour True).

**EvolutionError**
    *Commande optionnelle*. Elle d�finit la matrice de covariance des erreurs
    d'�volution, usuellement not�e :math:`\mathbf{Q}`.  Sa valeur est d�finie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

**EvolutionModel**
    *Commande optionnelle*. Elle indique l'op�rateur d'�volution du mod�le,
    usuellement not� :math:`M`, qui d�crit un pas �l�mentaire d'�volution. Sa
    valeur est d�finie comme un objet de type "*Function*". Diff�rentes formes
    fonctionnelles peuvent �tre utilis�es, comme d�crit dans la sous-section
    suivante `Exigences pour les fonctions d�crivant un op�rateur`_. Si un
    contr�le :math:`U` est inclus dans le mod�le d'�volution, l'op�rateur doit
    �tre appliqu� � une paire :math:`(X,U)`.

**InputVariables**
    *Commande optionnelle*. Elle permet d'indiquer le nom et la taille des
    variables physiques qui sont rassembl�es dans le vecteur d'�tat. Cette
    information est destin�e � �tre utilis�e dans le traitement algorithmique
    interne des donn�es.

**Observation**
    *Commande obligatoire*. Elle d�finit le vecteur d'observation utilis� en
    assimilation de donn�es ou en optimisation, et not� pr�c�demment
    :math:`\mathbf{y}^o`. Sa valeur est d�finie comme un objet de type "*Vector*"
    ou de type *VectorSerie*".

**ObservationError**
    *Commande obligatoire*. Elle d�finit la matrice de covariance des erreurs
    d'�bauche, not�e pr�c�demment :math:`\mathbf{R}`. Sa valeur est d�finie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

**ObservationOperator**
    *Commande obligatoire*. Elle indique l'op�rateur d'observation, not�e
    pr�c�demment :math:`H`, qui transforme les param�tres d'entr�e
    :math:`\mathbf{x}` en r�sultats :math:`\mathbf{y}` qui sont � comparer aux
    observations :math:`\mathbf{y}^o`.  Sa valeur est d�finie comme un objet de
    type "*Function*". Diff�rentes formes fonctionnelles peuvent �tre utilis�es,
    comme d�crit dans la sous-section suivante `Exigences pour les fonctions
    d�crivant un op�rateur`_. Si un contr�le :math:`U` est inclus dans le mod�le
    d'observation, l'op�rateur doit �tre appliqu� � une paire :math:`(X,U)`.

**Observers**
    *Commande optionnelle*. Elle permet de d�finir des observateurs internes,
    qui sont des fonctions li�es � une variable particuli�re, qui sont ex�cut�es
    chaque fois que cette variable est modifi�e. C'est une mani�re pratique de
    suivre des variables d'int�r�t durant le processus d'assimilation de donn�es
    ou d'optimisation, en l'affichant ou en la tra�ant, etc. Des exemples
    courants (squelettes) sont fournis pour aider l'utilisateur ou pour
    faciliter l'�laboration d'un cas.

**OutputVariables**
    *Commande optionnelle*. Elle permet d'indiquer le nom et la taille des 
    variables physiques qui sont rassembl�es dans le vecteur d'observation.
    Cette information est destin�e � �tre utilis�e dans le traitement
    algorithmique interne des donn�es.

**Study_name**
    *Commande obligatoire*. C'est une cha�ne de caract�res quelconque pour
    d�crire l'�tude ADAO par un nom ou une d�claration.

**Study_repertory**
    *Commande optionnelle*. S'il existe, ce r�pertoire est utilis� comme base
    pour les calculs, et il est utilis� pour trouver les fichiers de script,
    donn�s par nom sans r�pertoire, qui peuvent �tre utilis�s pour d�finir
    certaines variables.

**UserDataInit**
    *Commande optionnelle*. Elle permet d'initialiser certains param�tres ou
    certaines donn�es automatiquement avant le traitement de donn�es d'entr�e
    pour l'assimilation de donn�es ou l'optimisation. Pour cela, elle indique un
    nom de fichier de script � ex�cuter avant d'entrer dans l'initialisation des
    variables choisies.

**UserPostAnalysis**
    *Commande optionnelle*. Elle permet de traiter des param�tres ou des
    r�sultats apr�s le d�roulement de l'algorithme d'assimilation de donn�es ou
    d'optimisation. Sa valeur est d�finie comme un fichier script ou une cha�ne
    de caract�res, permettant de produire directement du code de post-processing
    dans un cas ADAO. Des exemples courants (squelettes) sont fournis pour aider
    l'utilisateur ou pour faciliter l'�laboration d'un cas.

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

Chaque algorithme peut �tre contr�l� en utilisant des options g�n�riques ou
particuli�res, donn�es � travers la commande optionnelle "*AlgorithmParameters*"
dans un fichier script ou une cha�ne de caract�res, � la mani�re de l'exemple
qui suit dans un fichier::

    AlgorithmParameters = {
        "Minimizer" : "LBFGSB",
        "MaximumNumberOfSteps" : 25,
        "StoreSupplementaryCalculations" : ["APosterioriCovariance","OMA"],
        }

Pour donner les valeurs de la commande "*AlgorithmParameters*" par une cha�ne de
caract�res, on doit utiliser des guillemets simples pour fournir une d�finition
standard de dictionnaire, comme par exemple::

    '{"Minimizer":"LBFGSB","MaximumNumberOfSteps":25}'

Cette section d�crit les options disponibles algorithme par algorithme. De plus,
pour chaque algorithme, les commandes/mots-cl�s obligatoires sont indiqu�s. Si
une option est sp�cifi�e par l'utilisateur pour un algorithme qui ne la supporte
pas, cette option est simplement laiss�e inutilis�e et ne bloque pas le
traitement. La signification des acronymes ou des noms particuliers peut �tre
trouv�e dans l':ref:`genindex` ou dans le :ref:`section_glossary`.

**"Blue"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  StoreInternalVariables
    Cette cl� bool�enne permet de stocker les variables internes par d�faut,
    principalement l'�tat courant lors d'un processus it�ratif. Attention, cela
    peut �tre un choix num�riquement co�teux dans certains cas de calculs. La
    valeur par d�faut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs co�teux. La valeur par d�faut est une liste vide, aucune de ces
    variables n'�tant calcul�e et stock�e par d�faut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "OMA", "OMB",
    "Innovation", "SigmaBck2", "SigmaObs2", "MahalanobisConsistency"].

**"ExtendedBlue"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  StoreInternalVariables
    Cette cl� bool�enne permet de stocker les variables internes par d�faut,
    principalement l'�tat courant lors d'un processus it�ratif. Attention, cela
    peut �tre un choix num�riquement co�teux dans certains cas de calculs. La
    valeur par d�faut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs co�teux. La valeur par d�faut est une liste vide, aucune de ces
    variables n'�tant calcul�e et stock�e par d�faut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "OMA", "OMB",
    "Innovation", "SigmaBck2", "SigmaObs2", "MahalanobisConsistency"].

**"LinearLeastSquares"**

  *Commandes obligatoires*
    *"Observation", "ObservationError",
    "ObservationOperator"*

  StoreInternalVariables
    Cette cl� bool�enne permet de stocker les variables internes par d�faut,
    principalement l'�tat courant lors d'un processus it�ratif. Attention, cela
    peut �tre un choix num�riquement co�teux dans certains cas de calculs. La
    valeur par d�faut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs co�teux. La valeur par d�faut est une liste vide, aucune de ces
    variables n'�tant calcul�e et stock�e par d�faut. Les noms possibles sont
    dans la liste suivante : ["OMA"].

**"3DVAR"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  Minimizer
    Cette cl� permet de changer le minimiseur pour l'optimiseur. Le choix par
    d�faut est "LBFGSB", et les choix possibles sont "LBFGSB" (minimisation non
    lin�aire sous contraintes, voir [Byrd95]_, [Morales11]_ et [Zhu97]_), "TNC"
    (minimisation non lin�aire sous contraintes), "CG" (minimisation non
    lin�aire sans contraintes), "BFGS" (minimisation non lin�aire sans
    contraintes), "NCG" (minimisation de type gradient conjugu� de Newton). On
    conseille de conserver la valeur par d�faut.

  Bounds
    Cette cl� permet de d�finir des bornes sup�rieure et inf�rieure pour
    chaque variable d'�tat optimis�e. Les bornes peuvent �tre donn�es par une
    liste de liste de paires de bornes inf�rieure/sup�rieure pour chaque
    variable, avec une valeur ``None`` chaque fois qu'il n'y a pas de borne. Les
    bornes peuvent toujours �tre sp�cifi�es, mais seuls les optimiseurs sous
    contraintes les prennent en compte.

  MaximumNumberOfSteps
    Cette cl� indique le nombre maximum d'it�rations possibles en optimisation
    it�rative. Le d�faut est 15000, qui est tr�s similaire � une absence de
    limite sur les it�rations. Il est ainsi recommand� d'adapter ce param�tre
    aux besoins pour des probl�mes r�els. Pour certains optimiseurs, le nombre
    de pas effectif d'arr�t peut �tre l�g�rement diff�rent de la limite � cause
    d'exigences de contr�le interne de l'algorithme.

  CostDecrementTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque la fonction co�t d�cro�t moins que cette
    tol�rance au dernier pas. Le d�faut est de 1.e-7, et il est recommand�
    de l'adapter aux besoins pour des probl�mes r�els.

  ProjectedGradientTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque toutes les composantes du gradient projet�
    sont en-dessous de cette limite. C'est utilis� uniquement par les
    optimiseurs sous contraintes. Le d�faut est -1, qui d�signe le d�faut
    interne de chaque optimiseur (usuellement 1.e-5), et il n'est pas recommand�
    de le changer.

  GradientNormTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque la norme du gradient est en dessous de cette
    limite. C'est utilis� uniquement par les optimiseurs sans contraintes. Le
    d�faut est 1.e-5 et il n'est pas recommand� de le changer.

  StoreInternalVariables
    Cette cl� bool�enne permet de stocker les variables internes par d�faut,
    principalement l'�tat courant lors d'un processus it�ratif. Attention, cela
    peut �tre un choix num�riquement co�teux dans certains cas de calculs. La
    valeur par d�faut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs co�teux. La valeur par d�faut est une liste vide, aucune de ces
    variables n'�tant calcul�e et stock�e par d�faut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "OMA", "OMB",
    "Innovation", "SigmaObs2", "MahalanobisConsistency"].

**"NonLinearLeastSquares"**

  *Commandes obligatoires*
    *"Background",
    "Observation", "ObservationError",
    "ObservationOperator"*

  Minimizer
    Cette cl� permet de changer le minimiseur pour l'optimiseur. Le choix par
    d�faut est "LBFGSB", et les choix possibles sont "LBFGSB" (minimisation non
    lin�aire sous contraintes, voir [Byrd95]_, [Morales11]_ et [Zhu97]_), "TNC"
    (minimisation non lin�aire sous contraintes), "CG" (minimisation non
    lin�aire sans contraintes), "BFGS" (minimisation non lin�aire sans
    contraintes), "NCG" (minimisation de type gradient conjugu� de Newton). On
    conseille de conserver la valeur par d�faut.

  Bounds
    Cette cl� permet de d�finir des bornes sup�rieure et inf�rieure pour
    chaque variable d'�tat optimis�e. Les bornes peuvent �tre donn�es par une
    liste de liste de paires de bornes inf�rieure/sup�rieure pour chaque
    variable, avec une valeur ``None`` chaque fois qu'il n'y a pas de borne. Les
    bornes peuvent toujours �tre sp�cifi�es, mais seuls les optimiseurs sous
    contraintes les prennent en compte.

  MaximumNumberOfSteps
    Cette cl� indique le nombre maximum d'it�rations possibles en optimisation
    it�rative. Le d�faut est 15000, qui est tr�s similaire � une absence de
    limite sur les it�rations. Il est ainsi recommand� d'adapter ce param�tre
    aux besoins pour des probl�mes r�els. Pour certains optimiseurs, le nombre
    de pas effectif d'arr�t peut �tre l�g�rement diff�rent de la limite � cause
    d'exigences de contr�le interne de l'algorithme.

  CostDecrementTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque la fonction co�t d�cro�t moins que cette
    tol�rance au dernier pas. Le d�faut est de 1.e-7, et il est recommand�
    de l'adapter aux besoins pour des probl�mes r�els.

  ProjectedGradientTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque toutes les composantes du gradient projet�
    sont en-dessous de cette limite. C'est utilis� uniquement par les
    optimiseurs sous contraintes. Le d�faut est -1, qui d�signe le d�faut
    interne de chaque optimiseur (usuellement 1.e-5), et il n'est pas recommand�
    de le changer.

  GradientNormTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque la norme du gradient est en dessous de cette
    limite. C'est utilis� uniquement par les optimiseurs sans contraintes. Le
    d�faut est 1.e-5 et il n'est pas recommand� de le changer.

  StoreInternalVariables
    Cette cl� bool�enne permet de stocker les variables internes par d�faut,
    principalement l'�tat courant lors d'un processus it�ratif. Attention, cela
    peut �tre un choix num�riquement co�teux dans certains cas de calculs. La
    valeur par d�faut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs co�teux. La valeur par d�faut est une liste vide, aucune de ces
    variables n'�tant calcul�e et stock�e par d�faut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "OMA", "OMB",
    "Innovation", "SigmaObs2", "MahalanobisConsistency"].

**"EnsembleBlue"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  SetSeed
    Cette cl� permet de donner un nombre entier pour fixer la graine du
    g�n�rateur al�atoire utilis� pour g�n�rer l'ensemble. Un valeur pratique est
    par exemple 1000. Par d�faut, la graine est laiss�e non initialis�e, et elle
    utilise ainsi l'initialisation de l'ordinateur.

**"KalmanFilter"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  EstimationOf
    Cette cl� permet de choisir le type d'estimation � r�aliser. Cela peut �tre
    soit une estimation de l'�tat, avec la valeur "State", ou une estimation de
    param�tres, avec la valeur "Parameters". Le choix par d�faut est "State".

  StoreInternalVariables
    Cette cl� bool�enne permet de stocker les variables internes par d�faut,
    principalement l'�tat courant lors d'un processus it�ratif. Attention, cela
    peut �tre un choix num�riquement co�teux dans certains cas de calculs. La
    valeur par d�faut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs co�teux. La valeur par d�faut est une liste vide, aucune de ces
    variables n'�tant calcul�e et stock�e par d�faut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "Innovation"].

**"ExtendedKalmanFilter"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  Bounds
    Cette cl� permet de d�finir des bornes sup�rieure et inf�rieure pour chaque
    variable d'�tat optimis�e. Les bornes peuvent �tre donn�es par une liste de
    liste de paires de bornes inf�rieure/sup�rieure pour chaque variable, avec
    une valeur extr�me chaque fois qu'il n'y a pas de borne. Les bornes peuvent
    toujours �tre sp�cifi�es, mais seuls les optimiseurs sous contraintes les
    prennent en compte.

  ConstrainedBy
    Cette cl� permet de d�finir la m�thode pour prendre en compte les bornes. Les
    m�thodes possibles sont dans la liste suivante : ["EstimateProjection"].

  EstimationOf
    Cette cl� permet de choisir le type d'estimation � r�aliser. Cela peut �tre
    soit une estimation de l'�tat, avec la valeur "State", ou une estimation de
    param�tres, avec la valeur "Parameters". Le choix par d�faut est "State".

  StoreInternalVariables
    Cette cl� bool�enne permet de stocker les variables internes par d�faut,
    principalement l'�tat courant lors d'un processus it�ratif. Attention, cela
    peut �tre un choix num�riquement co�teux dans certains cas de calculs. La
    valeur par d�faut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs co�teux. La valeur par d�faut est une liste vide, aucune de ces
    variables n'�tant calcul�e et stock�e par d�faut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "Innovation"].

**"UnscentedKalmanFilter"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  Bounds
    Cette cl� permet de d�finir des bornes sup�rieure et inf�rieure pour chaque
    variable d'�tat optimis�e. Les bornes peuvent �tre donn�es par une liste de
    liste de paires de bornes inf�rieure/sup�rieure pour chaque variable, avec
    une valeur extr�me chaque fois qu'il n'y a pas de borne. Les bornes peuvent
    toujours �tre sp�cifi�es, mais seuls les optimiseurs sous contraintes les
    prennent en compte.

  ConstrainedBy
    Cette cl� permet de d�finir la m�thode pour prendre en compte les bornes. Les
    m�thodes possibles sont dans la liste suivante : ["EstimateProjection"].

  EstimationOf
    Cette cl� permet de choisir le type d'estimation � r�aliser. Cela peut �tre
    soit une estimation de l'�tat, avec la valeur "State", ou une estimation de
    param�tres, avec la valeur "Parameters". Le choix par d�faut est "State".

  Alpha, Beta, Kappa, Reconditioner
    Ces cl�s sont des param�tres de mise � l'�chelle interne. "Alpha" requiert
    une valeur comprise entre 1.e-4 et 1. "Beta" a une valeur optimale de 2 pour
    une distribution *a priori* gaussienne. "Kappa" requiert une valeur enti�re,
    dont la bonne valeur par d�faut est obtenue en la mettant � 0.
    "Reconditioner" requiert une valeur comprise entre 1.e-3 et 10, son d�faut
    �tant 1.

  StoreInternalVariables
    Cette cl� bool�enne permet de stocker les variables internes par d�faut,
    principalement l'�tat courant lors d'un processus it�ratif. Attention, cela
    peut �tre un choix num�riquement co�teux dans certains cas de calculs. La
    valeur par d�faut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs co�teux. La valeur par d�faut est une liste vide, aucune de ces
    variables n'�tant calcul�e et stock�e par d�faut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "Innovation"].

**"ParticleSwarmOptimization"**

  *Commandes obligatoires*
    *"Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator"*

  MaximumNumberOfSteps
    Cette cl� indique le nombre maximum d'it�rations possibles en optimisation
    it�rative. Le d�faut est 50, qui est une limite arbitraire. Il est ainsi
    recommand� d'adapter ce param�tre aux besoins pour des probl�mes r�els.

  NumberOfInsects
    Cette cl� indique le nombre d'insectes ou de particules dans l'essaim. La
    valeur par d�faut est 100, qui est une valeur par d�faut usuelle pour cet
    algorithme.

  SwarmVelocity
    Cette cl� indique la part de la vitesse d'insecte qui est impos�e par
    l'essaim. C'est une valeur r�elle positive. Le d�faut est de 1.

  GroupRecallRate
    Cette cl� indique le taux de rappel vers le meilleur insecte de l'essaim.
    C'est une valeur r�elle comprise entre 0 et 1. Le d�faut est de 0.5.

  QualityCriterion
    Cette cl� indique le crit�re de qualit�, qui est minimis� pour trouver
    l'estimation optimale de l'�tat. Le d�faut est le crit�re usuel de
    l'assimilation de donn�es nomm� "DA", qui est le crit�re de moindres carr�s
    pond�r�s augment�s. Les crit�res possibles sont dans la liste suivante, dans
    laquelle les noms �quivalents sont indiqu�s par "=" :
    ["AugmentedPonderatedLeastSquares"="APLS"="DA",
    "PonderatedLeastSquares"="PLS", "LeastSquares"="LS"="L2",
    "AbsoluteValue"="L1", "MaximumError"="ME"]

  SetSeed
    Cette cl� permet de donner un nombre entier pour fixer la graine du
    g�n�rateur al�atoire utilis� pour g�n�rer l'ensemble. Un valeur pratique est
    par exemple 1000. Par d�faut, la graine est laiss�e non initialis�e, et elle
    utilise ainsi l'initialisation par d�faut de l'ordinateur.

  StoreInternalVariables
    Cette cl� bool�enne permet de stocker les variables internes par d�faut,
    principalement l'�tat courant lors d'un processus it�ratif. Attention, cela
    peut �tre un choix num�riquement co�teux dans certains cas de calculs. La
    valeur par d�faut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs co�teux. La valeur par d�faut est une liste vide, aucune de ces
    variables n'�tant calcul�e et stock�e par d�faut. Les noms possibles sont
    dans la liste suivante : ["BMA", "OMA", "OMB", "Innovation"].

**"QuantileRegression"**

  *Commandes obligatoires*
    *"Background",
    "Observation",
    "ObservationOperator"*

  Quantile
    Cette cl� permet de d�finir la valeur r�elle du quantile recherch�, entre 0
    et 1. La valeur par d�faut est 0.5, correspondant � la m�diane.

  Minimizer
    Cette cl� permet de choisir l'optimiseur pour l'optimisation. Le choix par
    d�faut et le seul disponible est "MMQR" (Majorize-Minimize for Quantile
    Regression).

  MaximumNumberOfSteps
    Cette cl� indique le nombre maximum d'it�rations possibles en optimisation
    it�rative. Le d�faut est 15000, qui est tr�s similaire � une absence de
    limite sur les it�rations. Il est ainsi recommand� d'adapter ce param�tre
    aux besoins pour des probl�mes r�els.

  CostDecrementTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque la fonction co�t d�cro�t moins que cette
    tol�rance au dernier pas. Le d�faut est de 1.e-6, et il est recommand� de
    l'adapter aux besoins pour des probl�mes r�els.

  StoreInternalVariables
    Cette cl� bool�enne permet de stocker les variables internes par d�faut,
    principalement l'�tat courant lors d'un processus it�ratif. Attention, cela
    peut �tre un choix num�riquement co�teux dans certains cas de calculs. La
    valeur par d�faut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs co�teux. La valeur par d�faut est une liste vide, aucune de ces
    variables n'�tant calcul�e et stock�e par d�faut. Les noms possibles sont
    dans la liste suivante : ["BMA", "OMA", "OMB", "Innovation"].

Description de r�f�rence pour les cas de v�rification ADAO
----------------------------------------------------------

Liste des commandes et mots-cl�s pour un cas de v�rification ADAO
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

Le second jeu de commandes est li�e � la description d'un cas de v�rification,
qui est une proc�dure pour v�rifier les propri�t�s requises ailleurs sur
l'information par un cas de calcul. Les termes sont class�s par ordre
alphab�tique, sauf le premier, qui d�crit le choix entre le calcul ou la
v�rification. Les diff�rentes commandes sont les suivantes:

**CHECKING_STUDY**
    *Commande obligatoire*. C'est la commande g�n�rale qui d�crit le cas de
    v�rification. Elle contient hi�rarchiquement toutes les autres commandes.

**Algorithm**
    *Commande obligatoire*. C'est une cha�ne de caract�re qui indique
    l'algorithme de test choisi. Les choix sont limit�s et disponibles � travers
    l'interface graphique. Il existe par exemple "FunctionTest",
    "AdjointTest"... Voir plus loin la liste des algorithmes et des param�tres
    associ�s dans la sous-section `Commandes optionnelles et requises pour les
    algorithmes de v�rification`_.

**AlgorithmParameters**
    *Commande optionnelle*. Elle permet d'ajouter des param�tres optionnels pour
    contr�ler l'algorithme d'assimilation de donn�es ou d'optimisation. Sa
    valeur est d�finie comme un objet de type "*Dict*". Voir plus loin la liste
    des algorithmes et des param�tres associ�s dans la sous-section `Commandes
    optionnelles et requises pour les algorithmes de v�rification`_.

**CheckingPoint**
    *Commande obligatoire*. Elle d�finit le vecteur utilis�, not� pr�c�demment
    :math:`\mathbf{x}`. Sa valeur est d�finie comme un objet de type "*Vector*".

**Debug**
    *Commande optionnelle*. Elle d�finit le niveau de sorties et d'informations
    interm�diaires de d�bogage. Les choix sont limit�s entre 0 (pour False) et
    1 (pour True).

**ObservationOperator**
    *Commande obligatoire*. Elle indique l'op�rateur d'observation, not�e
    pr�c�demment :math:`H`, qui transforme les param�tres d'entr�e
    :math:`\mathbf{x}` en r�sultats :math:`\mathbf{y}` qui sont � comparer aux
    observations :math:`\mathbf{y}^o`.  Sa valeur est d�finie comme un objet de
    type "*Function*". Diff�rentes formes fonctionnelles peuvent �tre utilis�es,
    comme d�crit dans la sous-section suivante `Exigences pour les fonctions
    d�crivant un op�rateur`_. Si un contr�le :math:`U` est inclus dans le mod�le
    d'observation, l'op�rateur doit �tre appliqu� � une paire :math:`(X,U)`.

**Study_name**
    *Commande obligatoire*. C'est une cha�ne de caract�res quelconque pour
    d�crire l'�tude ADAO par un nom ou une d�claration.

**Study_repertory**
    *Commande optionnelle*. S'il existe, ce r�pertoire est utilis� comme base
    pour les calculs, et il est utilis� pour trouver les fichiers de script,
    donn�s par nom sans r�pertoire, qui peuvent �tre utilis�s pour d�finir
    certaines variables.

**UserDataInit**
    *Commande optionnelle*. Elle permet d'initialiser certains param�tres ou
    certaines donn�es automatiquement avant le traitement de donn�es d'entr�e
    pour l'assimilation de donn�es ou l'optimisation. Pour cela, elle indique un
    nom de fichier de script � ex�cuter avant d'entrer dans l'initialisation des
    variables choisies.

Commandes optionnelles et requises pour les algorithmes de v�rification
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

On rappelle que chaque algorithme peut �tre contr�l� en utilisant des options
g�n�riques ou particuli�res, donn�es � travers la commande optionnelle
"*AlgorithmParameters*", � la mani�re de l'exemple qui suit dans un fichier::

    AlgorithmParameters = {
        "AmplitudeOfInitialDirection" : 1,
        "EpsilonMinimumExponent" : -8,
        }

Si une option est sp�cifi�e par l'utilisateur pour un algorithme qui ne la
supporte pas, cette option est simplement laiss�e inutilis�e et ne bloque pas le
traitement. La signification des acronymes ou des noms particuliers peut �tre
trouv�e dans l':ref:`genindex` ou dans le :ref:`section_glossary`. De plus, pour
chaque algorithme, les commandes/mots-cl�s sont donn�s, d�crits dans `Liste des
commandes et mots-cl�s pour un cas de v�rification ADAO`_.

**"AdjointTest"**

  *Commandes obligatoires*
    *"CheckingPoint",
    "ObservationOperator"*

  AmplitudeOfInitialDirection
    Cette cl� indique la mise � l'�chelle de la perturbation initiale construite
    comme un vecteur utilis� pour la d�riv�e directionnelle autour du point
    nominal de v�rification. La valeur par d�faut est de 1, ce qui signifie pas
    de mise � l'�chelle.

  EpsilonMinimumExponent
    Cette cl� indique la valeur de l'exposant minimal du coefficient en
    puissance de 10 qui doit �tre utilis� pour faire d�cro�tre le multiplicateur
    de l'incr�ment. La valeur par d�faut est de -8, et elle doit �tre entre 0 et
    -20. Par exemple, la valeur par d�faut conduit � calculer le r�sidu de la
    formule avec un incr�ment fixe multipli� par 1.e0 jusqu'� 1.e-8.

  InitialDirection
    Cette cl� indique la direction vectorielle utilis�e pour la d�riv�e
    directionnelle autour du point nominal de v�rification. Cela doit �tre un
    vecteur. Si elle n'est pas sp�cifi�e, la direction par d�faut est une
    perturbation par d�faut autour de z�ro de la m�me taille vectorielle que le
    point de v�rification.

  SetSeed
    Cette cl� permet de donner un nombre entier pour fixer la graine du
    g�n�rateur al�atoire utilis� pour g�n�rer l'ensemble. Un valeur pratique est
    par exemple 1000. Par d�faut, la graine est laiss�e non initialis�e, et elle
    utilise ainsi l'initialisation par d�faut de l'ordinateur.

**"FunctionTest"**

  *Commandes obligatoires*
    *"CheckingPoint",
    "ObservationOperator"*

  NumberOfPrintedDigits
    Cette cl� indique le nombre de d�cimales de pr�cision pour les affichages de
    valeurs r�elles. La valeur par d�faut est de 5, avec un minimum de 0.

  NumberOfRepetition
    Cette cl� indique le nombre de fois o� r�p�ter l'�valuation de la fonction.
    La valeur vaut 1.
  
  SetDebug
    Cette cl� requiert l'activation, ou pas, du mode de d�bogage durant
    l'�valuation de la fonction. La valeur par d�faut est "True", les choix sont
    "True" ou "False".

**"GradientTest"**

  *Commandes obligatoires*
    *"CheckingPoint",
    "ObservationOperator"*

  AmplitudeOfInitialDirection
    Cette cl� indique la mise � l'�chelle de la perturbation initiale construite
    comme un vecteur utilis� pour la d�riv�e directionnelle autour du point
    nominal de v�rification. La valeur par d�faut est de 1, ce qui signifie pas
    de mise � l'�chelle.

  EpsilonMinimumExponent
    Cette cl� indique la valeur de l'exposant minimal du coefficient en
    puissance de 10 qui doit �tre utilis� pour faire d�cro�tre le multiplicateur
    de l'incr�ment. La valeur par d�faut est de -8, et elle doit �tre entre 0 et
    -20. Par exemple, la valeur par d�faut conduit � calculer le r�sidu de la
    formule avec un incr�ment fixe multipli� par 1.e0 jusqu'� 1.e-8.

  InitialDirection
    Cette cl� indique la direction vectorielle utilis�e pour la d�riv�e
    directionnelle autour du point nominal de v�rification. Cela doit �tre un
    vecteur. Si elle n'est pas sp�cifi�e, la direction par d�faut est une
    perturbation par d�faut autour de z�ro de la m�me taille vectorielle que le
    point de v�rification.

  ResiduFormula
    Cette cl� indique la formule de r�sidu qui doit �tre utilis�e pour le test.
    Le choix par d�faut est "Taylor", et les choix possibles sont "Taylor"
    (r�sidu du d�veloppement de Taylor de l'op�rateur, qui doit d�cro�tre comme
    le carr� de la perturbation) et "Norm" (r�sidu obtenu en prenant la norme du
    d�veloppement de Taylor � l'ordre 0, qui approxime le gradient, et qui doit
    rester constant).
  
  SetSeed
    Cette cl� permet de donner un nombre entier pour fixer la graine du
    g�n�rateur al�atoire utilis� pour g�n�rer l'ensemble. Un valeur pratique est
    par exemple 1000. Par d�faut, la graine est laiss�e non initialis�e, et elle
    utilise ainsi l'initialisation par d�faut de l'ordinateur.

**"LinearityTest"**

  *Commandes obligatoires*
    *"CheckingPoint",
    "ObservationOperator"*

  AmplitudeOfInitialDirection
    Cette cl� indique la mise � l'�chelle de la perturbation initiale construite
    comme un vecteur utilis� pour la d�riv�e directionnelle autour du point
    nominal de v�rification. La valeur par d�faut est de 1, ce qui signifie pas
    de mise � l'�chelle.

  EpsilonMinimumExponent
    Cette cl� indique la valeur de l'exposant minimal du coefficient en
    puissance de 10 qui doit �tre utilis� pour faire d�cro�tre le multiplicateur
    de l'incr�ment. La valeur par d�faut est de -8, et elle doit �tre entre 0 et
    -20. Par exemple, la valeur par d�faut conduit � calculer le r�sidu de la
    formule avec un incr�ment fixe multipli� par 1.e0 jusqu'� 1.e-8.

  InitialDirection
    Cette cl� indique la direction vectorielle utilis�e pour la d�riv�e
    directionnelle autour du point nominal de v�rification. Cela doit �tre un
    vecteur. Si elle n'est pas sp�cifi�e, la direction par d�faut est une
    perturbation par d�faut autour de zero de la m�me taille vectorielle que le
    point de v�rification.

  ResiduFormula
    Cette cl� indique la formule de r�sidu qui doit �tre utilis�e pour le test.
    Le choix par d�faut est "CenteredDL", et les choix possibles sont
    "CenteredDL" (r�sidu de la diff�rence entre la fonction au point nominal et
    ses valeurs avec des incr�ments positif et n�gatif, qui doit rester tr�s
    faible), "Taylor" (r�sidu du d�veloppement de Taylor de l'op�rateur
    normalis� par sa valeur nominal, qui doit rester tr�s faible),
    "NominalTaylor" (r�sidu de l'approximation � l'ordre 1 de l'op�rateur,
    normalis� au point nominal, qui doit rester proche de 1), et
    "NominalTaylorRMS" (r�sidu de l'approximation � l'ordre 1 de l'op�rateur,
    normalis� par l'�cart quadratique moyen (RMS) au point nominal, qui doit
    rester proche de 0).

  SetSeed
    Cette cl� permet de donner un nombre entier pour fixer la graine du
    g�n�rateur al�atoire utilis� pour g�n�rer l'ensemble. Un valeur pratique est
    par exemple 1000. Par d�faut, la graine est laiss�e non initialis�e, et elle
    utilise ainsi l'initialisation par d�faut de l'ordinateur.

Exigences pour les fonctions d�crivant un op�rateur
---------------------------------------------------

Les op�rateurs d'observation et d'�volution sont n�cessaires pour mettre en
oeuvre les proc�dures d'assimilation de donn�es ou d'optimisation. Ils
comprennent la simulation physique par des calculs num�riques, mais aussi le
filtrage et de restriction pour comparer la simulation � l'observation.
L'op�rateur d'�volution est ici consid�r� dans sa forme incr�mentale, qui
repr�sente la transition entre deux �tats successifs, et il est alors similaire
� l'op�rateur d'observation.

Sch�matiquement, un op�rateur doit donner une solution �tant donn� les
param�tres d'entr�e. Une partie des param�tres d'entr�e peut �tre modifi�e au
cours de la proc�dure d'optimisation. Ainsi, la repr�sentation math�matique d'un
tel processus est une fonction. Il a �t� bri�vement d�crit dans la section
:ref:`section_theory` et il est g�n�ralis�e ici par la relation:

.. math:: \mathbf{y} = O( \mathbf{x} )

entre les pseudo-observations :math:`\mathbf{y}` et les param�tres
:math:`\mathbf{x}` en utilisant l'op�rateur d'observation ou d'�volution
:math:`O`. La m�me repr�sentation fonctionnelle peut �tre utilis�e pour le
mod�le lin�aire tangent :math:`\mathbf{O}` de :math:`O` et son adjoint
:math:`\mathbf{O}^*`, qui sont aussi requis par certains algorithmes
d'assimilation de donn�es ou d'optimisation.

En entr�e et en sortie de ces op�rateurs, les variables :math:`\mathbf{x}` et
:math:`\mathbf{y}` ou leurs incr�ments sont math�matiquement des vecteurs, et
ils sont donc pass�s comme des vecteurs non-orient�s (de type liste ou vecteur
Numpy) ou orient�s (de type matrice Numpy).

Ensuite, **pour d�crire compl�tement un op�rateur, l'utilisateur n'a qu'�
fournir une fonction qui r�alise uniquement l'op�ration fonctionnelle de mani�re
compl�te**.

Cette fonction est g�n�ralement donn�e comme un script qui peut �tre ex�cut�
dans un noeud YACS. Ce script peut aussi, sans diff�rences, lancer des codes
externes ou utiliser des appels et des m�thodes internes SALOME. Si l'algorithme
n�cessite les 3 aspects de l'op�rateur (forme directe, forme tangente et forme
adjointe), l'utilisateur doit donner les 3 fonctions ou les approximer.

Il existe 3 m�thodes effectives pour l'utilisateur de fournir une repr�sentation
fonctionnelle de l'op�rateur. Ces m�thodes sont choisies dans le champ "*FROM*"
de chaque op�rateur ayant une valeur "*Function*" comme "*INPUT_TYPE*", comme le
montre la figure suivante:

  .. eficas_operator_function:
  .. image:: images/eficas_operator_function.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir une repr�sentation fonctionnelle de l'op�rateur**

Premi�re forme fonctionnelle : utiliser "*ScriptWithOneFunction*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithOneFunction
.. index:: single: DirectOperator
.. index:: single: DifferentialIncrement
.. index:: single: CenteredFiniteDifference

La premi�re consiste � ne fournir qu'une seule fonction potentiellement non
lin�aire, et d'approximer les op�rateurs tangent et adjoint. Ceci est fait en
utilisant le mot-cl� "*ScriptWithOneFunction*" pour la description de
l'op�rateur choisi dans l'interface graphique ADAO. L'utilisateur doit fournir
la fonction dans un script, avec un nom obligatoire "*DirectOperator*". Par
exemple, le script peut suivre le mod�le suivant::

    def DirectOperator( X ):
        """ Op�rateur direct de simulation non-lin�aire """
        ...
        ...
        ...
        return Y=O(X)

Dans ce cas, l'utilisateur doit aussi fournir une valeur pour l'incr�ment
diff�rentiel (ou conserver la valeur par d�faut), en utilisant dans l'interface
graphique (GUI) le mot-cl� "*DifferentialIncrement*", qui a une valeur par
d�faut de 1%. Ce coefficient est utilis� dans l'approximation diff�rences finies
pour construire les op�rateurs tangent et adjoint. L'ordre de l'approximation
diff�rences finies peut aussi �tre choisi � travers l'interface, en utilisant le
mot-cl� "*CenteredFiniteDifference*", avec 0 pour un sch�ma non centr� du
premier ordre (qui est la valeur par d�faut), et avec 1 pour un sch�ma centr� du
second ordre (qui co�te num�riquement deux fois plus cher que le premier ordre).

Cette premi�re forme de d�finition de l'op�rateur permet ais�ment de tester la
forme fonctionnelle avant son usage dans un cas ADAO, r�duisant notablement la
complexit� de l'impl�mentation de l'op�rateur.

**Avertissement important :** le nom "*DirectOperator*" est obligatoire, et le
type de l'argument X peut �tre une liste, un vecteur ou une matrice Numpy.
L'utilisateur doit traiter ces cas dans sa fonction.

Seconde forme fonctionnelle : utiliser "*ScriptWithFunctions*"
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithFunctions
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

**En g�n�ral, il est recommand� d'utiliser la premi�re forme fonctionnelle
plut�t que la seconde. Un petit accroissement de performances n'est pas une
bonne raison pour utiliser l'impl�mentation d�taill�e de cette seconde forme
fonctionnelle.**

La seconde consiste � fournir directement les trois op�rateurs li�s :math:`O`,
:math:`\mathbf{O}` et :math:`\mathbf{O}^*`. C'est effectu� en utilisant le
mot-cl� "*ScriptWithFunctions*" pour la description de l'op�rateur choisi dans
l'interface graphique (GUI) d'ADAO. L'utilisateur doit fournir trois fonctions
dans un script, avec trois noms obligatoires "*DirectOperator*",
"*TangentOperator*" et "*AdjointOperator*". Par exemple, le script peut suivre
le squelette suivant::

    def DirectOperator( X ):
        """ Op�rateur direct de simulation non-lin�aire """
        ...
        ...
        ...
        return quelque chose comme Y

    def TangentOperator( (X, dX) ):
        """ Op�rateur lin�aire tangent, autour de X, appliqu� � dX """
        ...
        ...
        ...
        return quelque chose comme Y

    def AdjointOperator( (X, Y) ):
        """ Op�rateur adjoint, autour de X, appliqu� � Y """
        ...
        ...
        ...
        return quelque chose comme X

Un nouvelle fois, cette seconde d�finition d'op�rateur permet ais�ment de tester
les formes fonctionnelles avant de les utiliser dans le cas ADAO, r�duisant la
complexit� de l'impl�mentation de l'op�rateur.

Pour certains algorithmes, il faut que les fonctions tangente et adjointe puisse
renvoyer les matrices �quivalentes � l'op�rateur lin�aire. Dans ce cas, lorsque,
respectivement, les arguments ``dX`` ou ``Y`` valent ``None``, l'utilisateur
doit renvoyer la matrice associ�e.

**Avertissement important :** les noms "*DirectOperator*", "*TangentOperator*"
et "*AdjointOperator*" sont obligatoires, et le type des arguments ``X``,
``Y``, ``dX`` peut �tre une liste, un vecteur ou une matrice Numpy.
L'utilisateur doit traiter ces cas dans ses fonctions.

Troisi�me forme fonctionnelle : utiliser "*ScriptWithSwitch*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithSwitch
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

**Il est recommand� de ne pas utiliser cette troisi�me forme fonctionnelle sans
une solide raison num�rique ou physique. Un accroissement de performances n'est
pas une bonne raison pour utiliser la complexit� de cette troisi�me forme
fonctionnelle. Seule une impossibilit� � utiliser les premi�re ou seconde formes
justifie l'usage de la troisi�me.**

La troisi�me forme donne de plus grandes possibilit�s de contr�le de l'ex�cution
des trois fonctions repr�sentant l'op�rateur, permettant un usage et un contr�le
avanc�s sur chaque ex�cution du code de simulation. C'est r�alisable en
utilisant le mot-cl� "*ScriptWithSwitch*" pour la description de l'op�rateur �
travers l'interface graphique (GUI) d'ADAO. L'utilisateur doit fournir un script
unique aiguillant, selon un contr�le, l'ex�cution des formes directe, tangente
et adjointe du code de simulation. L'utilisateur peut alors, par exemple,
utiliser des approximations pour les codes tangent et adjoint, ou introduire une
plus grande complexit� du traitement des arguments des fonctions. Mais cette
d�marche sera plus difficile � impl�menter et � d�boguer.

Toutefois, si vous souhaitez utiliser cette troisi�me forme, on recommande de se
baser sur le mod�le suivant pour le script d'aiguillage. Il n�cessite un fichier
script ou un code externe nomm� ici "*Physical_simulation_functions.py*",
contenant trois fonctions nomm�es "*DirectOperator*", "*TangentOperator*" and
"*AdjointOperator*" comme pr�c�demment. Voici le squelette d'aiguillage::

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

Toutes les modifications envisageables peuvent �tre faites � partir de cette
hypoth�se de squelette.

Cas sp�cial d'un op�rateur d'�volution avec contr�le
++++++++++++++++++++++++++++++++++++++++++++++++++++

Dans certains cas, l'op�rateur d'�volution ou d'observation doit �tre contr�l�
par un contr�le d'entr�e externe, qui est donn� *a priori*. Dans ce cas, la
forme g�n�rique du mod�le incr�mental est l�g�rement modifi� comme suit:

.. math:: \mathbf{y} = O( \mathbf{x}, \mathbf{u})

o� :math:`\mathbf{u}` est le contr�le sur l'incr�ment d'�tat. Dans ce cas,
l'op�rateur direct doit �tre appliqu� � une paire de variables :math:`(X,U)`.
Sch�matiquement, l'op�rateur doit �tre constuit comme suit::

    def DirectOperator( (X, U) ):
        """ Op�rateur direct de simulation non-lin�aire """
        ...
        ...
        ...
        return quelque chose comme X(n+1) (�volution) ou Y(n+1) (observation)

Les op�rateurs tangent et adjoint ont la m�me signature que pr�c�demment, en
notant que les d�riv�es doivent �tre faites seulement partiellement par rapport
� :math:`\mathbf{x}`. Dans un tel cas de contr�le explicite, seule la deuxi�me
forme fonctionnelle (en utilisant "*ScriptWithFunctions*") et la troisi�me forme
fonctionnelle (en utilisant "*ScriptWithSwitch*") peuvent �tre utilis�es.

Exigences pour d�crire les matrices de covariance
-------------------------------------------------

De multiples matrices de covariance sont n�cessaires pour mettre en oeuvre des
proc�dures d'assimilation de donn�es ou d'optimisation. Les principales sont la
matrice de covariance des erreurs d'�bauche, not�e :math:`\mathbf{B}`, et la
matrice de covariance des erreurs d'observation, not�e :math:`\mathbf{R}`. Une
telle matrice doit �tre une matrice carr� sym�trique semi-d�finie positive.

Il y a 3 m�thodes pratiques pour l'utilisateur pour fournir une matrice de
covariance. Ces m�thodes sont choisies � l'aide du mot-cl� "*INPUT_TYPE*" de
chaque matrice de covariance, comme montr� dans la figure qui suit :

  .. eficas_covariance_matrix:
  .. image:: images/eficas_covariance_matrix.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir la repr�sentation d'une matrice de covariance**

Premi�re forme matricielle : utiliser la repr�sentation "*Matrix*"
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Matrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

La premi�re forme est le d�faut et la plus g�n�rale. La matrice de covariance
:math:`\mathbf{M}` doit �tre enti�rement sp�cifi�e. M�me si la matrice est
sym�trique par nature, la totalit� de la matrice :math:`\mathbf{M}` doit �tre
donn�e.

.. math:: \mathbf{M} =  \begin{pmatrix}
    m_{11} & m_{12} & \cdots   & m_{1n} \\
    m_{21} & m_{22} & \cdots   & m_{2n} \\
    \vdots & \vdots & \vdots   & \vdots \\
    m_{n1} & \cdots & m_{nn-1} & m_{nn}
    \end{pmatrix}


Cela peut �tre r�alis� soit par un vecteur ou une matrice Numpy, soit par une
liste de listes de valeurs (c'est-�-dire une liste de lignes). Par exemple, une
matrice simple diagonale unitaire de covariances des erreurs d'�bauche
:math:`\mathbf{B}` peut �tre d�crite dans un fichier de script Python par::

    BackgroundError = [[1, 0 ... 0], [0, 1 ... 0] ... [0, 0 ... 1]]

ou::

    BackgroundError = numpy.eye(...)

Seconde forme matricielle : utiliser la repr�sentation "*ScalarSparseMatrix*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScalarSparseMatrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

Au contraire, la seconde forme matricielle est une m�thode tr�s simplifi�e pour
d�finir une matrice. La matrice de covariance :math:`\mathbf{M}` est suppos�e
�tre un multiple positif de la matrice identit�. Cette matrice peut alors �tre
sp�cifi�e de mani�re unique par le multiplicateur :math:`m`:

.. math:: \mathbf{M} =  m \times \begin{pmatrix}
    1       & 0      & \cdots   & 0      \\
    0       & 1      & \cdots   & 0      \\
    \vdots  & \vdots & \vdots   & \vdots \\
    0       & \cdots & 0        & 1
    \end{pmatrix}

Le multiplicateur :math:`m` doit �tre un nombre r�el ou entier positif (s'il
est n�gatif, ce qui est impossible car une matrice de covariance est positive,
il est convertit en nombre positif). Par exemple, une simple matrice diagonale
unitaire de covariances des erreurs d'�bauche :math:`\mathbf{B}` peut �tre
d�crite dans un fichier de script Python par::

    BackgroundError = 1.

ou, mieux, par un "*String*" directement dans le cas ADAO.

Troisi�me forme matricielle : utiliser la repr�sentation "*DiagonalSparseMatrix*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: DiagonalSparseMatrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError

La troisi�me forme est aussi une m�thode simplifi�e pour fournir la matrice,
mais un peu plus puissante que la seconde. La matrice de covariance
:math:`\mathbf{M}` est toujours consid�r�e comme diagonale, mais l'utilisateur
doit sp�cifier toutes les valeurs positives situ�es sur la diagonale. La matrice
peut alors �tre d�finie uniquement par un vecteur :math:`\mathbf{V}` qui se
retrouve ensuite sur la diagonale:

.. math:: \mathbf{M} =  \begin{pmatrix}
    v_{1}  & 0      & \cdots   & 0      \\
    0      & v_{2}  & \cdots   & 0      \\
    \vdots & \vdots & \vdots   & \vdots \\
    0      & \cdots & 0        & v_{n}
    \end{pmatrix}

Cela peut �tre r�alis� soit par vecteur ou une matrice Numpy, soit par
une liste, soit par une liste de listes de valeurs positives (dans tous les cas,
si certaines valeurs sont n�gatives, elles sont converties en valeurs
positives). Par exemple, un matrice simple diagonale unitaire des covariances
des erreurs d'�bauche :math:`\mathbf{B}` peut �tre d�crite dans un fichier de
script Python par::

    BackgroundError = [1, 1 ... 1]

ou::

    BackgroundError = numpy.ones(...)
