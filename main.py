# -*- coding: utf-8 -*-
"""
Created on Tue May 13 15:02:26 2014

@author: Victor Barres
"""
import sys

import loader as LD
import simulator as SIM
import instance as INST
import construction as CXN

TCG_ABOUT = "Template Construction Grammar (TCG) Simulator v1.0\n\
\n\
Victor Barres (barres@usc.edu) May 14. 2014\n\
USC Brain Project and  Neuroscience Graduate Program\n\
University of Southern California (USC)\n\
[PYTHON reimplementation of c++ code:\n\
\tTemplate Construction Grammar (TCG) Simulator v2.5\n\
\tJinyong Lee (jinyongl@usc.edu), June 23. 2012\n\
\tUSC Brain Project, Computer Science Department\n\
\tUniversity of Southern California (USC)]\n"


def print_inst_status(sc_inst):
    p = ''
    p += "["
    if sc_inst.fresh:
        p += "!"
    else:
        p += " "
    if not(sc_inst.alive):
        p += "X"
    else:
        if sc_inst.activation>0:
            if sc_inst.old:
                p += "@"
            else:
                p += "x"
    p += "]"
    return p

def print_struct_status(cxn_str, rd_str):
    p = ''
    if cxn_str.valid:
        if rd_str.compare(cxn_str) == 3:
            p += "*"
        else:
            p += " "
    else:
        p += "X"
    p += "]"
    p += str(cxn_str.suitability) + ": "
    return p

def print_semrep_inst(sr_inst):
    p = ''
#    p += str(sr_inst.schema.name)
    p += str(sr_inst.concept.meaning)
    p += "_" + str(sr_inst.id)
    return p
    
def print_cxn_inst(cxn_inst):
    p = ''
    p += str(cxn_inst.base_cxn.name)
    p += "_" + str(cxn_inst.id)
    return p
    
def print_cxn_struct(cxn_str, cxn_inst, recursive = True):
    p = ''    
    if recursive:
        print_cxn_inst(cxn_inst)
    
    for i in range(len(cxn_inst.base_cxn.SynForm)):
        TpSynElem = cxn_inst.base_cxn.SynForm[i]
        if TpSynElem.type == CXN.TP_ELEM.SLOT:
            p += "'%s'" % TpSynElem.phonetics
        else:
            p += "["
            if cxn_str:
                child = cxn_str.get_child(cxn_inst, i)
            else:
                child = None
            
            if child:
                if recursive:
                    print_cxn_struct(cxn_str, child, recursive)
                else:
                    print_cxn_inst(child)
            else:
                p += " "
            p += "]"
        if i < (len(cxn_inst.base_cxn.Synform) -1):
            p += " "
    
    return p
    
def print_region(rgn):
    p = ''
    if(rgn):
        p += rgn.name
        if rgn.uncertainty > 0:
            p += " (uncertainty left: %i)" % rgn.uncertainty
        else:
            p += " (perception done)"
    else:
        p += "None"
    p += "\n"
    return p

def print_current_state(sim):
    p = ''
    p += ''.join(["=" for i in range(80)]) + "\n"
    p += " Simulation Time: %i\n" % sim.time
    p += ''.join(["=" for i in range(80)]) + "\n"
    
    p += "> Current Attention\n"
    p += "  %s\n" % print_region(sim.atten)
    
    if len(sim.per_regions) > 0:
        p += "> Perceived Regions\n"
        p += "  "
        for rgn in sim.per_regions:
            if sim.per_regions.index(rgn) > 0:
                p += ", "
            p += rgn.name
        p += "\n\n"
    
    if len(sim.instances) > 0:
        p += "> Schema Instances\n"
        for sc_inst in sim.instances:
            p += print_inst_status(sc_inst)
            
            if sc_inst.type == INST.SCHEMA_INST.NODE:
                p += "SemRep-N "
                p += "%s\n" % print_semrep_inst(sc_inst)
            
            elif sc_inst.type == INST.SCHEMA_INST.RELATION:
                p += "SemRep-R "
                p += print_semrep_inst(sc_inst)
                p += " from "
                if sc_inst.pFrom:
                    p += print_semrep_inst(sc_inst.pFrom)
                else:
                    p += "??"
                p += " tp "
                if sc_inst.pTo:
                    p += print_semrep_inst(sc_inst.pTo)
                else:
                    p += "??"
                p += "\n"
            
            elif sc_inst.type == INST.SCHEMA_INST.CONSTRUCTION:
                p += "Construction "
                p += print_cxn_inst(sc_inst)
                p += " covering "
                for i in range(len(sc_inst.covers)):
                    p += print_semrep_inst(sc_inst.covers[i])
                    p += " "
                p += "for %s\n" % print_cxn_struct(sc_inst.cxn_struct, sc_inst, False)
            
        p += "\n"
    
    if len(sim.comp_traces) > 0:
        p += "> Competition traces\n"
        for comp_tr in sim.comp_traces:
            p += "  "
            p += print_cxn_inst(comp_tr.winner)
            p += "  %s (%i) " % (print_cxn_inst(comp_tr.winner), comp_tr.winSuit)
            p += "eliminated %s (%i)\n" % (print_cxn_inst(comp_tr.loser), comp_tr.losSuit)
        
        p += "\n"
    
    if len(sim.cxn_strs) > 0:
        p += "> Construction Structures\n"
        for cxn_str in sim.cxn_strs:
            p += print_struct_status(cxn_str, sim.rd_str)
            p += print_cxn_struct(cxn_str, cxn_str.top, True)
            p + "\n"
    
    if len(sim.utter) > 0:
        p += "> Produced Utterance\n"
        p += "'%s'\n" % sim.utter
        
    p += "> Next Attention\n"
    p += "  %s\n" % print_region(sim.next_atten)
    return p

