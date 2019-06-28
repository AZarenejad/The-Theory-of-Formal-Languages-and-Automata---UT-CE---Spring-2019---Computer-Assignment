from collections import defaultdict 
import string
import copy

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


def chamski_check(grammars):
    for i in range(len(grammars)):
        for j in range(1,len(grammars[i])):
            if len(grammars[i][j])==2:
                if grammars[i][j][0].islower()==1 or grammars[i][j][1].islower()==1:
                    return False
            elif len(grammars[i][j])==1 :
                if grammars[i][j].islower()==0:

                    return False
            else:
                return False
    return True

def nullable_variable(grammars):
    null_list1 = set()
    null_list2 = set()
    for i in range(len(grammars)): 
        for j in range(1,len(grammars[i])):
            if grammars[i][j] == '#' :
                null_list2.add(grammars[i][0])
    while (null_list1!=null_list2):
        null_list1 = null_list2
        for i in range(len(grammars)):
            flag_new_nullable = 1
            for j in range(1,len(grammars[i])):
                flag_new_nullable = 1
                for k in range(len(grammars[i][j])):
                    if grammars[i][j][k] not in null_list1:
                        flag_new_nullable = 0
                        break
                if ( flag_new_nullable == 1):
                    null_list2.add(grammars[i][0])
                    break
                else:continue
    return null_list2

def removing_landa(grammars,nullable_variable):
    for i in range(len(grammars)):
        lst = []
        j=1
        while lst != grammars[i]:
            lst = grammars[i][:]
            for k in range(0,len(grammars[i][j])):
                if grammars[i][j][k] in nullable_variable:
                    check_str = grammars[i][j]
                    new_str = check_str.replace(check_str[k],"")
                    grammars[i].append(new_str)
            j+=1

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

def simplify_grammar(grammars):
    nullable_variables = nullable_variable(grammars)
    removing_landa(grammars,nullable_variables)
    print("removing landa",grammars)
    grammars = delete_unit(grammars)
    print("removing unit",grammars)
    generative_variables = generative_variable(grammars)
    print("generative_variables",generative_variables)
    grammars = remove_non_generative_production(grammars,generative_variables)
    print("remove non generative variables", grammars)
    grammars = delete_unreachable_variable_form_s(grammars)
    print("remove unreachable variable form S", grammars)
    return grammars


def change_to_chamskey_form(grammars):
    all_variables = set(list(string.ascii_uppercase))
    variable_used =set()
    dic_terminal_to_variable_chamski={}

    for i in range(len(grammars)):
        variable_used.add(grammars[i][0])
        for j in range(1,len(grammars[i])):
            for k in range(0,len(grammars[i][j])):
                if grammars[i][j][k].islower()==0 and grammars[i][j][k]!='#':
                    variable_used.add(grammars[i][j][k])
    new_production_term=[]
    for i in range(len(grammars)):
        for j in range(1,len(grammars[i])):
            for k in range(len(grammars[i][j])):
                if grammars[i][j][k].islower()==1:
                    terminal = grammars[i][j][k]
                    if terminal in dic_terminal_to_variable_chamski:
                        grammars[i][j] = grammars[i][j].replace(terminal,dic_terminal_to_variable_chamski[terminal])
                    else:
                        new_variable = list(all_variables-variable_used)[0]
                        dic_terminal_to_variable_chamski[terminal]= new_variable
                        grammars[i][j] = grammars[i][j].replace(grammars[i][j][k],new_variable)
                        variable_used.add(new_variable)
                        lst=[new_variable,terminal]
                        new_production_term.append(lst)
    grammars.extend(new_production_term)
    new_production_term=[]
    print(grammars)
    for i in range(len(grammars)):
        for j in range(1,len(grammars[i])):
            while len(grammars[i][j])>2:
                new_variable = list(all_variables-variable_used)[0]
                two_var_should_mix =  str(grammars[i][j][-2] + grammars[i][j][-1])
                check_string = grammars[i][j]
                grammars[i][j] = grammars[i][j].replace(two_var_should_mix,new_variable)
                variable_used.add(new_variable)
                lst=[new_variable,two_var_should_mix]
                new_production_term.append(lst)
    grammars.extend(new_production_term)
    print(grammars)





    




if __name__ == "__main__":
    grammars = read_grammar()
    is_chamski = chamski_check(grammars)
    print(is_chamski)
    if (not is_chamski):
        grammar_after_simplify = simplify_grammar(grammars)
        change_to_chamskey_form(grammar_after_simplify)



