#   CSE 226 Design of Compilers - CHEP ASU
#   Author: Ahmed Abdelaziz
#   Project title: Parser for TINY language complier
#   Project Description:

#       The role of the parser is to take input in the form of a sequence
#       of tokens or program instructions and build a data structure 
#       in the form of a parse tree or an abstract syntax tree.


import scanner
from itertools import groupby
index = 0
state = 'program'
TOKENCLASS = 'class'
TOKENLEXEME = 'lexeme'
IDENTIFIER = 'identifier'
NUMBER = 'number'
FLAG = True
flag_rep = False
flag_if = False
flag_as = False
flag_wr = False

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

state_log = []
parser_log = []
tokenList_dummy = []
file = open('tiny_sample_code.txt', 'r')
tokenList_dummy = scanner.tokenize(file.read())
#print(tokenList_dummy)

def cstate(strg):
    global state
    global state_log
    global flag_if
    state = strg
    level = ""
    if flag_if:
        level += "|--"
    if flag_rep:
        level += "|--"
    if flag_as:
        level += "|--"   
    if flag_wr:
        level += "|--"
    state_log.append(level+strg)

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
        printOutput(STATAMENT + FOUND )
        ifstmt()
    elif 'repeat' == getToken(TOKENLEXEME):
        printOutput(STATAMENT + FOUND)
        repeatStmt()
    elif IDENTIFIER == getToken(TOKENCLASS):
        printOutput(STATAMENT + FOUND)
        assignstmt()
    elif 'read' == getToken(TOKENLEXEME):
        printOutput(STATAMENT + FOUND)
        readStmt()
    elif 'write' == getToken(TOKENLEXEME):
        printOutput(STATAMENT +FOUND)
        writeStmt()
    else:
        if index < len(tokenList_dummy) and not flag_rep and not flag_if :
            match(False,TOKENCLASS)
            printOutput(STATAMENT + MISSING)
            statament()    


def ifstmt():
    global flag_if
    cstate(IFSTMT)
    flag_if = True
    
    printOutput(IFSTMT+FOUND + state if match('if', TOKENLEXEME) else IFSTMT+MISSING+IFSTMT)
    printOutput(IF+FOUND + state)
    exp()

    if match('then', TOKENLEXEME):
        printOutput(THEN+FOUND+state)
        cstate(THEN)
        stmtSeq()
    else:
        printOutput(THEN+MISSING+IFSTMT)

    if getToken(TOKENLEXEME) == 'else':
        printOutput(ELSE+FOUND)
        cstate(ELSE)
        stmtSeq()
    #else:
        #printOutput(ELSE+MISSING+IFSTMT)
        
    if match('end', TOKENLEXEME):
        printOutput(END+FOUND + state)
        flag_if = False
        cstate(END)
    else:
        printOutput(END+MISSING + IFSTMT)


def repeatStmt():
    cstate(REPEATSTMT)
    global flag_rep
    flag_rep = True
    printOutput( REPEATSTMT+FOUND + state if match('repeat', TOKENLEXEME) else REPEATSTMT+MISSING+REPEATSTMT)
    stmtSeq()
    if match('until', TOKENLEXEME):
        printOutput(UNTIL+FOUND+state)
        cstate(UNTIL)
    else:
        printOutput(UNTIL+MISSING+REPEATSTMT)
    exp()
    flag_rep = False

def assignstmt():
    cstate(ASSIGNSTMT)
    global flag_as
    flag_as = True
    cstate(IDENTIFIER)
    printOutput(ASSIGNSTMT+FOUND + state)
    printOutput(IDENTIFIER+FOUND + state)
    match(IDENTIFIER, TOKENCLASS)
    if match(':=', TOKENLEXEME):
        printOutput(':='+FOUND + state)
        exp()
    else:
        printOutput('=:'+MISSING+ASSIGNSTMT)
    flag_as = False    
    
        

def readStmt():
    cstate(READSTMT)
    printOutput(READSTMT+FOUND + state)
    match('read', TOKENLEXEME)
    printOutput(IDENTIFIER+FOUND + state if match(IDENTIFIER, TOKENCLASS) else IDENTIFIER+MISSING+READSTMT)   
        

def writeStmt():
    cstate(WRITESTMT)
    global flag_wr
    flag_wr = True
    printOutput(WRITESTMT+FOUND + state)
    match('write', TOKENLEXEME)
    exp()
    flag_wr = False

def exp():
    printOutput(EXP+FOUND + state)
    simpleExp()
    if '=' == getToken(TOKENLEXEME) or '<' == getToken(TOKENLEXEME):
        cstate(getToken(TOKENLEXEME))
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
    cstate(ADDOP)
    printOutput(ADDOP+FOUND + state)
    match(getToken(TOKENLEXEME),TOKENLEXEME)

def term():
    printOutput(TERM+FOUND + state)
    factor()
    while getToken(TOKENLEXEME) == '/' or getToken(TOKENLEXEME) == '*':
        mulOp()
        factor()

def mulOp():
    cstate(MULOP)
    printOutput(MULOP+FOUND + state)
    match(getToken(TOKENLEXEME),TOKENLEXEME)

def factor():
    if '(' == getToken(TOKENLEXEME):
        match('(',TOKENLEXEME)
        exp()
        match(')',TOKENLEXEME)
    elif getToken(TOKENCLASS) == NUMBER:
        cstate(NUMBER)
        printOutput(NUMBER+FOUND + state)
        match(getToken(TOKENCLASS), TOKENCLASS) 
    elif getToken(TOKENCLASS) == IDENTIFIER:
        cstate(IDENTIFIER)
        match(getToken(TOKENCLASS), TOKENCLASS)
        printOutput(IDENTIFIER+FOUND + state)
    else:
        match(False,TOKENCLASS)
        printOutput('factor'+MISSING+TERM) 
        factor()   


program()
with open('parser_output.txt', 'w') as f:
    for item in parser_log:
        f.write("%s\n" % item)    

res = [i[0] for i in groupby(state_log)]

with open('state_log.txt', 'w') as f:
    for item in res:
        f.write("%s\n" % item)    