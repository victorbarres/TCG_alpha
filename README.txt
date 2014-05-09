Date: 2014_04_28
Author: Victor Barres
Email: barres@usc.edu
University of Southern California
USC Brain Project and USC Neuroscience

Template Construction Grammar 1.0

TCG 1.0 is the python re-implementation of Jinyong Lee TCG c++ code.

Bibliographic references to this work:
Arbib, M.A., Lee, J., 2007. Vision and action in the language-ready brain: from mirror neurons to SemRep.
Arbib, M.A., Lee, J., 2008. Describing visual scenes: Towards a neurolinguistics based on construction grammar
Barres, V. & Lee, J.  2012. Template Construction Grammar: From visual scene description to language comprehension and agrammatism
*Lee, J. 2012. Linking eyes to mouth: a schema-based computational model for describing visual scenes (Thesis)

(* = Main reference)


###############################################################################
# Done
###############################################################################

construction.py
    - VOCAB class was renamed GRAMMAR

    TO_DO:
        - Add test cases

    TO IMPROVE:
        - Introduce symbolic link elements

instance.py
    TO DO:
        - Check the check_lineage method of CXN_STRUCT. Not sure what it is useful for....

    TO IMPROVE:
        - It seems that semantic distance does not matter in the current version
        (concept match or don't match). Introduce quality of matching.
        See CXN_STRUCT.create()
        - Might improve the parameters that enter in the calculus of suitability.
        - Think about how this integrates with the requirement to implement dynamic C2 computation.
        - See how merge can be generalized (i.e. bring together Merge and Combine.)

scene.py

loader.py

###############################################################################
# In progress
###############################################################################

concept.py
    - SEM_NET.ROOT() method was not implemented as it seems to be deprecated
    - SEM_NET.Explore() method was not implemented as it seems to be deprecated
    - CONCEPT.Create() method might need to be revisited...

    TO DO:
        - CONCEPT.Match() method is INCOMPLETE. Need to clarify some elements in Jin's code.

    TO IMPROVE:
        - Implement SEM_NET as a graph

simulator.py
    TO DO:
        - Finish the docstring of COMP_TRACE