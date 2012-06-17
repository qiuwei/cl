'''
Created on Jun 16, 2012

@author: wqiu
'''

class PCFGLearner(object):
    '''
    Learn PCFG from frequency data
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def learn(self, in_file_name, out_file_name):
        with open(in_file_name, 'r') as fin:
            with open(out_file_name, 'w') as fout:
                l1 = [lines.strip().split() for lines in fin]
                lc = [x[1] for x in l1]
                countdict = {}
                for item in l1:
                    try:
                        total_num = countdict[item[1]]
                        fout.write(' '.join(item[1:]) + ' ' + str(float(item[0])/total_num) + '\n')
                    except KeyError:
                        countdict[item[1]] = reduce(lambda x,y: x + float(y[0]), [i for i in l1 if i[1] == item[1] ], 0.0)
                        
if __name__ == '__main__':
    pl = PCFGLearner()
    pl.learn('exercise7-lexicon.txt', 'lexicon')
    pl.learn('exercise7-rules.txt', 'rules')
        