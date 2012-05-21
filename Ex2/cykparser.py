#!/usr/bin/python
#-*-coding:utf-8-*-

import os, sys,collections


class CYKParser(object):
    
    def __init__(self, grammar_file):
        self.grammar = collections.defaultdict(set)
        f = file(grammar_file)
        for line in f:
            tokens = line.strip().split()
            if len(tokens) == 3:
                self.grammar[(tokens[1], tokens[2])].add(tokens[0])
            else:
                # add _ before dictionary item to distinguish between dictionary and gramamr rules
                self.grammar['_' + tokens[1]].add(tokens[0])

    def _parse(self, sentence):
        tokens_sent = sentence.lower().strip().split()
        self.chart = [[set() for i in range(len(tokens_sent))] for j in range(len(tokens_sent))]
        len_sent = len(tokens_sent)
        #initialize the chart, put dictionary item in the diagon
        for i in range(len_sent):
            #print self.chart
            #use -1 to indicate the boundary
            # use 4 tuple to as a pointer to the right hand sand term
            # (lefthand side, midindex, lefthandside1, lefthandside2)
            #print self.chart[i][i]
            for key in self.grammar['_'+tokens_sent[i]]:
                self.chart[i][i].add((key, -1, '', ''))

        for len_chart in range(2,1+len_sent):
            for start_pos in range(len_sent-len_chart+1):
                for mid_pos in range(start_pos+1, start_pos+len_chart):
                    for r1 in self.chart[start_pos][mid_pos - 1]:
                        for r2 in self.chart[mid_pos][start_pos + len_chart - 1]:
                            try:
                                # get all possible combination from r1, r2
                                left = self.grammar[(r1[0], r2[0])]
                                # put it in the chart
                                for leftitem in left:
                                    self.chart[start_pos][start_pos + len_chart
                                            -1].add((leftitem, mid_pos, r1[0], r2[0]))
                            except KeyError:
                                pass


    def parse(self, sentence, verbose='T'):
        self._parse(sentence)
        for x in self.chart[0][-1]:
            if 'S' in x:
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
            lx = [y for y in self.chart[i][j-1] if sym in y]
            if len(lx) > 1:
                print 'Ambiguity occurs!'
            for x in lx:
                print i, j, sym
                self._print(i, x[1], x[2])
                self._print(x[1], j, x[3])
        



if __name__ == '__main__':
    p = CYKParser('grammar.txt')
    p.parse("The boy shot an elephant  in his pajamas", 'T')
