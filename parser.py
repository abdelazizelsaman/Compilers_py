import scanner
index = 0
TOKENCLASS = 'class'
TOKENLEXEME = 'lexeme'
IDENTIFIER = 'identifier'
NUMBER = 'number'
FLAG = True
flag_rep = False
PROGRAM = 'program'
STMTSEQ = ' stmt_sequence'
STATAMENT = 'statament'
IFSTMT = 'if-stmt'
REPEATSTMT = 'repeat-stmt'
ASSIGNSTMT = 'assign-stmt'
READSTMT = 'read-stmt'
WRITESTMT = 'write-stmt'
COMPARISONOP = 'comparison-op'
SIMPLEEXP = 'simple-exp'
ADDOP = 'addop'
MULOP = 'mulop'
IF = 'if'
ELSE = 'else'
EXP = 'exp'
THEN = 'then'
END = 'end'
UNTIL = 'until'
TERM = 'term'
FOUND = ' is Found in '
MISSING = ' is Missing in '

tokenList_dummy = []
file = open('tiny_sample_code.txt', 'r')
tokenList_dummy = scanner.tokenize(file.read())
print(tokenList_dummy)

def printOutput(strg):
    with open('parser_output.txt', 'w') as f:
        f.write("%s\n" % strg)   

def success():
    global FLAG
    FLAG = True
    print('Expected Input : '+getToken(TOKENLEXEME))

def failed():
    global FLAG
    FLAG = False
    print('Syntax Error : ')

def nextToken():
    global index
    index = index + 1

def getToken(param):
    global index
    if index < len(tokenList_dummy):
        return  tokenList_dummy[index].get(param, 'none')
    else:
        StopIteration()    

def match(token, param):
    flag = False
    if token == getToken(param):
        success()
        flag = True
    else:
        failed()
    nextToken()
    return flag 
   

def program():
    global index
    ##
    print(PROGRAM + FOUND)
    ##
    stmtSeq()
    if index < len(tokenList_dummy):
        print('Syntax Error : Expected ; \n') 
        program()

def stmtSeq():
    print(STMTSEQ + FOUND)
    statament()
    while getToken(TOKENLEXEME) == ';':
        match(';', TOKENLEXEME)
        statament()



def statament():
    if 'if' == getToken(TOKENLEXEME):
        print(STATAMENT + FOUND)
        ifstmt()
    elif 'repeat' == getToken(TOKENLEXEME):
        print(STATAMENT + FOUND)
        repeatStmt()
    elif IDENTIFIER == getToken(TOKENCLASS):
        print(STATAMENT + FOUND)
        assignstmt()
    elif 'read' == getToken(TOKENLEXEME):
        print(STATAMENT + FOUND)
        readStmt()
    elif 'write' == getToken(TOKENLEXEME):
        print(STATAMENT +FOUND)
        writeStmt()
    else:
        if index < len(tokenList_dummy) and not flag_rep:
            match(False,TOKENCLASS)
            print(STATAMENT + MISSING)
            statament()    


def ifstmt():
    print(IFSTMT+FOUND if match('if', TOKENLEXEME) else IFSTMT+MISSING+IFSTMT)
    print(IF+FOUND)
    exp()
    print( THEN+FOUND if  match('then', TOKENLEXEME) else THEN+MISSING+IFSTMT)
    stmtSeq()
    if getToken(TOKENLEXEME) == 'else':
        print( ELSE+FOUND if match('else', TOKENLEXEME) else ELSE+MISSING+IFSTMT)
        stmtSeq()
    print(END+FOUND if match('end', TOKENLEXEME) else END+MISSING+IFSTMT)    

def repeatStmt():
    global flag_rep
    flag_rep = True
    print( REPEATSTMT+FOUND if match('repeat', TOKENLEXEME) else REPEATSTMT+MISSING+REPEATSTMT)
    stmtSeq()
    print(UNTIL+FOUND if match('until', TOKENLEXEME) else UNTIL+MISSING+REPEATSTMT)
    exp()
    flag_rep = False

def assignstmt():
    print(ASSIGNSTMT+FOUND)
    print(IDENTIFIER+FOUND)
    match(IDENTIFIER, TOKENCLASS)
    if match(':=', TOKENLEXEME):
        print(':='+FOUND)
        exp()
    else:
        print('=:'+MISSING+ASSIGNSTMT)
    
        

def readStmt():
    print(READSTMT+FOUND)
    match('read', TOKENLEXEME)
    print(IDENTIFIER+FOUND if match(IDENTIFIER, TOKENCLASS) else IDENTIFIER+MISSING+READSTMT)   
        

def writeStmt():
    print(WRITESTMT+FOUND)
    match('write', TOKENLEXEME)
    exp()

def exp():
    print(EXP+FOUND)
    simpleExp()
    if '=' == getToken(TOKENLEXEME) or '<' == getToken(TOKENLEXEME):
        comparisonOp()
        simpleExp()

def comparisonOp():
    print(COMPARISONOP+FOUND)
    match(getToken(TOKENLEXEME),TOKENLEXEME)

def simpleExp():
    print(SIMPLEEXP+FOUND)
    term()
    while getToken(TOKENLEXEME) == '+' or getToken(TOKENLEXEME) == '-':
        addOp() 
        term()

def addOp():
    print(ADDOP+FOUND)
    match(getToken(TOKENLEXEME),TOKENLEXEME)

def term():
    print(TERM+FOUND)
    factor()
    while getToken(TOKENLEXEME) == '/' or getToken(TOKENLEXEME) == '*':
        mulOp()
        factor()

def mulOp():
    print(MULOP+FOUND)
    match(getToken(TOKENLEXEME),TOKENLEXEME)

def factor():
    if '(' == getToken(TOKENLEXEME):
        match('(',TOKENLEXEME)
        exp()
        match(')',TOKENLEXEME)
    elif getToken(TOKENCLASS) == NUMBER:
        print(NUMBER+FOUND)
        match(getToken(TOKENCLASS), TOKENCLASS) 
    elif getToken(TOKENCLASS) == IDENTIFIER:
        match(getToken(TOKENCLASS), TOKENCLASS)
    else:
        match(False,TOKENCLASS)
        print('factor'+MISSING+TERM) 
        factor()   


program()


        
                
        