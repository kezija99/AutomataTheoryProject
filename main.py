from IRegular import IRegular, NFA, DFA
from FAHelper import FAHelper

tmp = IRegular()
helper = FAHelper()
a_nfa = DFA('q0', {'q1'}, {('q0', 'a'): {'q1'}, ('q1', 'a'): {'q2'}, ('q2', 'a'): {'q2'}})
min_a_dfa = a_nfa.minimize_dfa()
print('AAAAAAAAAAAAAAAAAA' + str(min_a_dfa))
print(min_a_dfa.accepts(''))
min_a_dfa = helper.handle_start_incoming(min_a_dfa)
min_a_dfa = helper.handle_end_outgoing(min_a_dfa)
hop_table = helper.get_input_symbol(min_a_dfa)
regex = helper.dfa_to_regex(
    hop_table, min_a_dfa.startState, min_a_dfa.FinalStates, min_a_dfa)
print(regex)
regex = regex.replace('()', '')
regex = regex.replace('($)', '')
print(regex)
print('AAAAAAAAAAAAAAAAAA')
expresion = tmp.REtoIR('(aa|bb)|(a|b|c)*cd|a(bcd)*')
dfa = expresion.to_dfa().minimize_dfa()
#print(str(dfa))
dfa = helper.handle_start_incoming(dfa)
dfa = helper.handle_end_outgoing(dfa)
hop_table = helper.get_input_symbol(dfa)
regex = helper.dfa_to_regex(
    hop_table, dfa.startState, dfa.FinalStates, dfa)

regex = regex.replace('()*', '')
regex = regex.replace('($)', '')
print(regex)
expresion = tmp.REtoIR(regex)
dfa = expresion.to_dfa().minimize_dfa()
print('' + str(dfa.accepts('abcdbcdbcdbcdbcdbcdbc')))
print('' + str(dfa.accepts('aaaaaaabccccd')))
dfa = helper.handle_start_incoming(dfa)
dfa = helper.handle_end_outgoing(dfa)
hop_table = helper.get_input_symbol(dfa)
regex = helper.dfa_to_regex(
    hop_table, dfa.startState, dfa.FinalStates, dfa)

regex = regex.replace('()*', '')
regex = regex.replace('($)', '')

expresion = tmp.REtoIR(regex)
dfa = expresion.to_dfa().minimize_dfa()
print(str(dfa))
print('' + str(dfa.accepts('cd')))
print('' + str(dfa.accepts('ab')))
print("============================================")

dfa = DFA('q0', {'q7', 'q5', 'q10', 'q2'}, {('q0', 'd'): {'q1'}, ('q0', 'a'): {'q2'}, ('q0', 'c'): {'q3'}, ('q0', 'b'): {'q4'}, ('q1', 'd'): {'q1'}, ('q1', 'a'): {'q1'}, ('q1', 'c'): {'q1'}, ('q1', 'b'): {'q1'}, ('q2', 'd'): {'q1'}, ('q2', 'a'): {'q5'}, ('q2', 'c'): {'q3'}, ('q2', 'b'): {'q6'}, ('q3', 'd'): {'q7'}, ('q3', 'a'): {'q8'}, ('q3', 'c'): {'q3'}, ('q3', 'b'): {'q8'}, ('q4', 'd'): {'q1'}, ('q4', 'a'): {'q8'}, ('q4', 'c'): {'q3'}, ('q4', 'b'): {'q5'}, ('q5', 'd'): {'q1'}, ('q5', 'a'): {'q8'}, ('q5', 'c'): {'q3'}, ('q5', 'b'): {'q8'}, ('q6', 'd'): {'q1'}, ('q6', 'a'): {'q8'}, ('q6', 'c'): {'q9'}, ('q6', 'b'): {'q8'}, ('q7', 'd'): {'q1'}, ('q7', 'a'): {'q1'}, ('q7', 'c'): {'q1'}, ('q7', 'b'): {'q1'}, ('q8', 'd'): {'q1'}, ('q8', 'a'): {'q8'}, 
('q8', 'c'): {'q3'}, ('q8', 'b'): {'q8'}, ('q9', 'd'): {'q10'}, ('q9', 'a'): {'q8'}, ('q9', 'c'): {'q3'}, ('q9', 'b'): {'q8'}, ('q10', 'd'): {'q1'}, ('q10', 'a'): {'q1'}, ('q10', 'c'): {'q1'}, ('q10', 'b'): {'q11'}, ('q11', 'd'): {'q1'}, ('q11', 'a'): {'q1'}, ('q11', 'c'): {'q12'}, ('q11', 'b'): {'q1'}, ('q12', 'd'): {'q10'}, ('q12', 'a'): {'q1'}, ('q12', 'c'): {'q1'}, 
('q12', 'b'): {'q1'}})
dfa2 = DFA('q0', {'q7', 'q5', 'q10', 'q2'}, {('q0', 'd'): {'q1'}, ('q0', 'a'): {'q2'}, ('q0', 'c'): {'q3'}, ('q0', 'b'): {'q4'}, ('q1', 'd'): {'q1'}, ('q1', 'a'): {'q1'}, ('q1', 'c'): {'q1'}, ('q1', 'b'): {'q1'}, ('q2', 'd'): {'q1'}, ('q2', 'a'): {'q5'}, ('q2', 'c'): {'q3'}, ('q2', 'b'): {'q6'}, ('q3', 'd'): {'q7'}, ('q3', 'a'): {'q8'}, ('q3', 'c'): {'q3'}, ('q3', 'b'): {'q8'}, ('q4', 'd'): {'q1'}, ('q4', 'a'): {'q8'}, ('q4', 'c'): {'q3'}, ('q4', 'b'): {'q5'}, ('q5', 'd'): {'q1'}, ('q5', 'a'): {'q8'}, ('q5', 'c'): {'q3'}, ('q5', 'b'): {'q8'}, ('q6', 'd'): {'q1'}, ('q6', 'a'): {'q8'}, ('q6', 'c'): {'q9'}, ('q6', 'b'): {'q8'}, ('q7', 'd'): {'q1'}, ('q7', 'a'): {'q1'}, ('q7', 'c'): {'q1'}, ('q7', 'b'): {'q1'}, ('q8', 'd'): {'q1'}, ('q8', 'a'): {'q8'}, 
('q8', 'c'): {'q3'}, ('q8', 'b'): {'q8'}, ('q9', 'd'): {'q10'}, ('q9', 'a'): {'q8'}, ('q9', 'c'): {'q3'}, ('q9', 'b'): {'q8'}, ('q10', 'd'): {'q1'}, ('q10', 'a'): {'q1'}, ('q10', 'c'): {'q1'}, ('q10', 'b'): {'q11'}, ('q11', 'd'): {'q1'}, ('q11', 'a'): {'q1'}, ('q11', 'c'): {'q12'}, ('q11', 'b'): {'q1'}, ('q12', 'd'): {'q10'}, ('q12', 'a'): {'q1'}, ('q12', 'c'): {'q1'}, 
('q12', 'b'): {'q1'}})

print('OVAJ GLEDAAAAJ' + str(dfa.accepts('ab')))

dfa2 = helper.handle_start_incoming(dfa2)
dfa2 = helper.handle_end_outgoing(dfa2)
hop_table = helper.get_input_symbol(dfa2)
regex = helper.dfa_to_regex(
    hop_table, dfa2.startState, dfa2.FinalStates, dfa2)

regex = regex.replace('()*', '')
regex = regex.replace('($)', '')

expresion = tmp.REtoIR(regex)
dfa2 = expresion.to_dfa().minimize_dfa()

print(dfa2.is_equal(dfa))