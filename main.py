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

print("===================================")
expresion = tmp.re_to_ir('(abc|((ab*|ε|b*)))(abc|((ab*|ε|b*)))**|c*')
dfa = expresion.to_dfa().minimize_dfa()
print(str(dfa.minimize_dfa()))

a_nfa = DFA('q0', {'q0', 'q2', 'q3', 'q4', 'q5', 'q6'}, {('q0', 'a'): {'q3'}, ('q0', 'b'): {'q7'}, 
            ('q0', 'c'): {'q5'}, ('q1', 'a'): {'q9'}, ('q1', 'b'): {'q1'},
            ('q1', 'c'): {'q0'}, ('q2', 'a'): {'q8'}, ('q2', 'b'): {'q1'},
            ('q2', 'c'): {'q6'}, ('q3', 'a'): {'q3'}, ('q3', 'b'): {'q4'},
            ('q3', 'c'): {'q9'}, ('q4', 'a'): {'q1'}, ('q4', 'b'): {'q7'},
            ('q4', 'c'): {'q7'}, ('q5', 'a'): {'q9'}, ('q5', 'b'): {'q1'},
            ('q5', 'c'): {'q5'}, ('q6', 'a'): {'q2'}, ('q6', 'b'): {'q8'},
            ('q6', 'c'): {'q4'}, ('q7', 'a'): {'q3'}, ('q7', 'b'): {'q7'},
            ('q7', 'c'): {'q9'}, ('q8', 'a'): {'q6'}, ('q8', 'b'): {'q2'},
            ('q8', 'c'): {'q2'}, ('q9', 'a'): {'q9'}, ('q9', 'b'): {'q9'},
            ('q9', 'c'): {'q9'}
            })
min_a_dfa = a_nfa.minimize_dfa()
regex = helper.dfa_to_regex(min_a_dfa)
print(regex)