from ete3 import Tree
t = Tree(name="TT") # Creates an empty tree
A = t.add_child(name="A") # Adds a new child to the current tree root
                           # and returns it
B = t.add_child(name="B") # Adds a second child to the current tree
                           # root and returns it
C = A.add_child(name="C") # Adds a new child to one of the branches
D = C.add_sister(name="D") # Adds a second child to same branch as
                             # before, but using a sister as the starting
                             # point
R = A.add_child(name="R") # Adds a third child to the
                           # branch. Multifurcations are supported

t.show()

file = open('state_log.txt', 'r')
log = file.read().split()
ST = Tree()
index = 0

def indexSafe():
    return True if index < len(log) else False

def inc():
    global index
    if indexSafe():
        index += 1

def addNode(node):
    global index
    if indexSafe():
        if not t.name:
            ST.add_child(name = log[index])
            inc()
        else:
            if log[index] == 'read-stmt':
                node2 = node.add_child(name = log[index])
                inc()
                addNode(node2)
            elif log[index] == 'if-stmt':
                node3 = node.add_child(name = log[index])
                node4 = node3.add_child(name = log[index+2])
                node4.add_child(name =log[index+1])
                node3.add_child(name = log[index+3])
                inc()
                inc()
                inc()
                inc()
                addNode(node3)
            elif log[index] == 'assign-stmt':
                node4 = node.add_child(name = log[index])
                inc()
                node4.add_child(name = log[index])
                inc()
                addNode(node4)

        
        




