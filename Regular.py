from IRegular import DFA

class Regular:

    def create_table(self, dfa: DFA):

        table = {
            state1: {state2: '' for state2 in sorted(list(dfa.states))}
            for state1 in sorted(list(dfa.states))
        }

        for transitions, next_state in dfa.delta.items():
            state, character = transitions
            if table[state][list(next_state)[0]] == '':
                table[state][list(next_state)[0]] = character
            else:
                table[state][list(next_state)[0]] += '|' + character
        return table

    def find_pre_suc(self, state, table, dfa: DFA):
        preds = []
        succs = []
        curr_dict_for_from = {st: {to: v for to, v in val.items(
        ) if to == state} for st, val in table.items()}

        for pred in dfa.states:
            if pred not in curr_dict_for_from.keys() or pred == state:
                continue
            if curr_dict_for_from[pred][state] != '':
                preds.append(pred)

        for succ in dfa.states:
            if succ not in table[state].keys() or state == succ:
                continue
            if table[state][succ] != '':
                succs.append(succ)
        return preds, succs

    def state_loop(self, state, table):
        if table[state][state] == '':
            return False
        else:
            return True

    def modify_initial_state(self, dfa: DFA):
        flag = False
        initial_state = dfa.start_state
        for transition, state in dfa.delta.items():
            if initial_state in state:
                flag = True
                break
        if flag:
            dfa.states.add('qi')
            dfa.delta[('qi', 'ε')] = {dfa.start_state}
            dfa.start_state = 'qi'
        return dfa

    def modify_final_states(self, dfa: DFA):
        flag = False
        if len(dfa.final_states) > 1:
            flag = True
        
        final_state = list(dfa.final_states)[0]
        tmp = dfa.delta.keys()
        for s in tmp:
            if final_state in s:
                flag = True

        if flag:
            dfa.states.add('qf')
            for final_state in dfa.final_states:
                dfa.delta[(final_state, 'ε')] = {'qf'}
            dfa.final_states = 'qf'
        else:
            dfa.final_states = list(dfa.final_states)[0]
        return dfa

    def dfa_to_regex(self, dfa: DFA):

        dfa = self.modify_initial_state(dfa)
        dfa = self.modify_final_states(dfa)

        state_initial = dfa.start_state
        state_final = dfa.final_states

        table = self.create_table(dfa)

        for state in sorted(list(dfa.states)):
            if state == state_initial or state == state_final:
                continue

            preds, succs = self.find_pre_suc(
                state, table, dfa)

            for pred in preds:
                if pred in table.keys():
                    for succ in succs:
                        if succ in table[pred].keys():

                            pre_suc_input_exp = ''
                            self_loop_input_exp = ''
                            from_pre_input_exp = ''
                            to_suc_input_exp = ''

                            if table[pred][succ] != '':
                                pre_suc_input_exp = '(' + table[pred][succ] + ')'

                            if self.state_loop(state, table):
                                self_loop_input_exp = '(' + table[state][state] + ')' + '*'

                            if table[pred][state] != '':
                                from_pre_input_exp = '(' + table[pred][state] + ')'

                            if table[state][succ] != '':
                                to_suc_input_exp = '(' + table[state][succ] + ')'

                            new_pre_suc_input_exp = from_pre_input_exp + self_loop_input_exp + to_suc_input_exp

                            if pre_suc_input_exp != '':
                                new_pre_suc_input_exp += ('|' + pre_suc_input_exp)

                            table[pred][succ] = new_pre_suc_input_exp

            table = {st: {to: v for to, v in inp.items() if to != state}
                         for st, inp in table.items() if st != state}
        return table[state_initial][state_final]