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
    NOTES:
        - Compared to C++, the scene.txt format has been modified. Keyword "update" added to distinguish between use of "perceive"
        Now use:
        perceive { SCHEMA1, SCHEMA2, SCHEMA3 }
        update { SCHEMA1 = CONCEPT1, SCHEMA2 = CONCEPT2 }
            UPDATE IS NOT THE PROPER TERM!

        - Does not handle image name contain space (C++ code does)
    TO IMPROVE:
        - Migrate data storage format to Json for clarity.

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
        - FINISH process_constructions()
        - Check in produce utterance if the number of syllable cannot be more simply computed using synform.num_syllables.

    TO IMPROVE:
        - Subgraph matching algorithm (invoke_cxn_inst).
        - Concept matching (inb invoke_cxn_inst) is binary and could be improved.
        - Produce utterance:
            - the number of cxn-inst taken into consideration with respect to the thresh_cxn is the total number of cxn_inst in self.cxn_insts...
                might be better to look at each structure independently.
            - similarly for total syllable length: the number of syllables in all the cxn_inst that are in WM are summed...
                might be better to look at the syllable length of each structure...
            

main.py