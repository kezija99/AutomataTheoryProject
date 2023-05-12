from Automata import Automata
from iRegular import IRegular

class NFA(Automata, IRegular):
    def __init__(self, startState: str, FinalStates: Set[str], Delta: Dict[Tuple[str, str], Set[str]]):
        super().init(startState, FinalStates, Delta)

    def star(self):
        new_start_state = "newStart"
        old_start_state = set([self.start_state])

        star_delta = {(new_start_state, 'ε'): old_start_state}
        for key, value in self.Delta.items():
            star_delta[key] = value

        new_final = set([new_start_state])
        for state in self.final_states:
            star_delta[(state, 'ε')] = new_final

        return NFA(new_start_state, new_final, star_delta)
        
    def concat(self, L):
        A1 = self.exclude_unreachable_states_and_rename('q')
        A2 = L.to_dfa().to_nfa().exclude_unreachable_states_and_rename('p')

        new_start_state = "newStart"
        new_delta = A1.Delta.copy()

        A1_start = Automata.one_member_set(A1.start_state)
        new_delta[(new_start_state, 'ε')] = A1_start

        m_state = "Middle"
        middle_state = Automata.one_member_set(m_state)

        for final_state in A1.final_states:
            new_delta[(final_state, 'ε')] = middle_state

        A2_start = Automata.one_member_set(A2.start_state)
        new_delta[(m_state, 'ε')] = A2_start

        for entry in A2.Delta.items():
            new_delta[entry[0]] = entry[1]

        temp = NFA(new_start_state, A2.final_states, new_delta)
        return temp.exclude_unreachable_states_and_rename()

    def Union(self, L):
        A1 = self.exclude_unreachable_states_and_rename('q')
        A2 = L.toDFA().toNFA().exclude_unreachable_states_and_rename('p')
        
        newStartState = "newStart"
        newDelta = dict(A1.Delta)
        
        StartUnion = Automata.OneMemberSet(A1.startState)
        StartUnion.add(A2.startState)
        newDelta[(newStartState, 'ε')] = StartUnion
        
        for entry in A2.Delta.items():
            newDelta[entry[0]] = entry[1]
            
        newFinalStates = set(A1.FinalStates)
        newFinalStates |= A2.FinalStates
        
        temp = NFA(newStartState, newFinalStates, newDelta)
        
        return temp.exclude_unreachable_states_and_rename()

    def toDFA(self):
        newStart = self.Closure(self.startState)

        uncheckedSets = deque([newStart])
        count = 0
        newName = {newStart: Automata.FormStateName('p', count)}
        count += 1

        newFinal = set()
        if any(state in self.FinalStates for state in newStart):
            newFinal.add(newName[newStart])

        checkedStates = set()
        newDelta = {}

        nonEpsilonAlphabet = set(self.Alphabet)
        nonEpsilonAlphabet.discard('ε')
        while uncheckedSets:
            states = uncheckedSets.popleft()
            checkedStates.add(newName[states])
            for symbol in nonEpsilonAlphabet:
                resultStates = set()
                for state in states:
                    if (state, symbol) in self.Delta:
                        resultStates |= self.Delta[(state, symbol)]
                resultStates = self.Closure(resultStates)
                statename = next((name for name, s in newName.items() if s == resultStates), None)
                if statename is None:
                    newName[resultStates] = Automata.FormStateName('p', count)
                    count += 1
                    uncheckedSets.append(resultStates)
                    statename = newName[resultStates]
                if any(state in self.FinalStates for state in resultStates):
                    newFinal.add(statename)
                newDelta[(newName[states], symbol)] = {statename}

        return DFA(newName[newStart], newFinal, newDelta)

    def closure(self, states: Set[str]) -> Set[str]:
        closure_states = set(states)
        unchecked_states = list(states)

        while unchecked_states:
            state = unchecked_states.pop()
            if (state, 'ε') in self.Delta:
                new_states = self.Delta[(state, 'ε')] - closure_states
                closure_states.update(new_states)
                unchecked_states.extend(new_states)

        return closure_states

    def exclude_unreachable_states_and_rename(self, c='q'):
        result = self.RenameAndExcludeUnreachableStatesInner(c)
        return NFA(result[0], result[1], result[2])
