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
        """
        return None
    
    def deploy_attention(self):
        """
        """
        return None
    
    def get_semrep_inst(self, aSchema):
        """
        """
        return None
    
    def perceive_schema(self, aPer, new_rels):
        """
        """
        return None
        
    def perceive_scene(self):
        """
        """
        return None
    
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
    
        
        
        
        
    
