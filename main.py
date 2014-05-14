# -*- coding: utf-8 -*-
"""
Created on Tue May 13 15:02:26 2014

@author: Victor Barres
"""
import loader as LD
import simulator as SIM
import instance as INST
import construction as CXN
import scene as SCN
import concept as CPT

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
#    p += str(sr_inst.percept_schema.name)
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
            p += sim.per_regions.name
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
                if sc_inst.pTp:
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
    
    p += "> Next Attention\n"
    p += "  %s\n" % print_region(sim.next_atten)
    return p
        
                
                
                
                
    
    
        
        
    
    

if __name__=='__main__':
    print 'Main prgm here...!'

