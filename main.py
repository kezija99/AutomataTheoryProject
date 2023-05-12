from iRegular import IRegular
from Node import Node

#reg = input("Unesi regex: ")
tmp = IRegular()
expresion = tmp.REtoIR("ab|(c*d(xy)|z*)x")
print(str(expresion))
print(expresion.accepts('zzzzzzzyx'))