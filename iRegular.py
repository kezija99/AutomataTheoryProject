from Node import Node
from Automata import Automata
from queue import Queue
class IRegular:
    
    @staticmethod
    def print_tree(node: Node, level: int = 0) -> None:
        if node is None:
            return
        IRegular.print_tree(node.right, level + 1)
        print(' ' * 4 * level + '->', node.data)
        IRegular.print_tree(node.left, level + 1)
    
    @staticmethod
    def REtoIR(RE: str):
        if not RE:
            raise ValueError("RE string cannot be empty!")
        if ';' in RE or ',' in RE:
            raise ValueError("RE cannot contain the ; or , symbols!")
        tree = Node.parsing_tree(RE)
        #IRegular.print_tree(tree)
        return IRegular.construct_nfa(tree)

    @staticmethod
    def construct_nfa(root):
        if not root:
            raise ValueError("Improperly parsed root cannot be None")
        l, r = None, None
        if root.data == "|":
            l = IRegular.construct_nfa(root.left)
            r = IRegular.construct_nfa(root.right)
            #return l.union(r).to_dfa().to_nfa()
            pom = l.union(r).to_dfa().to_nfa()
            return pom
        elif root.data == "•":
            l = IRegular.construct_nfa(root.left)
            r = IRegular.construct_nfa(root.right)
            #return l.concat(r).to_dfa().to_nfa()
            pom2 = l.concat(r).to_dfa().to_nfa()
            return pom2
        elif root.data == "*":
            l = IRegular.construct_nfa(root.left)
            #return l.star().to_dfa().to_nfa()
            pom3 = l.star().to_dfa().to_nfa()
            return pom3
        else:
            nf = NFA("q0", {"q1"}, {("q0", root.data): ["q1"]})
            return nf
        
class DFA(Automata, IRegular):
    def __init__(self, startState, FinalStates, Delta):
        super().__init__(startState, FinalStates, Delta)
    
    def __str__(self):
        return self.startState + ' '  + str(self.FinalStates) + ' ' + str(self.Delta)
        
    def to_nfa(self):
        return NFA(self.startState, self.FinalStates, self.Delta)
        
    def exclude_unreachable_States_and_rename(self, c='q'):
        result = self.rename_and_exclude_unreachableStates_inner(c)
        df = DFA(result[0], result[1], result[2])
        return df

    def partion_add_to_delta(self, temp, state, newDelta, partions):
        for c in temp.Alfabet:
            if temp.Delta[(state, c)]:
                result = temp.Delta[(state, c)].pop()
                for p in partions:
                    if result in p:
                        result = next(iter(p))
                newDelta[(state, c)] = set([result])
            
    def minimize_dfa(self):
        temp = self.exclude_unreachable_States_and_rename()
        non_final = set(temp.States) - set(temp.FinalStates)
       
        all_States = list(temp.States)
        table = {}
        for i in range(len(all_States)):
            for j in range(i+1, len(all_States)):
                if ((all_States[i] in temp.FinalStates and all_States[j] in non_final) or
                    (all_States[j] in temp.FinalStates and all_States[i] in non_final)):
                    table[(all_States[i], all_States[j])] = True
                else:
                    table[(all_States[i], all_States[j])] = False
        
        change = True
        while change:
            change = False
            for key, value in table.items():
                if not value:
                    for c in temp.Alfabet:
                        result1 = next(iter(temp.Delta[(key[0], c)]))
                        result2 = next(iter(temp.Delta[(key[1], c)]))
                        
                        if (result1, result2) in table:
                            if table[(result1, result2)]:
                                table[key] = True
                                change = True

                        if (result2, result1) in table:
                            if table[(result2, result1)]:
                                table[(result2, result1)]
                                table[key] = True
                                change = True
        partions = []
        for key, value in table.items():
            if not value:
                found = False
                for i in range(len(partions)):
                    if key[0] in partions[i] or key[1] in partions[i]:
                        partions[i].add(key[0])
                        partions[i].add(key[1])
                        found = True
                if not found:
                    partions.append(set([key[0], key[1]]))
        
        newStart = temp.startState
        newFinal = set(temp.FinalStates)
        newDelta = {}
        nonPartionStates = set(temp.States)

        for partion in partions:
            state = next(iter(partion))
            self.partion_add_to_delta(temp, state, newDelta, partions)
            if newStart in partion:
                newStart = state
            if state in newFinal:
                newFinal -= partion
                newFinal.add(state)
            nonPartionStates -= partion

        for state in nonPartionStates:
            self.partion_add_to_delta(temp, state, newDelta, partions)

        result = DFA(newStart, newFinal, newDelta)
        result = result.exclude_unreachable_States_and_rename()
        
        return result
        
    def is_equal(self, L):
        A1 = L.minimize_dfa()
        A2 = self.minimize_dfa()
        if not (A1.Alfabet.issubset(A2.Alfabet) and A2.Alfabet.issubset(A1.Alfabet)):
            return False
        if len(A1.FinalStates) != len(A2.FinalStates):
            return False
        if len(A1.States) != len(A2.States):
            return False

        A2.Alfabet = A1.Alfabet
        A2.exclude_unreachable_States_and_rename()
        for entry in A1.Delta.items():
            key, value = entry
            if key in A2.Delta:
                r2 = next(iter(A2.Delta[key]))
                r1 = next(iter(value))
                if r1 != r2:
                    return False
            else:
                return False

        return True
    
    def complement(self):
        new_final = set(self.States) - self.FinalStates
        return DFA(self.startState, new_final, self.Delta)
    
