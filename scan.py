#   CSE 226 Design of Compilers - CHEP ASU
#   Author: Ahmed Abdelaziz
#   Project title: Scanner for TINY language complier
#   Project Description:

#       The role of the scanner is to perform lexical analysis
#       which splits program source code into substrings called tokens 
#       and classify each token to their role (token class).

#       This scanner accepts input as a txt file & named "inputfile.txt"  
#       & generates output as an array of dictionarys where each dict is 
#       labeled token in this format:
#           {class: SyntaxKind.ConstKeyword, lexeme: ‘const’}


from fysom import Fysom

# TINY scanner DFA presented as FSM 
DFA = Fysom(initial='START',
            events=[('init', 'DONE', 'START'),
                    ('whiteSpace',  'START',  '='),
                    ('rb', 'START', 'INCOMMENT'),
                    ('lb',  'INCOMMENT', 'START'),
                    ('colon', 'START', 'ASSIGN'),
                    ('eq', 'INASSIGN', 'DONE'),
                    ('digit', 'INNUM', '='),
                    ('digit', 'START', 'INNUM'),                    
                    ('letter', 'START', 'INID'),
                    ('letter', 'INID', '='),
                    ('other', 'INCOMMENT', '='),
                    ('other', 'INASSIGN', 'DONE'),
                    ('other', 'INNUM', 'DONE'),
                    ('other', 'INID', 'DONE'),
                    ('other', 'START', 'DONE')])

# function to control state transition for the scanner DFA
def DFAstate (token):
    for char in token:
        if DFA.current == 'DONE':
            DFA.init()
        if char == ' ':
                DFA.whiteSpace() if DFA.current == 'START' else DFA.other()
        elif type(char) is int:
            DFA.digit() if DFA.current == 'START' or DFA.current == 'INNUM' else DFA.other()
        elif type(char) is str:
            DFA.letter() if DFA.current == 'START' or DFA.current == 'INID' else DFA.other()
        elif char == '{':
            DFA.rb() if DFA.current == 'START' else DFA.other()
        elif char == '}':
            DFA.lb() if DFA.current == 'START' else DFA.other()
        elif char == ':':
            DFA.colon() if DFA.current == 'START' else DFA.other()
        elif char == '=':
            DFA.rb() if DFA.current == 'INASSIGN' else DFA.other()
        else:
            DFA.other()
        stateLog.append(DFA.current) 


#list of TINY language token classes
identifiers = [['+', '-', '*', '/', '=', '<', '(', ')', ';', ':='],
               ['if', 'then', 'else', 'end', 'repeat', 'until', 'read', 'write']]

#function to label & store special symbols in TokenList
def isSpecialSymbol(lexeme):
    tokenList.append({"class" : "Special Symbol", "lexeme" : lexeme})

#function to label & store reserved words in TokenList
def isReservedWord(lexeme):
    tokenList.append({"class" : "Reserved Word", "lexeme" : lexeme})

#function to label & store numbers in TokenList
def isNum(lexeme):
    tokenList.append({"class" : "Number", "lexeme" : lexeme})

#function to label & store identifiers in TokenList
def isIdentifier(lexeme):
    tokenList.append({"class" : "Identifier", "lexeme" : lexeme})

#function to check whether the lexeme is number or identifier
def other(lexeme):
    try:
        val = int(lexeme)
        isNum(lexeme)
    except ValueError:
        isIdentifier(lexeme)

# Print token list
def printToken():
    for t in range(len(tokenList)):
        print("Lexeme : '" + tokenList[t].get("lexeme","none") + "' , Class : '"+ tokenList[t].get("class","none")+"'")                         


comment = False

#function to identify each lexeme, label it & store it labeled in TokenList
def identify(inputLines):
    global comment
    for lexeme in inputLines:
        if comment is True and not('}' in lexeme) :
            continue
        if lexeme in identifiers[0]:
            isSpecialSymbol(lexeme)       
        elif lexeme in identifiers[1]:
            isReservedWord(lexeme)
        elif lexeme == '{':
            comment = True  
        elif '}' in lexeme :
                comment = False 
        #case where lexeme contains multiple tokens with no whitespaces in between
        else:
            temp = []
            for x in identifiers[0]:
                if x in lexeme:
                   temp = lexeme.split(x)
                   temp.insert(1,x)                         
            if len(temp) != 0:
                identify(temp)
            elif '{' in lexeme:
                temp = lexeme.split('{')    
                temp.insert(1, '{')
                identify(temp)
            elif '}' in lexeme:
                temp = lexeme.split('}')
                temp.insert(1, '}')
                identify(temp)   
            elif lexeme != '' and lexeme != ' ':                              
                other(lexeme)

#tokens array to be filled with each lexeme after being identified 
tokenList = []
#read input file
file = open('tiny_sample_code (1).txt', 'r')
sourceCode = file.read()
#split tokens from input file, remove spaces
inputSplitted = sourceCode.split()
#DFA State transition
stateLog = []
DFAstate(sourceCode)
#identify each token in the list & append it to TokenList
identify(inputSplitted)
#print token list
printToken()
with open('scanner_output.txt', 'w') as f:
    for item in tokenList:
        f.write("%s\n" % item)    

