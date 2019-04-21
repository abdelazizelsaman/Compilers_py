import scanner
from enum import Enum 
index = 0
TOKENCLASS = 'class'
TOKENLEXEME = 'lexeme'
IDENTIFIER = 'identifier'
NUMBER = 'number'

tokenList_dummy = []
file = open('tiny_sample_code.txt', 'r')
tokenList_dummy = scanner.tokenize(file.read())
print(tokenList_dummy)

def success():
    print('Expected Input : ' + str(getToken(TOKENLEXEME)))

def failed():
     print('Syntax Error : ' + str(getToken(TOKENLEXEME)))

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
    if token == getToken(param):
        success()
    else:
        failed()
    nextToken()
   

def program():
    stmtSeq()

def stmtSeq():
    statament()
    while getToken(TOKENLEXEME) == ';':
        match(';', TOKENLEXEME)
        statament()



def statament():
    if 'if' == getToken(TOKENLEXEME):
        ifstmt()
    elif 'repeat' == getToken(TOKENLEXEME):
        repeatStmt()
    elif IDENTIFIER == getToken(TOKENCLASS):
        assignstmt()
    elif 'read' == getToken(TOKENLEXEME):
        readStmt()
    elif 'write' == getToken(TOKENLEXEME):
        writeStmt()
    else:
        match(False,TOKENCLASS)    
        nextToken()


def ifstmt():
    match('if', TOKENLEXEME)
    exp()
    match('then', TOKENLEXEME)
    stmtSeq()
    if getToken(TOKENLEXEME) == 'else':
        match('else', TOKENLEXEME)
        stmtSeq()
    match('end', TOKENLEXEME)    

def repeatStmt():
    match('repeat', TOKENLEXEME)
    stmtSeq()
    match('until', TOKENLEXEME)
    exp()

def assignstmt():
    match(IDENTIFIER, TOKENCLASS)
    match(':=', TOKENLEXEME)
    exp()
        

def readStmt():
    match('read', TOKENLEXEME)
    match(IDENTIFIER, TOKENCLASS)   
        

def writeStmt():
    match('write', TOKENLEXEME)
    exp()

def exp():
    simpleExp()
    if '=' == getToken(TOKENLEXEME) or '<' == getToken(TOKENLEXEME):
        comparisonOp()
        simpleExp()

def comparisonOp():
    match(getToken(TOKENLEXEME),TOKENLEXEME)

def simpleExp():
    term()
    while getToken(TOKENLEXEME) == '+' or getToken(TOKENLEXEME) == '-':
        addOp() 
        term()

def addOp():
    match(getToken(TOKENLEXEME),TOKENLEXEME)

def term():
    factor()
    while getToken(TOKENLEXEME) == '/' or getToken(TOKENLEXEME) == '*':
        mulOp()
        factor()

def mulOp():
    match(getToken(TOKENLEXEME),TOKENLEXEME)

def factor():
    if '(' == getToken(TOKENLEXEME):
        match('(',TOKENLEXEME)
        exp()
        match(')',TOKENLEXEME)
    elif getToken(TOKENCLASS) == NUMBER:
        match(getToken(TOKENCLASS), TOKENCLASS)
    elif getToken(TOKENCLASS) == IDENTIFIER:
        match(getToken(TOKENCLASS), TOKENCLASS)
    else:
        match(False,TOKENCLASS)    


program()


        
                
        