def load_init_file(file_name, sim):
    print "Loading Initialization File '%s' ...\n" % file_name
    
    try:
        f = open(file_name, 'r')
    except:
        print "\nFailed to open file '%s'.\n" % file_name
        return False
    
    f_content = f.read()
    f.close()
    f_data = f_content.splitlines()
    
    fields = {'semantics file':'', 'grammar file':'', 'scene file':'', 
              'threshold time':-1, 'threshold constructions':-1, 
              'threshold syllables':-1, 'premature production':1,
              'utterance continuity':1, 'verbal guidance':1, 'max time':100}

    comment_sign = '#'
    
    for line in f_data:
        if not(line) or line[0] == comment_sign:
            continue
        
        line_data = [t.strip() for t in line.split('=')]
        
        if len(line_data) != 2:
            print "\nInvalid command line: %s\n" % line
            return False
        
        key_word = line_data[0]
        default_value = fields.get(key_word)
        if default_value == None:
            print "\nInvalid command line: %s\n" % line
            return False
        
        fields[key_word] = line_data[1]
    
    if not(fields['semantics file'] and fields['grammar file'] and fields['scene file']):
        print "\nInput file name missing.\n"
        return False
    
    lod = LD.LOADER()
    
    okay = False
    print "Loading Semantic Network '%s'...\n" % fields['semantics file']
    mySemNet = lod.load_SemNet(fields['semantics file'])
    if mySemNet:
        print "Loading TCG Grammar '%s'...\n" % fields['grammar file']
        myGrammar = lod.load_grammar(fields['grammar file'])
        if myGrammar:
            print "Loading TCG Scene '%s'...\n" % fields['scene file']
            myScene = lod.load_scene(fields['scene file'])
            if myScene:
                okay = True
    
    if not(okay):
        print "LOADER ERROR"
        return False
    
    # Initialize simulator
    print "\nInitializing Simulator...\n"
    sim.SemNet = mySemNet
    sim.grammar = myGrammar
    sim.scene = myScene
    
    try:
        max_time = int(fields['max time'])
        thresh_time = int(fields['threshold time'])
        thresh_cxn = int(fields['threshold constructions'])
        thresh_syll = int(fields['threshold syllables'])
        prem_prod = bool(int(fields['premature production']))
        utter_cont = bool(int(fields['utterance continuity']))
        verb_guide = bool(int(fields['verbal guidance']))
    except:
        print "\nInvalid simulator parameter.\n"
        return False
    
    sim.initialize(max_time, thresh_time, thresh_cxn, thresh_syll, prem_prod, utter_cont, verb_guide)
                   
    print "- Max Simulation Time : %i\n" % sim.max_time
    print "- Premature Production : %s\n" % sim.prema_prod
    print "- Utterance Continuity : %s\n" % sim.utter_cont
    print "- Verbal Guidance : %s\n" % sim.verb_guide
    print "- Threshold of Utterance : ",
    t = ['', '', '']
    i = 0
    for val in [sim.thresh_time, sim.thresh_cxn, sim.thresh_syll]:
        if val < 0:
            t[i] = 'infinite'
        else:
            t[i] = str(val)
        
        i +=1
    print "Time = %s, CXNs = %s, Syllables = %s\n" % (t[0], t[1], t[2])
    
    return True

def main():
    print "\n%s\n" % TCG_ABOUT
    if len(sys.argv) != 2:
        print "Usage: python TCG.py initialization_file\n"
        return
    
    # Initialization
    mySim = SIM.SIMULATOR()
    
    # Load init file
    if not(load_init_file(sys.argv[1], mySim)):
        return
    
    # Simulation
    print "\nBeginning Simulation...\n"
    while (mySim.proceed(verbose = False)):
        state_report = print_current_state(mySim)
        print state_report
    
    print "\nSimulation complete: ",
    if mySim.time < mySim.max_time:
        print "inactivity termination."
    else:
        print "max time reached."
    print "\n"
    
if __name__=='__main__':
    main()

