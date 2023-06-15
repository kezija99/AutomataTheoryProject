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
    def re_to_ir(re: str):
        if not re:
            raise ValueError("re string cannot be empty!")
        if ';' in re or ',' in re:
            raise ValueError("re cannot contain the ; or , symbols!")
        tree = Node.parsing_tree(re)
        #IRegular.print_tree(tree)
        return IRegular.construct_nfa(tree)

    @staticmethod
    def construct_nfa(root):
        if not root:
            raise ValueError("Improperly parsed, root cannot be None")
        l, r = None, None
        if root.data == "|":
            l = IRegular.construct_nfa(root.left)
            r = IRegular.construct_nfa(root.right)
            return l.union(r).to_dfa().to_nfa()
        elif root.data == "•":
            l = IRegular.construct_nfa(root.left)
            r = IRegular.construct_nfa(root.right)
            return l.concat(r).to_dfa().to_nfa()
        elif root.data == "*":
            l = IRegular.construct_nfa(root.left)
            return l.star().to_dfa().to_nfa()
        else:
            nf = NFA("q0", {"q1"}, {("q0", root.data): ["q1"]})
            return nf
        
class DFA(Automata):
    def __init__(self, start_state, final_states, delta):
        super().__init__(start_state, final_states, delta)
    
    def __str__(self):
        return self.start_state + ' '  + str(self.final_states) + ' ' + str(self.delta)
        
    def to_nfa(self):
        return NFA(self.start_state, self.final_states, self.delta)
        
    def exclude_unreachable_states_and_rename(self, c='q'):
        result = self.rename_and_exclude_unreachable_states_inner(c)
        df = DFA(result[0], result[1], result[2])
        return df

    def partition_add_to_delta(self, temp, state, new_delta, partitions):
        for c in temp.alfabet:
            if temp.delta[(state, c)]:
                result = temp.delta[(state, c)].pop()
                for p in partitions:
                    if result in p:
                        result = next(iter(p))
                new_delta[(state, c)] = set([result])
            
    def minimize_dfa(self):
        temp = self.exclude_unreachable_states_and_rename()
        non_final = set(temp.states) - set(temp.final_states)
       
        all_states = list(temp.states)
        table = {}
        for i in range(len(all_states)):
            for j in range(i+1, len(all_states)):
                if ((all_states[i] in temp.final_states and all_states[j] in non_final) or
                    (all_states[j] in temp.final_states and all_states[i] in non_final)):
                    table[(all_states[i], all_states[j])] = True
                else:
                    table[(all_states[i], all_states[j])] = False
        
        change = True
        while change:
            change = False
            for key, value in table.items():
                if not value:
                    for c in temp.alfabet:
                        result1 = next(iter(temp.delta[(key[0], c)]))
                        result2 = next(iter(temp.delta[(key[1], c)]))
                        
                        if (result1, result2) in table:
                            if table[(result1, result2)]:
                                table[key] = True
                                change = True

                        if (result2, result1) in table:
                            if table[(result2, result1)]:
                                table[(result2, result1)]
                                table[key] = True
                                change = True
        partitions = []
        for key, value in table.items():
            if not value:
                found = False
                for i in range(len(partitions)):
                    if key[0] in partitions[i] or key[1] in partitions[i]:
                        partitions[i].add(key[0])
                        partitions[i].add(key[1])
                        found = True
                if not found:
                    partitions.append(set([key[0], key[1]]))
        
        new_start = temp.start_state
        new_final = set(temp.final_states)
        new_delta = {}
        non_partion_states = set(temp.states)

        for partion in partitions:
            state = next(iter(partion))
            self.partition_add_to_delta(temp, state, new_delta, partitions)
            if new_start in partion:
                new_start = state
            if state in new_final:
                new_final -= partion
                new_final.add(state)
            non_partion_states -= partion

        for state in non_partion_states:
            self.partition_add_to_delta(temp, state, new_delta, partitions)

        return DFA(new_start, new_final, new_delta).exclude_unreachable_states_and_rename()
    
    def is_equal(self, l):
        a1 = l.minimize_dfa()
        a2 = self.minimize_dfa()
        if not (a1.alfabet.issubset(a2.alfabet) and a2.alfabet.issubset(a1.alfabet)):
            return False
        if len(a1.final_states) != len(a2.final_states):
            return False
        if len(a1.states) != len(a2.states):
            return False

        a2.alfabet = a1.alfabet
        a2.exclude_unreachable_states_and_rename()
        
        for key, value in a1.delta.items():
            if key in a2.delta:
                r2 = a2.delta[key]
                r1 = value
                if r1 != r2:
                    return False
            else:
                return False

        return True
    
    def complement(self):
        new_final = set(self.states) - self.final_states
        return DFA(self.start_state, new_final, self.delta)
    

