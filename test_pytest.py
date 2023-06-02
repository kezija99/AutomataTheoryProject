from IRegular import IRegular
from IRegular import DFA, NFA
from FAHelper import FAHelper
def test_regex():
    tmp = IRegular()
    L1 = tmp.REtoIR('a(a)*')
    assert L1.accepts("a")
    assert L1.accepts("aaa")
    assert L1.accepts("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert not L1.accepts("")
    assert L1.complement().is_equal(DFA('q0', {'q0'}, {('q0', 'a'): {'q1'}, ('q1', 'a'): {'q1'}}))

    L2 = L1.to_dfa().minimize_dfa()
    assert L2.complement().is_equal(DFA('q0', {'q0'}, {('q0', 'a'): {'q1'}, ('q1', 'a'): {'q1'}}))

    empty = tmp.REtoIR('ε')
    astar = empty.union(L1).to_dfa().minimize_dfa()
    
    assert astar.is_equal(tmp.REtoIR('a*').to_dfa())

def test_union():
    tmp = IRegular()
    L1 = tmp.REtoIR('aa|bb|(a|b|c)*')
    L2 = tmp.REtoIR('(aa)|(bb)')

    assert L1.is_equal(L1.union(L2).to_dfa())
    assert L2.complement().minimize_dfa().complement().is_equal(L2.to_dfa())

    L3 = tmp.REtoIR('(a|b|c)*')
    L4 = tmp.REtoIR('a*|b*|c*')

    assert not L3.is_equal(L4.to_dfa())

    empty = NFA('q0', {}, {})

    assert L1.is_equal(L1.union(empty).to_dfa())
    assert L2.is_equal(L2.union(empty).to_dfa())
    assert L3.is_equal(L3.union(empty).to_dfa())
    assert L4.is_equal(L4.union(empty).to_dfa())

    assert L1.is_equal(empty.union(L1).to_dfa())
    assert L2.is_equal(empty.union(L2).to_dfa())
    assert L3.is_equal(empty.union(L3).to_dfa())

def test_accept():
    tmp = IRegular()
    L1 = tmp.REtoIR('aa|bb|(a|b|c)*')
    L2 = tmp.REtoIR('(aa)|(bb)')
    L3 = tmp.REtoIR('(a|b|c)*')
    L4 = tmp.REtoIR('a*|b*|c*')

    assert L1.accepts('aa') and L1.accepts('bb') and L1.accepts('abbc') and L1.accepts('aaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbccccccccccccccc')
    assert L2.accepts('aa') and L2.accepts('bb') and not L2.accepts('a')  and not L2.accepts('aaa') and not L2.accepts('b')

def test_converison():
    tmp = IRegular()
    helper = FAHelper()
    
    a_dfa = DFA('q0', {'q1'}, {('q0', 'a'): {'q1'}, ('q1', 'a'): {'q2'}, ('q2', 'a'): {'q2'}})
    min_a_dfa = a_dfa.minimize_dfa()
    
    min_a_dfa = helper.handle_start_incoming(min_a_dfa)
    min_a_dfa = helper.handle_end_outgoing(min_a_dfa)
    hop_table = helper.get_input_symbol(min_a_dfa)
    regex = helper.dfa_to_regex(
        hop_table, min_a_dfa.startState, min_a_dfa.FinalStates, min_a_dfa).replace('($)', '').replace('()*', '')
    
    expresion = tmp.REtoIR(regex)
    a_dfa2 = expresion.to_dfa().minimize_dfa()

    assert a_dfa.is_equal(a_dfa2)
    assert regex == '(a)'

    a_star_dfa = DFA('q0', {'q0'}, {('q0', 'a'): {'q0'}})
    min_a_star_dfa = a_star_dfa.minimize_dfa()
    
    min_a_star_dfa = helper.handle_start_incoming(min_a_star_dfa)
    min_a_star_dfa = helper.handle_end_outgoing(min_a_star_dfa)
    hop_table = helper.get_input_symbol(min_a_star_dfa)
    regex = helper.dfa_to_regex(
        hop_table, min_a_star_dfa.startState, min_a_star_dfa.FinalStates, min_a_star_dfa).replace('($)', '').replace('()*', '')
    
    expresion = tmp.REtoIR(regex)
    a_star_dfa2 = expresion.to_dfa().minimize_dfa()

    assert a_star_dfa.is_equal(a_star_dfa2)
    assert regex == '(a)*'

    a_or_b_dfa = DFA('q0', {'q1'}, {('q0', 'a'): {'q1'}, ('q0', 'b'): {'q1'}, ('q1', 'a'): {'q2'}, ('q1', 'b'): {'q2'}, ('q2', 'a'): {'q2'}, ('q2', 'b'): {'q2'}})
    min_a_or_b_dfa = a_or_b_dfa.minimize_dfa()
    
    min_a_or_b_dfa = helper.handle_start_incoming(min_a_or_b_dfa)
    min_a_or_b_dfa = helper.handle_end_outgoing(min_a_or_b_dfa)
    hop_table = helper.get_input_symbol(min_a_or_b_dfa)
    regex = helper.dfa_to_regex(
        hop_table, min_a_or_b_dfa.startState, min_a_or_b_dfa.FinalStates, min_a_or_b_dfa).replace('($)', '').replace('()*', '')
    
    expresion = tmp.REtoIR(regex)
    a_or_b_dfa2 = expresion.to_dfa().minimize_dfa()

    assert a_or_b_dfa.is_equal(a_or_b_dfa2)
    assert regex == '(a)|(b)' or '(b)|(a)'

