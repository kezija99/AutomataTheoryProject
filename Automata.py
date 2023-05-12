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
            
    def RenameAndExcludeUnreachableStatesInner(self, c: str) -> Tuple[str, Set[str], Dict[Tuple[str, str], Set[str]]]:
        Mapping = {}
        stateCount = 0
        Mapping[self.startState] = self.FormStateName(c, stateCount)
        
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
                        if resultState not in Mapping:
                            stateCount += 1
                            Mapping[resultState] = self.FormStateName(c, stateCount)
                            uncheckedStates.put(resultState)
                        renamedResults.add(Mapping[resultState])

                    reducedDelta[(Mapping[state], symbol)] = renamedResults
                    
        renamedFinalStates = set()
        for finalState in self.FinalStates:
            if finalState in Mapping:
                renamedFinalStates.add(Mapping[finalState])
                
        return Mapping[self.startState], renamedFinalStates, reducedDelta
    
    @staticmethod
    def FormStateName(c: str, i: int) -> str:
        return c + str(i)