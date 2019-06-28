
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


def find_variable_producing_terminal(grammars,terminal):
    lst=set()
    for i in range(len(grammars)):
        for j in range(1,len(grammars[i])):
            if len(grammars[i][j])==1 and grammars[i][j]==terminal:
                lst.add(grammars[i][0])
    return list(lst)

def find_variable_poducing_two_variable(grammars,list_X,list_Y):
    producer_variable=set()
    for x in range(len(list_X)):
        for y in range(len(list_Y)):
            var_XY = list_X[x]+list_Y[y]
            for i in range(len(grammars)):
                for j in range(1,len(grammars[i])):
                    if len(grammars[i][j])==2 and grammars[i][j]==var_XY:
                        producer_variable.add(grammars[i][0])
    return list(producer_variable)
    



def CYK(input_string , grammars):
    size = len(input_string)
    table = [[list() for j in range(0,size)] for n in range(0,size)]

    for row in range(size):
        for col in range(size):
            if row==col:
                table[row][col].extend(find_variable_producing_terminal(grammars,input_string[row]))
    
    for distance in range(1,size):
        for row in range(size-distance):
            col = row + distance
            result=set()
            for i in range(row,col):
                list_X = table[row][i][:]
                list_Y = table[i+1][col][:]
                lst = find_variable_poducing_two_variable(grammars,list_X,list_Y)
                result.update(set(lst))
            table[row][col].extend(list(result))
    if 'S' in table[0][size-1]:
        print("accept")
    else:
        print("reject")

            





if __name__ == "__main__":
    grammars=read_grammar()
    input_string= input()
    CYK(input_string,grammars)