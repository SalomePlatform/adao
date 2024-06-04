.. index:: single: Convergence on residue or number criteria

- The methods proposed by this algorithm **achieve their convergence on one or
  more residue or number criteria**. In practice, there may be several
  convergence criteria active simultaneously.

  The residue can be a conventional measure based on a gap (e.g.
  "*calculation-measurement gap*"), or be a significant value for the algorithm
  (e.g. "*nullity of gradient*").

  The number is frequently a significant value for the algorithm, such as a
  number of iterations or a number of evaluations, but it can also be, for
  example, a number of generations for an evolutionary algorithm.

  Convergence thresholds need to be carefully adjusted, to reduce the gobal
  calculation cost, or to ensure that convergence is adapted to the physical
  case encountered.
