class Node:
    def __init__(self, data):
            self.left = None
            self.right = None
            self.data = data
    
    def __str__(self):
        return self.data
        
    @staticmethod
    def evaluate_stack(s):
        if len(s) == 1:
            return s.pop()
        else:
            t = Node("•")
            t.right = s.pop()
            t.left = Node.evaluate_stack(s)
            return t
            
    @staticmethod 
    def tree(RI: str, i):
        s = []
        while i < len(RI):
            if RI[i] == '(':
                i += 1
                sub_expression, sub_i = Node.tree(RI, i)
                s.append(sub_expression)
                i = sub_i
            elif RI[i] == ')':
                return Node.evaluate_stack(s), i
            elif RI[i] == '|':
                temp = Node("|")
                temp.left = Node.evaluate_stack(s)
                i += 1
                temp.right, i = Node.tree(RI, i)
                return temp, i
            elif RI[i] == '*':
                temp = Node("*")
                temp.left = s.pop()
                s.append(temp)
            else:
                temp = Node(RI[i] + '')
                s.append(temp)
            i += 1
        return Node.evaluate_stack(s), i

        
    @staticmethod
    def parsing_tree(RE: str):
        i = 0
        return Node.tree(RE, i)[0]