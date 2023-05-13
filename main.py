from iRegular import IRegular
from Node import Node

#reg = input("Unesi regex: ")
tmp = IRegular()
expresion = tmp.REtoIR("a*b|(cd)*xy").minimize_dfa()
#print(str(expresion))
dfa = expresion.minimize_dfa()
#print(str(dfa))
print(dfa.accepts('xy'))