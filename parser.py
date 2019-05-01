import scanner
index = 0
state = 'program'
TOKENCLASS = 'class'
TOKENLEXEME = 'lexeme'
IDENTIFIER = 'identifier'
NUMBER = 'number'
FLAG = True
flag_rep = False
PROGRAM = 'program'
STMTSEQ = 'stmt_sequence'
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
FOUND = ' is found in '
MISSING = ' is Missing in '


parser_log = []
tokenList_dummy = []
file = open('test.txt', 'r')
tokenList_dummy = scanner.tokenize(file.read())
#print(tokenList_dummy)

def cstate(strg):
    global state
    state = strg

def printOutput(strg):
    global parser_log
    print(strg)
    parser_log.append(strg)


def success():
    global FLAG
    FLAG = True
    #printOutput('Expected Input : '+getToken(TOKENLEXEME))

def failed():
    global FLAG
    FLAG = False
    printOutput('Syntax Error : ')

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
    printOutput(PROGRAM + FOUND)
    ##
    stmtSeq()
    if index < len(tokenList_dummy):
        printOutput('Syntax Error : Expected ; in ' + state+'\n') 
        program()

def stmtSeq():
    printOutput(STMTSEQ + FOUND + state)
    statament()
    while getToken(TOKENLEXEME) == ';':
        match(';', TOKENLEXEME)
        statament()


def statament():
    if 'if' == getToken(TOKENLEXEME):
        printOutput(STATAMENT + FOUND + state)
        cstate(IFSTMT)
        ifstmt()
    elif 'repeat' == getToken(TOKENLEXEME):
        printOutput(STATAMENT + FOUND + state)
        cstate(READSTMT)
        repeatStmt()
    elif IDENTIFIER == getToken(TOKENCLASS):
        printOutput(STATAMENT + FOUND + state)
        cstate(ASSIGNSTMT)
        assignstmt()
    elif 'read' == getToken(TOKENLEXEME):
        printOutput(STATAMENT + FOUND + state)
        cstate(READSTMT)
        readStmt()
    elif 'write' == getToken(TOKENLEXEME):
        printOutput(STATAMENT +FOUND + state)
        cstate(WRITESTMT)
        writeStmt()
    else:
        if index < len(tokenList_dummy) and not flag_rep:
            match(False,TOKENCLASS)
            printOutput(STATAMENT + MISSING)
            statament()    


def ifstmt():
    printOutput(IFSTMT+FOUND + state if match('if', TOKENLEXEME) else IFSTMT+MISSING+IFSTMT)
    printOutput(IF+FOUND + state)
    exp()
    printOutput( THEN+FOUND + state if  match('then', TOKENLEXEME) else THEN+MISSING+IFSTMT)
    stmtSeq()
    if getToken(TOKENLEXEME) == 'else':
        printOutput( ELSE+FOUND + state if match('else', TOKENLEXEME) else ELSE+MISSING+IFSTMT)
        stmtSeq()
    printOutput(END+FOUND + state if match('end', TOKENLEXEME) else END+MISSING+IFSTMT)    

def repeatStmt():
    global flag_rep
    flag_rep = True
    printOutput( REPEATSTMT+FOUND + state if match('repeat', TOKENLEXEME) else REPEATSTMT+MISSING+REPEATSTMT)
    stmtSeq()
    printOutput(UNTIL+FOUND + state if match('until', TOKENLEXEME) else UNTIL+MISSING+REPEATSTMT)
    exp()
    flag_rep = False

def assignstmt():
    printOutput(ASSIGNSTMT+FOUND + state)
    printOutput(IDENTIFIER+FOUND + state)
    match(IDENTIFIER, TOKENCLASS)
    if match(':=', TOKENLEXEME):
        printOutput(':='+FOUND + state)
        exp()
    else:
        printOutput('=:'+MISSING+ASSIGNSTMT)
    
        

def readStmt():
    printOutput(READSTMT+FOUND + state)
    match('read', TOKENLEXEME)
    printOutput(IDENTIFIER+FOUND + state if match(IDENTIFIER, TOKENCLASS) else IDENTIFIER+MISSING+READSTMT)   
        

def writeStmt():
    printOutput(WRITESTMT+FOUND + state)
    match('write', TOKENLEXEME)
    exp()

def exp():
    printOutput(EXP+FOUND + state)
    simpleExp()
    if '=' == getToken(TOKENLEXEME) or '<' == getToken(TOKENLEXEME):
        comparisonOp()
        simpleExp()

def comparisonOp():
    printOutput(COMPARISONOP+FOUND + state)
    match(getToken(TOKENLEXEME),TOKENLEXEME)

def simpleExp():
    printOutput(SIMPLEEXP+FOUND + state)
    term()
    while getToken(TOKENLEXEME) == '+' or getToken(TOKENLEXEME) == '-':
        addOp() 
        term()

def addOp():
    printOutput(ADDOP+FOUND + state)
    match(getToken(TOKENLEXEME),TOKENLEXEME)

def term():
    printOutput(TERM+FOUND + state)
    factor()
    while getToken(TOKENLEXEME) == '/' or getToken(TOKENLEXEME) == '*':
        mulOp()
        factor()

def mulOp():
    printOutput(MULOP+FOUND + state)
    match(getToken(TOKENLEXEME),TOKENLEXEME)

def factor():
    if '(' == getToken(TOKENLEXEME):
        match('(',TOKENLEXEME)
        exp()
        match(')',TOKENLEXEME)
    elif getToken(TOKENCLASS) == NUMBER:
        printOutput(NUMBER+FOUND + state)
        match(getToken(TOKENCLASS), TOKENCLASS) 
    elif getToken(TOKENCLASS) == IDENTIFIER:
        match(getToken(TOKENCLASS), TOKENCLASS)
    else:
        match(False,TOKENCLASS)
        printOutput('factor'+MISSING+TERM) 
        factor()   


program()
with open('parser_output.txt', 'w') as f:
    for item in parser_log:
        f.write("%s\n" % item)    
