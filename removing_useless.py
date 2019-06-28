from collections import defaultdict 
import string
import copy


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


def generative_variable(grammars):
    generative_list1 = set()
    generative_list2 = set()
    for i in range(len(grammars)):
        is_generative = 1
        for j in range(1,len(grammars[i])):
            is_generative = 1
            for k in range(len(grammars[i][j])):
                if  grammars[i][j][k].islower()==0:
                    is_generative = 0
                    break
            if is_generative==1 : 
                generative_list2.add(grammars[i][0])
                continue
    while (generative_list1 != generative_list2):
        generative_list1 = copy.deepcopy(generative_list2)
        for i in range(len(grammars)):
            flag_new_generative = 1
            for j in range(1,len(grammars[i])):
                flag_new_generative = 1
                for k in range(len(grammars[i][j])):
                    if  grammars[i][j][k] not in generative_list1 and grammars[i][j][k].islower()==0 :
                        flag_new_generative = 0
                        break
                if ( flag_new_generative == 1):
                    generative_list2.add(grammars[i][0])
                    break
        
    return generative_list2



def delete_unreachable_variable_form_s(grammars):
    dependency_graph = Graph() 
    for i in range(len(grammars)):
        for j in range(1,len(grammars[i])):
            for k in range(0,len(grammars[i][j])):
                if grammars[i][j][k].islower()==0 and grammars[i][j][k]!='#' :
                    dependency_graph.addEdge(grammars[i][0],grammars[i][j][k])
    reachable_variable = dependency_graph.BFS('S')
    lst = []
    for i in range(len(grammars)):
        if grammars[i][0] not in reachable_variable:
            continue
        else:
            lst.append(grammars[i])
    grammars=lst
    return grammars
    


def remove_non_generative_production(grammars,generative_variable):
    new_grammar = []
    for i in range(len(grammars)):
        lst=[]
        if grammars[i][0] in generative_variable:
            lst.append(grammars[i][0])
            for j in range(1,len(grammars[i])):
                is_generative=1
                for k in range(0,len(grammars[i][j])):
                    if grammars[i][j][k].islower() == 0 and grammars[i][j][k] not in generative_variable:
                        is_generative = 0
                if is_generative == 1 or grammars[i][j]=='#':
                    if grammars[i][j] not in lst:
                        lst.append(grammars[i][j])
            new_grammar.append(lst)
    grammars = new_grammar
    return grammars


def print_new_grammar(grammars):
    for i in range(len(grammars)):
        row_list = []
        for j in grammars[i]:
            if j not in row_list and j!='' :
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
generative_variables = generative_variable(grammars)
grammars = remove_non_generative_production(grammars,generative_variables)
grammars = delete_unreachable_variable_form_s(grammars)
print_new_grammar(grammars)