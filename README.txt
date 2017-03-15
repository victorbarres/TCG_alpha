Date: 2014_04_28
Author: Victor Barres
Email: barres@usc.edu
University of Southern California
USC Brain Project and USC Neuroscience

Template Construction Grammar (alpha)

TCG_alpha is the python re-implementation of Jinyong Lee TCG c++ code.

Bibliographic references to this work:
Arbib, M.A., Lee, J., 2007. Vision and action in the language-ready brain: from mirror neurons to SemRep.
Arbib, M.A., Lee, J., 2008. Describing visual scenes: Towards a neurolinguistics based on construction grammar
Barres, V. & Lee, J.  2012. Template Construction Grammar: From visual scene description to language comprehension and agrammatism
*Lee, J. 2012. Linking eyes to mouth: a schema-based computational model for describing visual scenes (Thesis)

(* = Main reference)


Notes:

construction.py
    - VOCAB class was renamed GRAMMAR

loader.py
        - The scene.txt format has been modified. Keyword "update" added to distinguish between use of "perceive"
        Now use:
        perceive { SCHEMA1, SCHEMA2, SCHEMA3 }
        update { SCHEMA1 = CONCEPT1, SCHEMA2 = CONCEPT2 }
            UPDATE IS NOT THE PROPER TERM!
        - Does not handle image name contain space (C++ code does)
  
concept.py
    - SEM_NET.ROOT() method was not implemented as it seems to be deprecated
    - SEM_NET.Explore() method was not implemented as it seems to be deprecated

simulator.py
    TO DO:
        - Check in produce utterance if the number of syllable cannot be more simply computed using synform.num_syllables.
        - Finish DOCSTRINGS