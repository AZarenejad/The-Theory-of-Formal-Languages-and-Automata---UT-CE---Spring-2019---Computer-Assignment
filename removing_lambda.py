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
nullable_variable = nullable_variable(grammars)
removing_landa(grammars,nullable_variable)
print_new_grammar(grammars)


