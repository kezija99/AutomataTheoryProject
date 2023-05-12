from Node import Node
from Automata import Automata
from typing import Set, Dict, Tuple, List
from queue import Queue
from collections import deque

class IRegular:
    
    @staticmethod
    def print_tree(node: Node, level: int = 0) -> None:
        if node is None:
            return
        IRegular.print_tree(node.right, level + 1)
        print(' ' * 4 * level + '->', node.data)
        IRegular.print_tree(node.left, level + 1)
    
    def REtoIR(self, RE: str):
        if not RE:
            raise ValueError("RE string cannot be empty!")
        if ';' in RE or ',' in RE:
            raise ValueError("RE cannot contain the ; or , symbols!")
        tree = Node.parsing_tree(RE)
        IRegular.print_tree(tree)
        return self.construct_nfa(tree).to_dfa()

    def construct_nfa(self, root):
        if not root:
            raise ValueError("Improperly parsed root cannot be None")
        l, r = None, None
        if root.data == "|":
            l = self.construct_nfa(root.left)
            r = self.construct_nfa(root.right)
            return l.Union(r).to_dfa().to_nfa()
        elif root.data == "•":
            l = self.construct_nfa(root.left)
            r = self.construct_nfa(root.right)
            return l.concat(r).to_dfa().to_nfa()
        elif root.data == "*":
            l = self.construct_nfa(root.left)
            return l.star().to_dfa().to_nfa()
        else:
            nf = NFA("q0", self.FinalStates_from_string("q1"), {("q0", root.data): ["q1"]})
            return nf
            
    def FinalStates_from_string(self, FinalStates):
        final = set()
        if len(FinalStates) > 0:
            final.update(FinalStates.split(','))
        return final


class NFA(Automata, IRegular):
    def init(self, startState, FinalStates, Delta):
        super().init(startState, FinalStates, Delta)

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
        #A2 = L.to_dfa().to_nfa().exclude_unreachable_States_and_rename('p')
        A2 = L.exclude_unreachable_States_and_rename('p')
        new_startState = "newStart"
        new_Delta = A1.Delta.copy()

        A1_start = {A1.startState}
        new_Delta[(new_startState, 'ε')] = A1_start

        m_state = "Middle"
        middle_state = {m_state}

        for final_state in A1.FinalStates:
            new_Delta[(final_state, 'ε')] = middle_state

        A2_start = {A2.startState}
        new_Delta[(m_state, 'ε')] = A2_start

        for entry in A2.Delta.items():
            new_Delta[entry[0]] = entry[1]

        temp = NFA(new_startState, A2.FinalStates, new_Delta)
        #print(str(temp))
        return temp.exclude_unreachable_States_and_rename()

    def Union(self, L):
        A1 = self.exclude_unreachable_States_and_rename('q')
        A2 = L.to_dfa().to_nfa().exclude_unreachable_States_and_rename('p')
        
        newStartState = "newStart"
        newDelta = dict(A1.Delta)
        
        StartUnion = {A1.startState}
        StartUnion.add(A2.startState)
        newDelta[(newStartState, 'ε')] = StartUnion
        
        for entry in A2.Delta.items():
            newDelta[entry[0]] = entry[1]
            
        newFinalStates = set(A1.FinalStates)
        newFinalStates |= A2.FinalStates
        
        temp = NFA(newStartState, newFinalStates, newDelta)
        
        return temp.exclude_unreachable_States_and_rename()

    def to_dfa(self):
        newStart = self.OneClosure(self.startState)
        uncheckedSets = list()
        uncheckedSets.append(newStart)
        count = 0
        newName = dict()
        newName[frozenset(newStart)] = Automata.FormStateName('p', count)
        count += 1
        newFinal = set()
        if newStart.intersection(self.FinalStates):
            newFinal.add(newName[frozenset(newStart)])
        checkedStates = set()
        newDelta = dict()
        nonEpsilonAlfabet = set(self.Alfabet)
        nonEpsilonAlfabet.discard('ε')
        while uncheckedSets:
            States = uncheckedSets.pop(0)
            checkedStates.add(newName[frozenset(States)])
            for symbol in nonEpsilonAlfabet:
                resultStates = set()
                for state in States:
                    if (state, symbol) in self.Delta:
                        resultStates.update(self.Delta[(state, symbol)])
                resultStates = self.Closure(resultStates)
                statename = ""
                for key in newName:
                    if key == resultStates:
                        statename = newName[key]
                if not statename:
                    newName[frozenset(resultStates)] = Automata.FormStateName('p', count)
                    statename = newName[frozenset(resultStates)]
                    count += 1
                    uncheckedSets.append(resultStates)
                if resultStates.intersection(self.FinalStates):
                    newFinal.add(statename)
                newDelta[(newName[frozenset(States)], symbol)] = {statename}
        df = DFA(newName[frozenset(newStart)], newFinal, newDelta)
        return df
        
    def OneClosure(self, state):
        C = {state}
        uncheckedStates = deque(C)
        checkedStates = set()
        while len(uncheckedStates) > 0:
            currentState = uncheckedStates.popleft()
            checkedStates.add(currentState)
            if (currentState, 'ε') in self.Delta:
                C.update(self.Delta[(currentState, 'ε')])
                for s in self.Delta[(currentState, 'ε')]:
                    if s not in checkedStates:
                        uncheckedStates.append(s)
        return C

    def Closure(self, States):
        ClosureStates = set()
        for state in States:
            ClosureStates.update(self.OneClosure(state))
        return ClosureStates


    def exclude_unreachable_States_and_rename(self, c='q'):
        result = self.RenameAndExcludeUnreachableStatesInner(c)
        nf = NFA(result[0], result[1], result[2])
        return nf
        
