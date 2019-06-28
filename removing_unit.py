from collections import defaultdict 
import string

def find_non_unit_term_by_start_variable_in_grammar_list(var,grammars):
    lst=[]
    for i in range(len(grammars)):
        if grammars[i][0]==var:
            for j in range(1,len(grammars[i])):
                if len(grammars[i][j])!=1 or grammars[i][j].islower()==1 or grammars[i][j]=='#':
                    lst.append(grammars[i][j])
    return lst

class Graph:
    def __init__(self):
        self.graph = defaultdict(set)
    def addEdge(self,u,v):
        self.graph[u].add(v)
    def BFS(self, s):
        visited={}
        lst = list(string.ascii_uppercase)
        for x in lst:
            visited[x]=False
        visited['#']= False
        reachable=[]
        queue = [] 
        queue.append(s) 
        visited[s] = True
        while queue:
            s = queue.pop(0)
            reachable.append(s)
            for i in self.graph[s]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
        return reachable




def read_grammar():
    lines=[]
    grammars = []
    grammar_line = []
    line = input()
    while line!='$':
        lines.append(line)
        line = input()
    for i in range(len(lines)):
        grammar_line=[]
        split_line = lines[i][3:len(lines[i])].split('|')
        grammar_line.append(lines[i][0])
        grammar_line.extend(split_line)
        grammars.append(grammar_line)
    return grammars



def delete_unit(grammars):
    unit_depedency = Graph()
    grammar_with_deleting_unit_term=[]
    for i in range(len(grammars)):
        lst = []
        lst.append(grammars[i][0])
        for j in range(1,len(grammars[i])):
            if len(grammars[i][j])==1 and grammars[i][j].islower()==0 :
                unit_depedency.addEdge(grammars[i][0],grammars[i][j])
            else:
                lst.append(grammars[i][j])
        grammar_with_deleting_unit_term.append(lst)
    
    new_grammar = grammar_with_deleting_unit_term[:]
    for i in range(len(grammars)):
        reach_unit_variable = unit_depedency.BFS(grammars[i][0])[1:]
        lst=[]
        for var in reach_unit_variable:
            lst.extend(find_non_unit_term_by_start_variable_in_grammar_list(var,grammars))
        new_grammar[i].extend(lst)
    return new_grammar
            
    

def print_new_grammar(grammars):
    for i in range(len(grammars)):
        row_list = []
        for j in grammars[i]:
            if j not in row_list and j!='' and j!='#':
                row_list.append(j)
        result_str = row_list[0]+"->"
        if len(row_list) == 2:
            result_str+=row_list[1]
            print(result_str)
        else:
            for j in range(1,len(row_list)-1):
                result_str+=row_list[j]+"|"
            result_str+=row_list[len(row_list)-1]
            print(result_str)
    print('$')




grammars = read_grammar()
grammars = delete_unit(grammars)
print_new_grammar(grammars)