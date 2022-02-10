.. index:: single: Observation

Observation
  *Liste de vecteurs*. La variable désigne le vecteur d'observation utilisé en
  assimilation de données ou en optimisation, et usuellement noté
  :math:`\mathbf{y}^o`. Sa valeur est définie comme un objet de type "*Vector*"
  si c'est une unique observation (temporelle ou pas) ou "*VectorSerie*" si
  c'est une succession d'observations. Sa disponibilité en sortie est
  conditionnée par le booléen "*Stored*" associé en entrée.