class DFA(Automata, IRegular):
    def init(self, startState, FinalStates, Delta):
        super().init(startState, FinalStates, Delta)
    
    def __str__(self):
        return self.startState + ' '  + str(self.FinalStates) + ' ' + str(self.Delta)
        
    def to_nfa(self):
        return NFA(self.startState, self.FinalStates, self.Delta)
        
    def accepts(self, word):
        current_state = self.startState
        for symbol in word:
            if symbol in self.Alfabet:
                current_state = next(iter(self.Delta[(current_state, symbol)]), None)
                if current_state is None:
                    return False
            else:
                return False
        return current_state in self.FinalStates
        
    def combine(self, A, filter_func):
        if not (self.Alfabet < A.Alfabet and A.Alfabet < self.Alfabet):
            raise Exception("For operations on regular languages the Alfabet has to be the same!")

        A1 = self
        A2 = A

        uncheckedStatePairs = deque()
        uncheckedStatePairs.append((A1.startState, A2.startState))

        newName = {}
        checkedSatePairs = set()

        combinedDelta = {}
        combinedFinal = set()

        count = 0
        newName[(A1.startState, A2.startState)] = Automata.FormStateName('q', count)
        if filter_func(A1.FinalStates, A2.FinalStates, (A1.startState, A2.startState)):
            combinedFinal.add(newName[(A1.startState, A2.startState)])

        while uncheckedStatePairs:
            statePair = uncheckedStatePairs.popleft()
            checkedSatePairs.add(statePair)
            for symbol in self.Alfabet:
                resultPair = (A1.Delta[(statePair[0], symbol)].pop(), A2.Delta[(statePair[1], symbol)].pop())
                A1.Delta[(statePair[0], symbol)].add(resultPair[0])
                A2.Delta[(statePair[1], symbol)].add(resultPair[1])
                if resultPair not in checkedSatePairs:
                    uncheckedStatePairs.append(resultPair)
                if resultPair not in newName:
                    count += 1
                    newName[resultPair] = Automata.FormStateName('q', count)
                    if filter_func(A1.FinalStates, A2.FinalStates, resultPair):
                        combinedFinal.add(newName[resultPair])
                combinedDelta[(newName[statePair], symbol)] = {newName[resultPair]}

        return DFA(newName[(A1.startState, A2.startState)], combinedFinal, combinedDelta)
    
    def exclude_unreachable_States_and_rename(self, c='q'):
        result = self.RenameAndExcludeUnreachableStatesInner(c)
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
                        if (key[0], c) not in temp.Delta or not temp.Delta[(key[0], c)]:
                            continue
                        result1 = temp.Delta[(key[0], c)].pop()
                        if (key[1], c) not in temp.Delta or not temp.Delta[(key[1], c)]:
                            continue
                        result2 = temp.Delta[(key[1], c)].pop()

                        if (result1, result2) in table:
                            if table[(result1, result2)]:
                                table[key] = True
                                change = True

                        if (result2, result1) in table:
                            if table[(result2, result1)]:
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
        
