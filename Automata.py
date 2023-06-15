from typing import Set, Dict, Tuple
from queue import Queue

class Automata:
    def __init__(self, start_state: str, final_states: Set[str], delta: Dict[Tuple[str, str], Set[str]]):
        self.states = set()
        self.alfabet = set()
        self.final_states = set(final_states)
        self.start_state = start_state
        self.delta = delta
        self.construct_infered_sets()
        self.state_consistency()
        
    def accepts(self, word):
        current_state = self.start_state
        for symbol in word:
            if symbol in self.alfabet:
                current_state = next(iter(self.delta[(current_state, symbol)]), None)
                if current_state is None:
                    return False
            else:
                return False
        return current_state in self.final_states
    
    def construct_infered_sets(self):
        if len(self.start_state) > 0:
            self.states.add(self.start_state)
        for (state, symbol), target_states in self.delta.items():
            self.alfabet.add(symbol)
            self.states.add(state)
            self.states.update(target_states)

    def state_consistency(self):
        if not self.final_states.issubset(self.states):
            raise Exception("The set of final_states has to be a sub set of all states!")
        if self.start_state not in self.states:
            raise Exception("Start state has to be a member of states!")
            
    def rename_and_exclude_unreachable_states_inner(self, c: str) -> Tuple[str, Set[str], Dict[Tuple[str, str], Set[str]]]:
        mapping = {}
        state_count = 0
        mapping[self.start_state] = self.form_state_name(c, state_count)
        state_count += 1

        reduced_delta = {}
        unchecked_states = Queue()
        unchecked_states.put(self.start_state)
        
        while not unchecked_states.empty():
            state = unchecked_states.get()
            for symbol in self.alfabet:
                if (state, symbol) in self.delta:
                    results = self.delta[(state, symbol)]
                    renamed_results = set()
                    for result_state in results:
                        if result_state not in mapping:
                            mapping[result_state] = self.form_state_name(c, state_count)
                            state_count += 1
                            unchecked_states.put(result_state)
                        renamed_results.add(mapping[result_state])

                    reduced_delta[(mapping[state], symbol)] = renamed_results
                    
        renamed_final_states = set()
        for final_state in self.final_states:
            if final_state in mapping:
                renamed_final_states.add(mapping[final_state])
                
        return mapping[self.start_state], renamed_final_states, reduced_delta
    
    @staticmethod
    def form_state_name(c: str, i: int) -> str:
        return c + str(i)