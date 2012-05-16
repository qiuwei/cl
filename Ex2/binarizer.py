#!/usr/bin/python
'''
Created on May 16, 2012

@author: Ehsan Khoddammohammadi
'''
import sys

joiner_string = "#"
def left_binarize(rule):
    #rule is tuple, first element is LHS and second element is list of constituents as RHS
    LHS = rule[0]
    RHS_list = rule[1]
#    print LHS,"--> ",RHS_list
    if len(RHS_list)>2 :
        new_RHS = [joiner_string.join(RHS_list[0:-1])]
        new_RHS.append(RHS_list[-1])
        first_new_rule = (LHS, new_RHS )
        second_new_rule = (joiner_string.join(RHS_list[0:-1]), RHS_list[0:-1])
        new_rules = []
        new_rules = new_rules + left_binarize (second_new_rule)
        new_rules.append( first_new_rule )
        
        return new_rules
    else:
        new_rules=[]
        new_rules.append(rule)
#        print new_rules,"else"
        return new_rules
def right_binarize(rule):
    #rule is tuple, first element is LHS and second element is list of constituents as RHS
    LHS = rule[0]
    RHS_list = rule[1]
#    print LHS,"--> ",RHS_list
    if len(RHS_list)>2 :
        new_RHS=[]
        new_RHS.append(RHS_list[0])
        new_RHS.append(joiner_string.join(RHS_list[1:]))
        
        first_new_rule = (LHS, new_RHS )
        second_new_rule = (joiner_string.join(RHS_list[1:]), RHS_list[1:])
        new_rules = []
        new_rules = new_rules + right_binarize (second_new_rule)
        new_rules.append( first_new_rule )
        
        return new_rules
    else:
        new_rules=[]
        new_rules.append(rule)
#        print new_rules,"else"
        return new_rules        
    
def rule_reader(file_path):
    fin = open(file_path,'r')
    rules=[]
    for line in fin:
        tokens = line.split()
        LHS = tokens[0]
        RHS_list = tokens[1:]
        rules.append((LHS,RHS_list))
    fin.close()
    return rules

def binarize (rules,method='left'):
    binarized_rules = list()
    if (method!='right'):
        for rule in rules:
            for new_rule in left_binarize(rule):
                binarized_rules.append(new_rule)
    else:
        for rule in rules:
            for new_rule in right_binarize(rule):
                binarized_rules.append(new_rule)
    return binarized_rules

def show(binarized_rules):
    strings = []
    for rule in binarized_rules:
        strings.append(rule[0]+'\t'+rule[1][0]+'\t'+rule[1][1]+'\n')   
    return strings 
        
if __name__ == '__main__':
    #rule = ('S', ['NP','VP', 'VP','DP'])
    #print left_binarize(rule)
    if (len(sys.argv)>2):
        file_name = sys.argv[1]
        method = sys.argv[2]
    else:
        print "first_argument=pathToGrammar  second_argument=left[,right]"
        sys.exit(1)
    rules = rule_reader(file_name)
    binarized_rules = binarize(rules, method)
    
    for rule in show(binarized_rules):
        print rule