def sympleticform(operator_a,operator_b):
    'A is an operator in the list [X,Y,Z,I]'
    'B is an operator in the list [X,Y,Z,I]'
    'Returns the sign of (-1)^(symplectic form)'

    if (operator_a == 'X'):
        if(operator_b == 'X'):
            return 1
        elif(operator_b == 'Y'):
            return -1
        elif(operator_b == 'Z'):
            return -1
        else:
            return 1
    elif(operator_a == 'Y'):
        if(operator_b == 'X'):
            return -1
        elif(operator_b == 'Y'):
            return 1
        elif(operator_b == 'Z'):
            return -1
        else:
            return 1
    elif(operator_b == 'Z'):
        if(operator_b == 'X'):
            return -1
        elif(operator_b == 'Y'):
            return -1
        elif(operator_b == 'Z'):
            return 1
        else:
            return 1
    elif(operator_a == 'I'):
        if(operator_b == 'X'):
            return 1
        elif(operator_b == 'Y'):
            return 1
        elif(operator_b == 'Z'):
            return 1
        else:
            return 1    
