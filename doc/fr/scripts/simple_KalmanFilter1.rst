.. index:: single: KalmanFilter (exemple)

Premier exemple
...............

Le filtre de Kalman peut être utilisé pour une **réanalyse des observations
d'un modèle dynamique donné**. C'est parce que l'ensemble de l'historique
complet de l'observation est déjà connu au début des fenêtres temporelles qu'on
parle de *réanalyse*, même si l'analyse itérative conserve comme inconnues les
observations futures à un pas de temps donné.

Cet exemple décrit l'estimation itérative d'une quantité physique constante
(une tension électrique) selon l'exemple de [Welch06]_ (pages 11 et suivantes,
aussi disponible dans le SciPy Cookbook). Ce modèle permet d'illustrer
l'excellent comportement de cet algorithme vis-à-vis du bruit de mesure lorsque
le modèle d'évolution est simple. Le problème physique est l'estimation d'une
tension électrique, observée sur 50 pas de temps, avec du bruit, ce qui
implique ensuite 50 étapes d'analyses par le filtre. L'état idéalisé (valeur
dite "vraie", inconnu dans un cas réel) est désigné par ``Xtrue`` dans
l'exemple. Les observations :math:`\mathbf{y}^o` (désignée par ``Yobs`` dans
l'exemple) sont à renseigner, en utilisant le mot-clé "*VectorSerie*", comme
une série chronologique de mesures. On privilégie les observations au détriment
de l'ébauche, par l'indication d'une importante variance d'erreur d'ébauche par
rapport à la variance d'erreur d'observation. La première observation n'est pas
utilisée car l'ébauche :math:`\mathbf{x}^b` sert de première estimation de
l'état.

L'estimation s'effectue en affichant des résultats intermédiaires lors du
filtrage itératif. Grâce à ces informations intermédiaires, on peut aussi
obtenir les graphiques illustrant l'estimation de l'état et de la covariance
d'erreur a posteriori associée.
