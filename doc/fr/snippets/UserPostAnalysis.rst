.. index:: single: UserPostAnalysis
.. index:: single: UserPostAnalysis Template

UserPostAnalysis
  *Chaîne de caractères multi-lignes*. La variable permet de traiter des
  paramètres ou des résultats après le déroulement de l'algorithme
  d'assimilation de données ou d'optimisation. Sa valeur est définie soit par
  un nom de patron prédéfini, soit par nom de un fichier script, soit par une
  chaîne de caractères, permettant de produire directement du code de
  post-processing dans un cas ADAO. Des exemples courants (squelettes ou
  "templates") sont fournis pour aider l'utilisateur ou pour faciliter
  l'élaboration d'un cas. Remarque importante : ce traitement n'est exécuté que
  lorsque le cas est exécuté en TUI ou exporté en YACS.
