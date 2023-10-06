.. index:: single: SingularValues

SingularValues
  *List of real value series*. Each element is a series, containing the
  singular values obtained through a SVD decomposition of a collection of full
  state vectors. The number of singular values is not limited by the requested
  size of the reduced basis.

  Example :
  ``sv = ADD.get("SingularValues")[-1]``
