from typing import Set, Dict, Tuple
from queue import Queue

class Automata:
    def __init__(self, startState: str, FinalStates: Set[str], Delta: Dict[Tuple[str, str], Set[str]]):
        self.States = set()
        self.Alfabet = set()
        self.FinalStates = set(FinalStates)
        self.startState = startState
        self.Delta = Delta
        self.ConstructInferedSets()
        self.StateConsistency()
        
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
    
    def ConstructInferedSets(self):
        if len(self.startState) > 0:
            self.States.add(self.startState)
        for (state, symbol), targetStates in self.Delta.items():
            self.Alfabet.add(symbol)
            self.States.add(state)
            self.States.update(targetStates)

    def StateConsistency(self):
        if not self.FinalStates.issubset(self.States):
            raise Exception("The set of FinalStates has to be a sub set of all states!")
        if self.startState not in self.States:
            raise Exception("Start state has to be a member of states!")
            
    def rename_and_exclude_unreachableStates_inner(self, c: str) -> Tuple[str, Set[str], Dict[Tuple[str, str], Set[str]]]:
        mapping = {}
        stateCount = 0
        mapping[self.startState] = self.form_state_name(c, stateCount)
        stateCount += 1

        reducedDelta = {}
        uncheckedStates = Queue()
        uncheckedStates.put(self.startState)
        
        while not uncheckedStates.empty():
            state = uncheckedStates.get()
            for symbol in self.Alfabet:
                if (state, symbol) in self.Delta:
                    results = self.Delta[(state, symbol)]
                    renamedResults = set()
                    for resultState in results:
                        if resultState not in mapping:
                            mapping[resultState] = self.form_state_name(c, stateCount)
                            stateCount += 1
                            uncheckedStates.put(resultState)
                        renamedResults.add(mapping[resultState])

                    reducedDelta[(mapping[state], symbol)] = renamedResults
                    
        renamed_finalStates = set()
        for finalState in self.FinalStates:
            if finalState in mapping:
                renamed_finalStates.add(mapping[finalState])
                
        return mapping[self.startState], renamed_finalStates, reducedDelta
    
    @staticmethod
    def form_state_name(c: str, i: int) -> str:
        return c + str(i)