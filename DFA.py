from Automata import Automata
from iRegular import IRegular

class DFA(Automata, IRegular):
    def __init__(self, startState: str, FinalStates: Set[str], Delta: Dict[Tuple[str, str], Set[str]]):
        super().init(startState, FinalStates, Delta)
    
    def toNFA(self):
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