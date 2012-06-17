#!/usr/bin/python2
#-*-coding:utf-8-*-
'''
Created on Jun 15, 2012

@author: wqiu
'''

import os, sys, collections, math

class PCYKParser(object):
    '''
    CYK algorithm implmentation with probability
    '''
    #data structure for binarized grammar
    grammar = collections.defaultdict(list)

    def __init__(self):
        '''
        Constructor
        '''
        
    def read_in_grammar(self, grammar_file, lexicon_file=None):
        with open(grammar_file) as f:
            for line in f:
                tokens = line.strip().split()
                tokens_length = len(tokens)
                #binarized rule:
                if tokens_length == 4:
                    self.grammar[(tokens[1], tokens[2])].append([tokens[0], math.log(float(tokens[3]))])
                #not binarized rule
                elif tokens_length > 4:
                    self.grammar[(tokens[1], '#'.join(tokens[2:-1]))].append([tokens[0],math.log(float(tokens[-1]))])
                    self.binarize(tokens[2:-1])
                #dictionary entry
                else:
                    self.grammar['_' + tokens[1]].append([tokens[0],math.log(float(tokens[2]))])
            # if separated lexicon file is provided
        if lexicon_file != None:
            with open(lexicon_file, 'r') as f:
                for line in f:
                    tokens = line.strip().split()
                    self.grammar['_' + tokens[1]].append([tokens[0], math.log(float(tokens[2]))])
                
    # method to binarize the grammar            
    def binarize(self, tokens):
        if len(tokens) == 1:
            return tokens[0]
        else:
            s2 = self.binarize(tokens[1:])
            s0 = tokens[0] + '#' + s2
            self.grammar[(tokens[0], s2)].append([s0, 0])
            return s0
            
    def _parse(self, sentence):
        tokens_sent = sentence.lower().strip().split()
        self.chart = [[list() for i in range(len(tokens_sent))] for j in range(len(tokens_sent))]
        len_sent = len(tokens_sent)
        #initialize the chart, put dictionary item in the diagon
        for i in range(len_sent):
            #print self.chart
            #use -1 to indicate the boundary
            # use 4 tuple to as a pointer to the right hand sand term
            # (lefthand side, midindex, lefthandside1, lefthandside2)
            #print self.chart[i][i]
            for key in self.grammar['_'+tokens_sent[i]]:
                self.chart[i][i].append([key, -1, '', '' ])

        for len_chart in range(2,1+len_sent):
            for start_pos in range(len_sent-len_chart+1):
                for mid_pos in range(start_pos+1, start_pos+len_chart):
                    for r1 in self.chart[start_pos][mid_pos - 1]:
                        for r2 in self.chart[mid_pos][start_pos + len_chart - 1]:
                            if (r1[0][0], r2[0][0]) in self.grammar:
                                # get all possible combination from r1, r2
                                left = self.grammar[(r1[0][0], r2[0][0])]
                                # put it in the chart
                                for leftitem in left:
                                    try:
                                        i = map(lambda x: x[0][0], self.chart[start_pos][start_pos + len_chart-1]).index(leftitem[0])
                                        # if we find a more possible substring parse, then replace the parsing result
                                        if r1[0][1] + r2[0][1] + leftitem[1] > self.chart[start_pos][start_pos + len_chart - 1][i][0][1]:
                                            self.chart[start_pos][start_pos + len_chart - 1][i] = [leftitem, mid_pos, r1[0], r2[0]]
                                    except ValueError:
                                        self.chart[start_pos][start_pos + len_chart - 1].append([leftitem, mid_pos, r1[0], r2[0]])
 
    def parse(self, sentence, verbose='T'):
        self._parse(sentence)
        for x in self.chart[0][-1]:
            if 'S' == x[0][0]:
                if verbose == 'T':
                    self._print(0, len(self.chart), 'S')
                print('The sentence can be passed successfully!')
                return True
        print 'The sentence can not be passed successfully!'
        return False

    def _print(self, i, j, sym):
        #print 'calling _print( %d , %d, '%(i,j) + sym +')'
        # end printing
        if j-i == 1:
            print i, j, sym
        else:
            lx = [y for y in self.chart[i][j-1] if sym == y[0][0]]
            for x in lx:
                if not '#' in sym:
                    print i, j, sym
                self._print(i, x[1], x[2][0])
                self._print(x[1], j, x[3][0])
 
if __name__ == '__main__':
    p = PCYKParser()
    p.read_in_grammar('simplegrammar')
    p.parse("The student reads a book in the library")
    p.parse("The student reads a book")
    p.parse("The student book a book")
    
    p1 = PCYKParser()
    p1.read_in_grammar('rules', 'lexicon')
    p1.parse("The reason was not high interest rates or labor costs")
    p1.parse("Many other factors played a part in yesterday 's comeback")