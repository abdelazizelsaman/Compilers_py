import scanner as s
import parser as p
import tree as t 

file = open('tiny_sample_code.txt', 'r')
tokenList = s.tokenize(file.read())
#p.parse(tokenList)
file = open('state_log.txt', 'r')
log = file.read().split()
t.draw(log)