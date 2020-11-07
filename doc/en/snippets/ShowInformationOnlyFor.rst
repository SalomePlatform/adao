.. index:: single: ShowInformationOnlyFor

ShowInformationOnlyFor
  *List of predefined names*. This key indicates the list of vector names whose
  summarized information (size, min/max...) is to be printed, the default value
  being the set of vectors. If the named vector is not a provided entry, the
  name is simply ignored. This allows you to restrict summarized printing. The
  possible names are in the following list: [
  "Background",
  "CheckingPoint",
  "Observation",
  ].

  Exemple :
  ``{"ShowInformationOnlyFor":["Background"]}``
