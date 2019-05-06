from ete3 import Tree, TreeStyle, TextFace

log = []
index = 0
ST = Tree()
NODE = Tree()
flagr = False
flagif = False
ifNode = Tree()
repeatNode = Tree()

def checkNode():
    global repeatNode
    global NODE
    if not flagr:
        NODE = repeatNode

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
    global flagif
    global flagr
    global repeatNode
    global ifNode
    if index == 0:
        NODE = ST.add_child(name=getState())
        NODE.add_face(TextFace(getState()), column=0, position = "branch-right")
        inc()
    elif getState() in ["read-stmt", "write-stmt"]:
        checkNode()
        NODE = NODE.add_child(name=getState())
        nodeName()
        inc()
        NODE.add_child(name=getState())
        nodeName()
        inc()  
    elif getState() == "if-stmt":
        flag = True
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
        NN.add_sister(name=getState())
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
        flagr = True
        repeatNode = NODE
        NODE = NODE.add_child(name=getState())
        NODE.add_face(TextFace(getState()), column=0, position = "branch-right")
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
        flagr = False

    elif getState() == 'end':
        inc()

def draw(syntaxlist):
    global log
    log = syntaxlist
    while index < len(log):
        buildTree()

    ts = TreeStyle()
    ts.show_leaf_name = True
    ts.show_branch_length = True
    ts.show_branch_support = True
    ts.show_border = True
    ST.show(tree_style=ts)
    ST.render("syntax tree.png", w=183, units="mm")




        
        
        













