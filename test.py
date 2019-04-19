import scanner
file = open('tiny_sample_code.txt', 'r')
tokens = scanner.tokenize(file.read())

for t in range(len(tokens)):
        print("Lexeme : '" + tokens[t].get("lexeme","none") + "' , Class : '"+ tokens[t].get("class","none")+"'")                         
