.. index:: single: InnovationAtCurrentAnalysis

InnovationAtCurrentAnalysis
  *List of vectors*. Each element is an innovation vector at current analysis.
  This quantity is identical to the innovation vector at current state in the
  case of a single-state assimilation.

  Example:
  ``ds = ADD.get("InnovationAtCurrentAnalysis")[-1]``
