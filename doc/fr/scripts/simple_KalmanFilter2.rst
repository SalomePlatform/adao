Le filtre de Kalman peut aussi être utilisé pour une **analyse courante des
observations d'un modèle dynamique donné**. Dans ce cas, l'analyse est conduite
de manière itérative, lors de l'arrivée de chaque observation.

L'exemple suivant porte sur le même système dynamique simple issu de la
référence [Welch06]_. La différence essentielle consiste à effectuer
l'exécution d'une étape de Kalman à l'arrivée de chaque observation fournie
itérativement. Le mot-clé "*nextStep*", inclut dans l'ordre d'exécution, permet
de ne pas stocker l'ébauche en double de l'analyse précédente.

De manière entièrement similaire à la réanalyse (sachant que l'on peut afficher
des résultats intermédiaires qui sont ici omis par simplicité), l'estimation
donne les mêmes résultats lors du filtrage itératif. Grâce à ces informations
intermédiaires, on peut aussi obtenir les graphiques illustrant l'estimation de
l'état et de la covariance d'erreur *a posteriori* associée.
