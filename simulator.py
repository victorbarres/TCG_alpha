# -*- coding: utf-8 -*-
"""
Created on Fri May 09 13:49:40 2014

@author: Victor Barres

Define the simulator that runs the SemRep/TCG processes.
"""

import concept as cpt
import construction as cxn
import scene as scn
import instance as inst
import random

class COMP_TRACE:
    """
    Competition trace
    
    IMCOMPLETE!!!
    
    Data:
        - winner (CXN_INST):
        - loser (CXN_INST):
        - winSuit (INT):
        - losSuit (INT):
    """
    def __init__(self):
        self.winner = None
        self.loser = None
        self.winSuit = 0
        self.losSuit = 0

class SIMULATOR:
    """
    INCOMPLETE!!!
    
    Data:
        <LONG TERM MEMORY>
        - SemNet (SEM_NET): Semantic network (world knowledge)
        - grammar (GRAMMAR): Grammatical knowledge
        
        <VISUAL INPUT>
        - scene (SCENE): Currently viewed scene
        
        <VISION SYSTEM>
        - atten (REGION): Region currently under attentional focus
        - next_atten (REGION): Next attention focus
        - vis_update (BOOL): Visual update flag
        - per_regions ([REGION]): Already perceived regions
        
        <LANGUAGE SYSTEM>
        - utter (STR): Produced utterance
        - incomp_utter (BOOL): Incomplete utterance flag
        - rd_str (CXN_STRUCT): Read-out construction structure
        - rd_phons ([TP_PHON]): Read-out phonetic notations
        
        <WORKING MEMORY>
        - instances ([SCHEMA_INST]): All schema instances
        - sem_insts ([SEMREP_INST]): All SemRep instances
        - cxn_insts ([CXN_INST]): All construction instances
        - cxn_strs ([CXN_STRUCT]): All construction structures        
        - comp_traces ([COMP_TRACE]): Competition traces
        
        <SIMULATION PARAMETERS>
        - time (INT):  Current simulation time (in relative unit)
        - max_time (INT): Max simulation duration
        - utter_time (INT): Last utterance production time
        
        <THRESHOLD OF UTTERANCE>
        - thresh_time (INT): Time threshold (-1 for infinity)
        - thresh_cxn (INT): Construction number limit (-1 for infinity)
        - thresh_syll (INT): Syllable length limit (-1 for infinity)
        
        <TCG PRINCIPLE FLAGS>
        - prema_prod (BOOL): Premature production principle
        - utter_cont (BOOL): Utterance continuity principle
        - verb_guide (BOOL): Verbal guidance principle
    """
    def __init__(self):
        self.SemNet = None
        self.grammar = None
        
        self.scene = None
        
        self.atten = None
        self.next_atten = None
        self.vis_update = True
        self.per_regions = []
        
        self.utter = ''
        self.incomp_utter = False
        self.rd_str = None
        self.rd_phons = []
        
        self.instances = []
        self.sem_insts = []
        self.cxn_insts = []
        self.cxn_strs = []
        self.comp_traces =[]
        
        self.time = 0
        self.max_time = 0
        self.utter_time = 0
        
        self.thresh_time = 0
        self.thresh_cxn = 0
        self.thresh_syll= 0
        
        self.prema_prod = False
        self.utter_cont = False
        self.verb_guide = False
    
    def initialize(self, maxTime, threshTime, threshCxn, threshSyll,
                   premaProd, utterCont, verbGuide, clearData):
        """
        Initialize the simulator.
        
        Args:
            - maxTime (INT): Max simulation duration
            - threshTime (INT): Time threshold (-1 for infinity)
            - threshCxn (INT): Construction number limit (-1 for infinity)
            - threshSyll (INT): Syllable length limit (-1 for infinity)
            - premaProd (BOOL): Premature production principle
            - utterCont (BOOL): Utterance continuity principle
            - verbGuide (BOOL): Verbal guidance principles
            - clearData (BOOL): If True, grammatical knowlegde, semantic knowledge and visual input are cleared.
        """
        self.time = 0
        self.max_time = maxTime
        self.utter_time = self.m_time
        self.comp_traces = []
        
        self.thresh_time = threshTime
        self.thresh_syll = threshSyll
        self.thresh_cxn = threshCxn
        
        self.prema_prod = premaProd
        self.utter_cont = utterCont
        self.verb_guide = verbGuide
        
        self.atten = None
        self.next_atten = None
        self.vis_update = True
        self.per_regions = []
        
        self.utter = ''
        self.incomp_utter = False
        self.rd_str = []
        self.rd_phons = []
        
        self.instances = []
        self.sem_insts = []
        self.cxn_insts = []
        
        if clearData:
            self.SemNet = None
            self.grammar = None
            self.scene = None
        
    ###########################################################################
    # Private methods
    def _randmax(i, j):
        if i > j:
            return 0
        elif i < j:
            return 1
        else:
            return random.randint(0,1)
    
    def add_schema_inst(self, sc_inst):
        """
        Add a schema instance to the working memory
        
        Args:
            - sc_inst (SCHEMA_INST)
        """
        
        if not(sc_inst):
            return
        
        if (sc_inst.type == inst.SCHEMA_INST.NODE or sc_inst.type == inst.SCHEMA_INST.RELATION):
            self.instances.append(sc_inst)
            self.sem_insts.append(sc_inst)
        elif (sc_inst.type == inst.SCHEMA_INST.CONSTRUCTION):
            self.instances.append(sc_inst)
            self.cxn_insts.append(sc_inst)
    
    def ellapsed_time(self):
        """
        Maintenance process.
        Steps:
            - Set cxn_inst with activity <= 0 to dead
            - Set old cxn_inst to activity = 0 (old means it has been read out)
            - Set cxn_inst to Fresh = False (Fresh only when it has just been invoked)
            - Validate all instances
            - Remove dead instances
            - Advance time
        """
        for sc_inst in self.instances:
            if not(sc_inst.alive):
                continue
            
            # When activation drops to zero, an instance dies
            if (sc_inst.activation <= 0):
                sc_inst.Alive(False)
            
            # When old, activation falls down (to 0)
            if (sc_inst.old):
                sc_inst.activation = 0
                # Employ a more subtle policy later for treating already produced instances
            
            # Not fresh anymore
            sc_inst.Fresh(False)
        
        # Validate all instances (iteratively find dead ones)
        while True:
            someone_died = False
            for sc_inst in self.instances:
                if not(sc_inst.alive):
                    continue
                
                #  Do maintenance
                sc_inst.validate()
                someone_died = someone_died or not(sc_inst.alive)
            if not(someone_died):
                break
        
        # Remove dead instances
        for sc_inst in self.instances:
            if not(sc_inst.alive):
                if(sc_inst in self.sem_insts):
                    self.sem_insts.remove(sc_inst)
                if(sc_inst in self.cxn_insts):
                    self.cxn_insts.remove(sc_inst)
                if(sc_inst in self.rd_str.insts):
                    self.rd_str.insts.remove(sc_inst)
                
                self.instances.remove(sc_inst)
        
        # Advance time
        self.time += 1
                
    
    def deploy_attention(self):
        """
        WRITE DOCSTRING!!
        """
        # Visual update
        self.vis_update = True
        
        # Set the current attention focus
        self.atten = self.next_atten
        
        # Inspect region (incrementally reduce uncertainty)
        if self.atten or self.atten.uncertainty>0:
            self.atten.uncertainty -= 1
        
        # Find the next target (if no region curently inspected or no uncertainty anymore)
        if (not(self.atten) or self.atten <=0):
            
            # Saccade to the most salient region
            max_saliency = 0
            for reg in self.scene.regions:
                if(reg.uncertainty <=0):
                    continue # Already inspected, inhibition of return
            
                if self._randmax(max_saliency, reg.saliency) == 1:
                    max_saliency = reg.saliency
                    self.next_atten = reg
            
            if max_saliency <=0:
                self.vis_update = False # No more region to attend
                self.next_atten = None
                
    
    def get_semrep_inst(self, percept_schema):
        """
        Look for the SemRep instance linked to a given perceptual schema.
        Return the SemRep instance if it exists, None otherwise.
        """
        for s in self.sem_insts:
            if not(s.alive):
                continue
            if s.percept_schema == percept_schema:
                return s
        return None
    
    def perceive_schema(self, aPercept, new_rels):
        """
        For a given percept, update or create associated SemRep nodes and relations.
        
        Notes:
            - Updated or created relations will be added to new_rels.
        """
        if not(aPercept):
            return
        
        if (aPercept.schema.type == scn.SCHEMA.OBJECT):
            node = self.get_semrep_inst(aPercept.schema)
            if node:
                # Update node instance
                if aPercept.replace_concept:
                    node.Update(aPercept.concept)
                else:
                    node.Update(aPercept.schema.concept)
            else:
                # Create new node instance
                node = inst.NODE_INST()
                node.Instantiate(aPercept.schema, 100)
                if aPercept.replace_concept:
                    node.Update(aPercept.concept)
                
                self.add_schema_inst(node)
        if (aPercept.schema.type == scn.SCHEMA.RELATION):
            relation = self.get_semrep_inst(aPercept.schema)
            if relation:
                # Update relation instance
                if aPercept.replace_concept:
                    relation.Update(aPercept.concept)
                else:
                    relation.Update(aPercept.schema.concept)
            else:
                # Create new relation instance
                relation = inst.REL_INST()
                relation.Instantiate(aPercept.schema, 100)
                if aPercept.replace_concept:
                    relation.Update(aPercept.concept)
                
                self.add_schema_inst(relation)
                self.new_rels.append(relation)
        
    def perceive_scene(self):
        """
        Perceive all regions that are certain (uncertainty == 0).
        """
        new_rels = []
        
        # Reset perceived regions
        self.per_regions = []
        
        # Perceive regions that are certain (uncertainty == 0)
        for rgn in self.scene.regions:
            if rgn.uncertainty == 0:
                # Perceive schemas
                for percept in rgn.percepts:
                    self.perceive_schema(percept, new_rels)
                
                rgn.uncertainty -= 1 # Region won't be perceived anymore
                
                # Append traces for perceived regions
                self.per_regions.append(rgn)
        
        # Establish connection of the newly created SemRep relations
        for rel in new_rels:
            sc_rel = rel.schema
            
            # Connect node instances
            rel.pFrom  = self.get_semrep_inst(sc_rel.pFrom)
            rel.pTo = self.get_semrep_inst(sc_rel.pTo)
            
            # Alive only when the full connection is valid
            rel.Alive(rel.pFrom and rel.pTo)
    
    def pair_node(self):
        """
        """
        return None
        
    def invoke_cxn_inst(self):
        """
        """
        return None
    
    def invoke_constructions(self):
        """
        """
        return None
    
    def find_cxn_struct(self):
        """
        """
        return None
    
    def do_cooperation(self):
        """
        """
        return None
    
    def create_comp_trace(self):
        """
        """
        return None
    
    def do_competition(self):
        """
        """
        return None
    
    def process_constructions(self):
        """
        """
        return None
    
    def match_phon_lists(self):
        """
        """
        return None
    
    def produce_utterance(self):
        """
        """
        return None
    
    ###########################################################################
    # Public method
    
    def proceed(self):
        """
        WRITE DOCSTRING
        """
        if (self.time >= self.max_time):
            return False
        
        # Maintenance processes
        self.ellapsed_time()
        
        # Vision processes
        self.deploy_attention()
        self.perceive_scene()
        
        # TCG processes
        self.invoke_constructions()
        self.process_constructions()
        
        # Utterance processes
        self.produce_utterance()
        
        return (inst.SCHEMA_INST.inst_activity or self.vis_update)
    
###############################################################################

if __name__=='__main__':
    print "No test case implemented"
    
        
        
        
        
    
