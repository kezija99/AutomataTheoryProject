from IRegular import NFA, DFA

class FAHelper:

    def get_input_symbol(self, automata: DFA):

        hop_table = {
            state1: {state2: '' for state2 in sorted(list(automata.States))}
            for state1 in sorted(list(automata.States))
        }

        for transitions, next_state in automata.Delta.items():
            state, character = transitions
            if hop_table[state][list(next_state)[0]] == '':
                hop_table[state][list(next_state)[0]] = character
            else:
                hop_table[state][list(next_state)[0]] += '|' + character
        return hop_table

    def get_predecessors_successors(self, state, hop_table, automata: DFA):
        predecessors = []
        successors = []
        curr_dict_for_from = {st: {to: v for to, v in val.items(
        ) if to == state} for st, val in hop_table.items()}

        for predecessor in automata.States:
            if predecessor not in curr_dict_for_from.keys() or predecessor == state:
                continue
            if curr_dict_for_from[predecessor][state] != '':
                predecessors.append(predecessor)

        for successor in automata.States:
            if successor not in hop_table[state].keys() or state == successor:
                continue
            if hop_table[state][successor] != '':
                successors.append(successor)
        return predecessors, successors

    def check_state_loop(self, state, automata: DFA):
        next_states = set()
        for transition in automata.Delta.values():
            if state in transition:
                next_states.update(transition)
        if state in next_states:
            return True
        return False


    def start_has_incoming(self, automata: DFA):
        check = False
        initial_state = automata.startState
        for transition, state in automata.Delta.items():
            if initial_state in state:
                check = True
                break
        return check

    def end_has_outgoing(self, automata: DFA):
        # if there is multiple final states return true
        if len(automata.FinalStates) > 1:
            return True
        # else find that one final state
        final_state = list(automata.FinalStates)[0]
        # check that there is some state that final has transition to
        tmp = automata.Delta.values()
        for s in tmp:
            if final_state in s:
                return True
        return False

    def handle_start_incoming(self, automata: DFA):
        if self.start_has_incoming(automata):
            automata.States.add('qi')
            automata.Delta[('qi', '$')] = {automata.startState}
            automata.startState = 'qi'
        return automata

    def handle_end_outgoing(self, automata: DFA):
        if self.end_has_outgoing(automata):
            automata.States.add('qf')
            for final_state in automata.FinalStates:
                automata.Delta[(final_state, '$')] = {'qf'}
            automata.FinalStates = 'qf'
        else:
            automata.FinalStates = list(automata.FinalStates)[0]
        return automata

    def dfa_to_regex(self, hop_table, state_initial, state_final, automata: DFA):
        for state in sorted(list(automata.States)):
            if state == state_initial or state == state_final:
                continue

            predecessors, successors = self.get_predecessors_successors(
                state, hop_table, automata)

            for predecessor in predecessors:
                if predecessor in hop_table.keys():
                    for successor in successors:
                        if successor in hop_table[predecessor].keys():

                            pre_suc_input_exp = ''
                            self_loop_input_exp = ''
                            from_pre_input_exp = ''
                            to_suc_input_exp = ''

                            if hop_table[predecessor][successor] != '':
                                pre_suc_input_exp = '(' + \
                                    hop_table[predecessor][successor] + ')'

                            if self.check_state_loop(state, automata):
                                self_loop_input_exp = '(' + \
                                    hop_table[state][state] + ')' + '*'

                            if hop_table[predecessor][state] != '':
                                from_pre_input_exp = '(' + \
                                    hop_table[predecessor][state] + ')'

                            if hop_table[state][successor] != '':
                                to_suc_input_exp = '(' + \
                                    hop_table[state][successor] + ')'

                            new_pre_suc_input_exp = from_pre_input_exp + \
                                self_loop_input_exp + to_suc_input_exp

                            if pre_suc_input_exp != '':
                                new_pre_suc_input_exp += ('|' +
                                                          pre_suc_input_exp)

                            hop_table[predecessor][successor] = new_pre_suc_input_exp

            hop_table = {st: {to: v for to, v in inp.items() if to != state}
                         for st, inp in hop_table.items() if st != state}
        return hop_table[state_initial][state_final]
