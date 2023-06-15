from IRegular import IRegular
from IRegular import DFA, NFA
from Regular import Regular
def test_regex():
    l1 = IRegular.re_to_ir('a(a)*')
    assert l1.accepts("a")
    assert l1.accepts("aaa")
    assert l1.accepts("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert not l1.accepts("")
    assert l1.complement().is_equal(DFA('q0', {'q0'}, {('q0', 'a'): {'q1'}, ('q1', 'a'): {'q1'}}))

    l2 = l1.to_dfa().minimize_dfa()
    assert l2.complement().is_equal(DFA('q0', {'q0'}, {('q0', 'a'): {'q1'}, ('q1', 'a'): {'q1'}}))

    empty = IRegular.re_to_ir('ε')
    a_star = empty.union(l1).to_dfa().minimize_dfa()
    
    assert a_star.is_equal(IRegular.re_to_ir('a*').to_dfa())

def test_union():
    l1 = IRegular.re_to_ir('aa|bb|(a|b|c)*')
    l2 = IRegular.re_to_ir('(aa)|(bb)')

    assert l1.is_equal(l1.union(l2).to_dfa())

    l3 = IRegular.re_to_ir('(a|b|c)*')

    empty = NFA('q0', {}, {})

    assert l1.is_equal(l1.union(empty).to_dfa())
    assert l2.is_equal(l2.union(empty).to_dfa())
    assert l3.is_equal(l3.union(empty).to_dfa())

    assert l1.is_equal(empty.union(l1).to_dfa())
    assert l2.is_equal(empty.union(l2).to_dfa())
    assert l3.is_equal(empty.union(l3).to_dfa())

def test_accept():
    l1 = IRegular.re_to_ir('aa|bb|(a|b|c)*')
    l2 = IRegular.re_to_ir('(aa)|(bb)')
    l3 = IRegular.re_to_ir('(a|b|c)*')
    l4 = IRegular.re_to_ir('a*|b*|c*')

    assert l1.accepts('aa') and l1.accepts('bb') and l1.accepts('abbc') and l1.accepts('aaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbccccccccccccccc')
    assert l2.accepts('aa') and l2.accepts('bb') and not l2.accepts('a')  and not l2.accepts('aaa') and not l2.accepts('b')

def test_conversion():
    helper = Regular()
    
    a_nfa = NFA('q0', {'q1'}, {('q0', 'a'): {'q1'}})
    min_a_dfa = a_nfa.to_dfa().minimize_dfa()
    
    regex = helper.dfa_to_regex(min_a_dfa)
    
    expresion = IRegular.re_to_ir(regex)
    a_dfa2 = expresion.to_dfa().minimize_dfa()

    assert a_nfa.to_dfa().minimize_dfa().is_equal(a_dfa2)
    assert regex.replace('(ε)', '') == '(a)'

    a_star_dfa = DFA('q0', {'q0'}, {('q0', 'a'): {'q0'}})
    min_a_star_dfa = a_star_dfa.minimize_dfa()

    regex = helper.dfa_to_regex(min_a_star_dfa)
    
    expresion = IRegular.re_to_ir(regex)
    a_star_dfa2 = expresion.to_dfa().minimize_dfa()

    assert a_star_dfa.is_equal(a_star_dfa2)
    assert regex.replace('(ε)', '') == '(a)*'

    a_or_b_dfa = DFA('q0', {'q1'}, {('q0', 'a'): {'q1'}, ('q0', 'b'): {'q1'}, ('q1', 'a'): {'q2'}, ('q1', 'b'): {'q2'}, ('q2', 'a'): {'q2'}, ('q2', 'b'): {'q2'}})
    min_a_or_b_dfa = a_or_b_dfa.minimize_dfa()

    regex = helper.dfa_to_regex(min_a_or_b_dfa)
    
    expresion = IRegular.re_to_ir(regex)
    a_or_b_dfa2 = expresion.to_dfa().minimize_dfa()

    assert a_or_b_dfa.is_equal(a_or_b_dfa2)
    assert regex.replace('(ε)', '') == '(a)|(b)' or '(b)|(a)'