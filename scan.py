#   CSE 226 Design of Compilers - CHEP ASU
#   Author: Ahmed Abdelaziz
#   Project title: Scanner for TINY language complier
#   Project Description:

#       The role of the scanner is to perform lexical analysis
#       which splits program source code into substrings called tokens 
#       and classify each token to their role (token class).

#       This scanner accepts input as a txt file & named "inputfile.txt"  
#   `   & generates output as an array of dictionarys where each dict is 
#       labeled token in this format:
#           {class: SyntaxKind.ConstKeyword, lexeme: ‘const’}


#list of TINY language token classes
identifiers = [['+', '-', '*', '/', '=', '<', '(', ')', ';', ':'],
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

#function to identify each lexeme, label it & store it labeled in TokenList
def identify(inputLines):
    for lexeme in inputLines:
        if lexeme in identifiers[0]:
            isSpecialSymbol(lexeme)
        elif ':' in lexeme:
            isSpecialSymbol(lexeme)        
        elif lexeme in identifiers[1]:
            isReservedWord(lexeme)
        elif ';' in lexeme:
            if lexeme.replace(';','') in identifiers[1]:
                isReservedWord(lexeme.replace(';',''))
            else:
                other(lexeme.replace(';',''))
            isSpecialSymbol(';')    
        else:
            other(lexeme)
    for t in range(len(tokenList)):
        print("Lexeme : '" + tokenList[t].get("lexeme","none") + "' , Class : '"+ tokenList[t].get("class","none")+"'")         

#tokens array to be filled with each lexeme after being identified 
tokenList = []
#read input file
file = open('inputfile.txt', 'r')
#split tokens from input file
inputSplitted = file.read().split()
#identify each token in the list & append it to TokenList
identify(inputSplitted)

