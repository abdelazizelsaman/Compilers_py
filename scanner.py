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



#tokens array to be filled with each lexeme after being identified 
__tokenList = []
#list of TINY language token classes
__identifiers = [['+', '-', '*', '/', '=', '<', '(', ')', ';', ':='],
               ['if', 'then', 'else', 'end', 'repeat', 'until', 'read', 'write']]

#function to label & store special symbols in TokenList
def __isSpecialSymbol(lexeme):
    __tokenList.append({"class" : "Special Symbol", "lexeme" : lexeme})

#function to label & store reserved words in TokenList
def __isReservedWord(lexeme):
    __tokenList.append({"class" : "Reserved Word", "lexeme" : lexeme})

#function to label & store numbers in TokenList
def __isNum(lexeme):
    __tokenList.append({"class" : "number", "lexeme" : lexeme})

#function to label & store identifiers in TokenList
def __isIdentifier(lexeme):
    __tokenList.append({"class" : "identifier", "lexeme" : lexeme})

#function to check whether the lexeme is number or identifier
def __other(lexeme):
    try:
        val = int(lexeme)
        __isNum(lexeme)
    except ValueError:
        __isIdentifier(lexeme)

#function to identify each lexeme, label it & store it labeled in TokenList
def __identify(inputSplitted):
    comment = False
    for lexeme in inputSplitted:
        if comment is True and not('}' in lexeme) :
            continue
        if lexeme in __identifiers[0]:
            __isSpecialSymbol(lexeme)       
        elif lexeme in __identifiers[1]:
            __isReservedWord(lexeme)
        elif lexeme == '{':
            comment = True  
        elif '}' in lexeme :
                comment = False 
        #case where lexeme contains multiple tokens with no whitespaces in between
        else:
            temp = []
            for x in __identifiers[0]:
                if x in lexeme:
                   temp = lexeme.split(x)
                   temp.insert(1,x)                         
            if len(temp) != 0:
                __identify(temp)
            elif '{' in lexeme:
                temp = lexeme.split('{')    
                temp.insert(1, '{')
                __identify(temp)
            elif '}' in lexeme:
                temp = lexeme.split('}')
                temp.insert(1, '}')
                __identify(temp)   
            elif lexeme != '' and lexeme != ' ':                              
                __other(lexeme)

def tokenize(sourceCode):
    #split tokens from input file, remove spaces
    inputSplitted = sourceCode.split()
    __identify(inputSplitted)
    return __tokenList

    