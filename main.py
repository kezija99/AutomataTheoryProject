from IRegular import IRegular, NFA, DFA
from Regular import Regular

tmp = IRegular()
helper = Regular()
a_nfa = NFA('q0', {'q7'}, {('q0', 'a'): {'q1'}, ('q0', 'ε'): {'q1', 'q2', 'q3'}, 
            ('q1', 'a'): {'q9'}, ('q1', 'b'): {'q2'}, ('q1', 'ε'): {'q2', 'q3'},
            ('q2', 'a'): {'q3'}, ('q2', 'ε'): {'q3'}, ('q3', 'a'): {'q7'},
            ('q3', 'b'): {'q8'}, ('q4', 'a'): {'q4', 'q5'}, ('q4', 'ε'): {'q0'},
            ('q5', 'a'): {'q5'}, ('q5', 'b'): {'q5'}, ('q5', 'ε'): {'q1', 'q2', 'q3'},
            ('q6', 'b'): {'q5'}, ('q6', 'ε'): {'q3'}, ('q7', 'ε'): {'q3'},
            ('q8', 'ε'): {'q7'}, ('q9', 'a'): {'q12'}, ('q9', 'b'): {'q10'},
            ('q10', 'a'): {'q10', 'q11'}, ('q12', 'a'): {'q11', 'q12'}, ('q12', 'b'): {'q12'}})
min_a_dfa = a_nfa.to_dfa().minimize_dfa()

print("============================================")
print(min_a_dfa.accepts(''))
regex = helper.dfa_to_regex(min_a_dfa)

print("============================================")
expresion = tmp.re_to_ir('(aa|bb)|(a|b|c)*cd|a(bcd)*')
ddfa1 = expresion.to_dfa().minimize_dfa()
dfa = expresion.to_dfa().minimize_dfa()
regex1 = helper.dfa_to_regex(dfa)

expresion = tmp.re_to_ir(regex1)
print(regex1)
dfa = expresion.to_dfa().minimize_dfa()
print(str(dfa))
print(str(ddfa1))
print('Poredjenje automaata ============ ' + str(dfa.is_equal(ddfa1)))
print('' + str(dfa.accepts('bb')))
print('' + str(dfa.accepts('abcdbcdbcdbcdbcdbcd')))
print('' + str(dfa.accepts('aaaaaaabccccd')))
print('' + str(dfa.accepts('cd')))
print('' + str(dfa.accepts('ab')))
regex = helper.dfa_to_regex(dfa)
expresion = tmp.re_to_ir(regex)
dfa = expresion.to_dfa().minimize_dfa()

print("===============DRUGA RUNDA====================")
print('Poredjenje automaata ============ ' + str(dfa.is_equal(ddfa1)))
print('' + str(dfa.accepts('bb')))
print('' + str(dfa.accepts('abcdbcdbcdbcdbcdbcdbc')))
print('' + str(dfa.accepts('aaaaaaabccccd')))
print('' + str(dfa.accepts('cd')))
print('' + str(dfa.accepts('ab')))

print("============================================")
expresion = tmp.re_to_ir('(a|B)*(c9|ε)|ε')
dfa1 = expresion.to_dfa().minimize_dfa()
dfa = expresion.to_dfa().minimize_dfa()
regex1 = helper.dfa_to_regex(dfa)

expresion = tmp.re_to_ir(regex1)
dfa = expresion.to_dfa().minimize_dfa()
print('Poredjenje automaata ============ ' + str(dfa.is_equal(dfa1)))
print('' + str(dfa.accepts('')))
print('' + str(dfa.accepts('aaaaBaaa')))
print('' + str(dfa.accepts('aaaaBaaac')))
print('' + str(dfa.accepts('aaaaBaaac9')))
print('' + str(dfa.accepts('c9')))
print('' + str(dfa.accepts('ε')))
regex = helper.dfa_to_regex( dfa)
expresion = tmp.re_to_ir(regex)
dfa = expresion.to_dfa().minimize_dfa()

print("===============DRUGA RUNDA====================")
print('Poredjenje automaata ============ ' + str(dfa.is_equal(ddfa1)))
print('' + str(dfa.accepts('')))
print('' + str(dfa.accepts('aaaaBaaa')))
print('' + str(dfa.accepts('aaaaBaaac')))
print('' + str(dfa.accepts('aaaaBaaac9')))
print('' + str(dfa.accepts('c9')))
print('' + str(dfa.accepts('ε')))