class NFA(Automata, IRegular):
    def __init__(self, startState, FinalStates, Delta):
        super().__init__(startState, FinalStates, Delta)

    def __str__(self):
        return self.startState + ' '  + str(self.FinalStates) + ' ' + str(self.Delta)
        
    def star(self):
        new_startState = "newStart"
        old_startState = set([self.startState])

        star_Delta = {(new_startState, 'ε'): old_startState}
        for key, value in self.Delta.items():
            star_Delta[key] = value

        new_final = set([new_startState])
        for state in self.FinalStates:
            star_Delta[(state, 'ε')] = new_final

        return NFA(new_startState, new_final, star_Delta)
        
    def concat(self, L):
        A1 = self.exclude_unreachable_States_and_rename('q')
        A2 = L.to_dfa().to_nfa().exclude_unreachable_States_and_rename('p')
        #A2 = L.exclude_unreachable_States_and_rename('p')
        new_startState = "newStart"
        new_delta = A1.Delta

        A1_start = {A1.startState}
        new_delta[(new_startState, 'ε')] = A1_start

        m_state = "Middle"
        middle_state = {m_state}

        for final_state in A1.FinalStates:
            new_delta[(final_state, 'ε')] = middle_state

        A2_start = {A2.startState}
        new_delta[(m_state, 'ε')] = A2_start

        for entry in A2.Delta.items():
            new_delta[entry[0]] = entry[1]

        temp = NFA(new_startState, A2.FinalStates, new_delta).exclude_unreachable_States_and_rename()
        return temp

    def union(self, L):
        A1 = self.exclude_unreachable_States_and_rename('q')
        A2 = L.to_dfa().to_nfa().exclude_unreachable_States_and_rename('p')
        #A2 = L.exclude_unreachable_States_and_rename('p')

        new_startState = "newStart"
        new_delta = A1.Delta
        
        start_union = {A1.startState}
        start_union.add(A2.startState)
        new_delta[(new_startState, 'ε')] = start_union
        
        for entry in A2.Delta.items():
            new_delta[entry[0]] = entry[1]
            
        new_finalStates = set(A1.FinalStates)
        new_finalStates.update(A2.FinalStates)
        
        temp = NFA(new_startState, new_finalStates, new_delta)
        
        return temp.exclude_unreachable_States_and_rename()

    def to_dfa(self):
        newStart = self.one_closure(self.startState)
        uncheckedSets = Queue()
        uncheckedSets.put(newStart)
        count = 0
        newName = dict()
        newName[frozenset(newStart)] = Automata.form_state_name('p', count)
        count += 1
        newFinal = set()
        if newStart.intersection(self.FinalStates):
            newFinal.add(newName[frozenset(newStart)])
        checkedStates = set()
        newDelta = dict()
        nonEpsilon_alfabet = set(self.Alfabet)
        nonEpsilon_alfabet.discard('ε')
        while not uncheckedSets.empty():
            States = uncheckedSets.get()
            checkedStates.add(newName[frozenset(States)])
            for symbol in nonEpsilon_alfabet:
                resultStates = set()
                for state in States:
                    if (state, symbol) in self.Delta:
                        resultStates.update(self.Delta[(state, symbol)])
                resultStates = self.closure(resultStates)
                
                statename = ""
                for key in newName:
                    if key == resultStates:
                        statename = newName[key]
                if len(statename) == 0:
                    newName[frozenset(resultStates)] = Automata.form_state_name('p', count)
                    statename = newName[frozenset(resultStates)]
                    count += 1
                    uncheckedSets.put(resultStates)
                if resultStates.intersection(self.FinalStates):
                    newFinal.add(statename)
                newDelta[(newName[frozenset(States)], symbol)] = {statename}
        df = DFA(newName[frozenset(newStart)], newFinal, newDelta)
        return df
        
    def one_closure(self, state):
        C = set([state])
        uncheckedStates = Queue()
        uncheckedStates.put(state)
        checkedStates = set()
        while not uncheckedStates.empty():
            currentState = uncheckedStates.get()
            checkedStates.add(currentState)
            if (currentState, 'ε') in self.Delta:
                C.update(self.Delta[(currentState, 'ε')])
                for s in self.Delta[(currentState, 'ε')]:
                    if s not in checkedStates:
                        uncheckedStates.put(s)
        return C

    def closure(self, States):
        closure_states = set()
        for state in States:
            closure_states.update(self.one_closure(state))
        return closure_states


    def exclude_unreachable_States_and_rename(self, c='q'):
        result = self.rename_and_exclude_unreachableStates_inner(c)
        nf = NFA(result[0], result[1], result[2])
        return nf
        
    def complement(self):
        return self.to_dfa().complement()
    
    def is_equal(self, L):
        return self.to_dfa().is_equal(L)