import scanner
index = 0
tokenList_dummy = []
file = open('tiny_sample_code.txt', 'r')
tokenList_dummy = scanner.tokenize(file.read())

def success():
    print('Expected')

def failed():
     print('Error')   

def nextToken():
    global index
    index = index + 1

def getTokenClass():
    global index
    return  tokenList_dummy[index].get('class', 'none')

def getToken():
    global index
    return  tokenList_dummy[index].get('lexeme', 'none')

def match(identifier, token):
    state = True if identifier == token else False
    print('Expected' if state else 'Error')

def program():
    stmtseq()

def stmtseq():
    statament()
    if ';' == getToken():
        statament()



def statament():
    if 'if' == getTokenClass():
        ifstmt()
    elif 'repeat' == getTokenClass():
        repeatstmt()
    elif 'assign' == getTokenClass():
        assignstmt()
    elif 'read' == getTokenClass():
        readstmt()
    elif 'write' == getTokenClass():
        writestmt()
    else:
        failed()

def ifstmt():
    exp()
    match('then', getTokenClass())

def repeatstmt():
    stmtseq()
    if 'until' == getToken():
        exp()
    else:
        failed()
    return True

def assignstmt():
    if getToken() not in scanner.__identifiers[1]:
        if getToken() == '=:':
            exp()
    else:
        failed()
        

def readstmt():
    if getToken not in scanner.__identifiers[1]:
        success()
    else:
        failed()    
        

def writestmt():
    exp()

def exp():
    simpleexp()
    if '=' == getToken | '<' == getToken():
        comparisonop()
        simpleexp()
    else:
        exp()

def comparisonop():
    success()

def simpleexp():
    if '+' == getToken() | '-' == getToken():
        addop()
        term()
    else:
        term()

def addop():
    success()

def term():
    if '*' == getToken() | '/' == getToken():
        mulop()
        factor()
    else:
        factor()

def mulop():
    success()

def factor():
    if '(' == getToken():
        exp()
        if ')' != getToken():
            failed()
    elif getToken() in [0,1,2,3,4,5,6,7,8,9]:
        success()
    elif getToken() not in scanner.__identifiers[1]:
        success()
    else:
        failed()    





        
                
        