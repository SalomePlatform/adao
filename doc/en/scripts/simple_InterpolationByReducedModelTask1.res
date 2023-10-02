Defining a set of artificial physical fields
--------------------------------------------
- Dimension of physical field space....................: 7
- Number of physical field vectors.....................: 7

Search for optimal measurement positions
-------------------------------------------
- ADAO calculation performed

Display of optimal positioning of measures
------------------------------------------
- Number of optimal measurement positions..............: 2
- Optimal measurement positions, numbered by default...: [6 0]

Reconstruction by interpolation of known measured states
--------------------------------------------------------
- Reference state 1 used for the learning..............: [1 2 3 4 5 6 7]
- Optimal measurement positions, numbered by default...: [6 0]
- Measures extracted from state 1 for reconstruction...: [7 1]
- State 1 reconstructed with the precision of 1%.......: [1. 2. 3. 4. 5. 6. 7.]
  ===> There is no difference between the two states, as expected

Reconstruction by interpolation of unknown measured states
----------------------------------------------------------
  Illustration of an interpolation on unknown real measurements
- Optimal measurement positions, numbered by default...: [6 0]
- Measures not present in the known states.............: [4 3]
- State reconstructed with the precision of 1%.........: [3.    3.167 3.333 3.5   3.667 3.833 4.   ]
  ===> At measure positions [6 0], the reconstructed field is equal to measures