class NFA(Automata):
    def __init__(self, start_state, final_states, delta):
        super().__init__(start_state, final_states, delta)

    def __str__(self):
        return self.start_state + ' '  + str(self.final_states) + ' ' + str(self.delta)
        
    def star(self):
        new_start_state = "new_start"
        old_start_state = set([self.start_state])

        star_delta = {(new_start_state, 'ε'): old_start_state}
        for key, value in self.delta.items():
            star_delta[key] = value

        new_final = set([new_start_state])
        for state in self.final_states:
            star_delta[(state, 'ε')] = new_final

        return NFA(new_start_state, new_final, star_delta)
        
    def concat(self, l):
        a1 = self.exclude_unreachable_states_and_rename('q')
        a2 = l.to_dfa().to_nfa().exclude_unreachable_states_and_rename('p')
        new_start_state = "new_start"
        new_delta = a1.delta

        a1_start = {a1.start_state}
        new_delta[(new_start_state, 'ε')] = a1_start

        m_state = "Middle"
        middle_state = {m_state}

        for final_state in a1.final_states:
            new_delta[(final_state, 'ε')] = middle_state

        a2_start = {a2.start_state}
        new_delta[(m_state, 'ε')] = a2_start

        for entry in a2.delta.items():
            new_delta[entry[0]] = entry[1]

        return NFA(new_start_state, a2.final_states, new_delta).exclude_unreachable_states_and_rename()

    def union(self, l):
        a1 = self.exclude_unreachable_states_and_rename('q')
        a2 = l.to_dfa().to_nfa().exclude_unreachable_states_and_rename('p')

        new_start_state = "new_start"
        new_delta = a1.delta
        
        start_union = {a1.start_state}
        start_union.add(a2.start_state)
        new_delta[(new_start_state, 'ε')] = start_union
        
        for entry in a2.delta.items():
            new_delta[entry[0]] = entry[1]
            
        new_final_states = set(a1.final_states)
        new_final_states.update(a2.final_states)
        
        return NFA(new_start_state, new_final_states, new_delta).exclude_unreachable_states_and_rename()

    def to_dfa(self):
        new_start = self.one_closure(self.start_state)
        unchecked_sets = Queue()
        unchecked_sets.put(new_start)
        count = 0
        new_name = dict()
        new_name[frozenset(new_start)] = Automata.form_state_name('p', count)
        count += 1
        new_final = set()
        if new_start.intersection(self.final_states):
            new_final.add(new_name[frozenset(new_start)])
        checked_states = set()
        new_delta = dict()
        non_epsilon_alfabet = set(self.alfabet)
        non_epsilon_alfabet.discard('ε')
        while not unchecked_sets.empty():
            states = unchecked_sets.get()
            checked_states.add(new_name[frozenset(states)])
            for symbol in non_epsilon_alfabet:
                result_states = set()
                for state in states:
                    if (state, symbol) in self.delta:
                        result_states.update(self.delta[(state, symbol)])
                result_states = self.closure(result_states)
                
                state_name = ""
                for key in new_name:
                    if key == result_states:
                        state_name = new_name[key]
                if len(state_name) == 0:
                    new_name[frozenset(result_states)] = Automata.form_state_name('p', count)
                    state_name = new_name[frozenset(result_states)]
                    count += 1
                    unchecked_sets.put(result_states)
                if result_states.intersection(self.final_states):
                    new_final.add(state_name)
                new_delta[(new_name[frozenset(states)], symbol)] = {state_name}
        return DFA(new_name[frozenset(new_start)], new_final, new_delta)
        
    def one_closure(self, state):
        c = set([state])
        unchecked_states = Queue()
        unchecked_states.put(state)
        checked_states = set()
        while not unchecked_states.empty():
            current_state = unchecked_states.get()
            checked_states.add(current_state)
            if (current_state, 'ε') in self.delta:
                c.update(self.delta[(current_state, 'ε')])
                for s in self.delta[(current_state, 'ε')]:
                    if s not in checked_states:
                        unchecked_states.put(s)
        return c

    def closure(self, states):
        closure_states = set()
        for state in states:
            closure_states.update(self.one_closure(state))
        return closure_states


    def exclude_unreachable_states_and_rename(self, c='q'):
        result = self.rename_and_exclude_unreachable_states_inner(c)
        nf = NFA(result[0], result[1], result[2])
        return nf
        
    def complement(self):
        return self.to_dfa().complement()
    
    def is_equal(self, l):
        return self.to_dfa().is_equal(l)