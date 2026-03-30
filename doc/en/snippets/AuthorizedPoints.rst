.. index:: single: AuthorizedPoints

AuthorizedPoints
  *List of integer series*. Each element is a series, containing the indices of
  the points allowed for the optimal search, according to the order of the
  variables of a state vector considered arbitrarily in one-dimensional form.
  By default, when all points are implicitly allowed, the set is empty.

  Example :
  ``ep = ADD.get("AuthorizedPoints")[-1]``
