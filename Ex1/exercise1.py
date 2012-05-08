import collections

class DFA:
    def __init__(self, start, final, transitions):
        self.start = start
        self.final = set(final)
        self.transitions = dict()
        for (src, char, tgt) in transitions:
            self.transitions[(src, char)] = tgt
    
    def recognize(self, string):
        state = self.start
        for char in string:
            try:
                state = self.transitions[(state, char)]
            except KeyError:
                return False
        return state in self.final

def test_dfa():
    # the automaton on slide 7, without "failure" state
    dfa = DFA(0, [0, 2, 3], [(0, 'a', 1), (1, 'b', 2), (2, 'a', 3), (3, 'a', 1), (3, 'b', 2)])
    for test in ['ababa', 'babba', 'abaa']:
        print(test, dfa.recognize(test))



class NFA:
    def __init__(self, start, final, transitions):
        self.start = start
        self.final = final
        self.transitions = collections.defaultdict(set)
        for (src, char, tgt) in transitions:
            self.transitions[(src, char)].add(tgt)
    
    def alphabet(self):
        '''returns the alphabet'''
        return set(char for (src, char) in self.transitions if char != '')
    
    def recognize(self, string):
        # your code
        conf = (-1, "")
        agenda = [(self.start, string)]
        while agenda:
            tempconf = agenda.pop()
            if conf == tempconf:
                continue
            conf = tempconf
            if conf[1] == "":
                if conf[0] in self.final:
                    return True
            else:
                for state in self._move([conf[0]], conf[1][0]):
                    agenda.append((state, conf[1][1:]))
        return False

         
    def closure(self, state):
        '''returns all states reachable by 'state' using zero or more e-transitions'''
        reachable = [state]
        agenda = [state]
        while agenda:
            state = agenda.pop()
            for other in self.transitions[(state, '')]:
                if other not in reachable:
                    reachable.append(other)
                    agenda.append(other)
        # frozensets are like sets, but cannot be modified. Also, frozensets can be
        # used as keys in dictionaries and as elements of other sets
        return frozenset(reachable)
    
    def _closure(self, states):
        result = set()
        for state in states:
            result.update(self.closure(state))
        return frozenset(result)
    
    def _move(self, states, char):
        result = set()
        for state in states:
            result.update(self.transitions[(state, char)])
        return frozenset(result)
    
    def dfa(self):
        # start = ...
        # transitions = ...
        # final = ...
        # ...
        # return DFA(start, final, transitions)
        start_closure = self.closure(self.start)
        final = []
        agenda = []
        label = 0
        agenda.append((start_closure,label))
        k = dict()
        transitions = list()
        while agenda:
            # mark T
            t = agenda.pop()
            k[t[0]] = t[1] 
            for char in self.alphabet():
                u = self._closure(self._move(t[0], char))
                if u not in k:
                    label = label + 1
                    agenda.append((u, label))
                    transitions.append((t[1], char, label))
                else:
                    transitions.append((t[1], char, k[u]))
        for f in self.final:
            final.extend([k[state] for state in k if f in state])
        start = k[start_closure]
        return DFA(start, final, transitions)


def test_nfa():
    nfa = NFA(0, [0, 2], [(0, 'a', 1), (1, 'b', 2), (2, 'a', 1), (1, 'b', 3), (3, 'a', 2)])
    dfa = nfa.dfa()
    for test in ['ab', 'aba', 'abaaba', 'abba', 'aabab']:
        print(test, nfa.recognize(test), dfa.recognize(test))

if __name__ == '__main__':
    test_dfa()
    test_nfa()
