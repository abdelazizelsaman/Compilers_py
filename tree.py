from ete3 import Tree, TreeStyle, TextFace
import parser as p
file = open('state_log.txt', 'r')
log = file.read().split()
ST = Tree()
index = 0
NODE = Tree()

def getState():
    return log[index]

def nodeName():
    NODE.add_face(TextFace(getState()), column=0, position = "branch-right")   

def indexSafe():
    return True if index < len(log) else False

def inc():
    global index
    if indexSafe():
        index += 1

def dec():
    global index
    if indexSafe():
        index -= 1        

def buildTree():
    global NODE
    if index == 0:
        NODE = ST.add_child(name=getState())
        NODE.add_face(TextFace(getState()), column=0, position = "branch-right")
        inc()
    elif getState() in ["read-stmt", "write-stmt"]:
        NODE = ST.add_child(name=getState())
        nodeName()
        inc()
        NODE.add_child(name=getState())
        nodeName()
        inc()  
    elif getState() == "if-stmt":
        NODE = ST.add_child(name=getState())
        NODE.add_face(TextFace(getState()), column=0, position = "branch-right")
        inc()
        inc()
        N = NODE.add_child(name=getState())
        N.add_face(TextFace(getState()), column=0, position = "branch-right")
        dec()
        NN = N.add_child(name=getState())
        inc()
        inc()
        NNN = NN.add_sister(name=getState())
        NNN.add_face(TextFace(getState()), column=0, position = "branch-right")
        inc()
    elif getState() == 'then':
        inc()
    elif getState() == 'assign-stmt':
        if log[index+2] in ['mulop', 'addop']:
            N = NODE.add_child(name=getState())
            N.add_face(TextFace(getState()), column=0, position = "branch-top")
            inc()
            inc()
            NN = N.add_child(name=getState())
            NN.add_face(TextFace(getState()), column=0, position = "branch-top")
            dec()
            NN.add_child(name=getState())
            inc()
            inc()
            NN.add_child(name=getState())
            inc()
        else:
            N = NODE.add_child(name=getState())
            N.add_face(TextFace(getState()), column=0, position = "branch-top")
            N.add_face(TextFace('identifier'), column=0, position = "branch-right")
            inc()
            inc()
            N = N.add_child(name=getState())
            inc()
    elif getState() == 'repeat-stmt':
        NODE = NODE.add_child(name=getState())
        inc()
    elif getState() == 'until':
        inc()
        inc()
        N = NODE.add_child(name=getState())
        N.add_face(TextFace('='), column=0, position = "branch-right")
        dec()
        N.add_child(name=getState())
        inc()
        inc()
        N.add_child(name=getState())
        inc()
    elif getState() == 'end':
        inc()

        




        
        
        





while index < len(log):
    buildTree()
    print(ST)

ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_length = True
ts.show_branch_support = True
ts.show_border = True
ST.show(tree_style=ts)








