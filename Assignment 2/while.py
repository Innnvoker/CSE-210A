import numpy as np

class Node:
    def __init__(self, key = None, num=0, tf=True, tp=None):
        self.left = None
        self.right = None
        self.num = num
        self.key = key
        self.tf = tf
        self.tp = tp

    def printNode(self):
        print("num: ", num, " key: ", key, " tf: ", tf, " type: ", tp)

vars = []
outVars = []
lines = []
whileArr = []
parseTree = Node()
add = "+"
minus = "-"
multi = "*"
equal = ":="
he = "∧"
huo = "∨"
no = "¬"


def build(text):
    divString(text)
    for line in lines:
        split(line)


def split(text):
    global parseTree
    if text[0] == "if":
        parseTree = ifthen(text)
    elif text[0] == "while":
        parseTree = whiledo(text)
    elif text[0] == "skip":
        pass
    else:
        nameVar(text)


# def parseSub(text):
#     if text[0] == "if":
#         ifthen(text)
#     elif text[0] == "while":
#         whiledo(text)

def parse(text):
    global outVars
    if text[0] == "(" and text[len(text)-1] == ")":
        text = text[1:len(text) - 1]
    if text[0] == no:
        return not parse(text[1:])
    if len(text) == 1:
        if text[0] == "true":
            return True
        else:
            return False
    if len(text) == 3 and text[1] == ":=":
        nameVar(text)
    if len(text) == 3 and text[1] == "=":
        var = text[:text.index("=")][0]
        val = text[text.index("=") + 1:][0]
        outVars = np.transpose(np.asarray(outVars))
        if var not in outVars[0]:
            outVars = np.transpose(outVars)
            outVars = outVars.tolist()
            return val == 0
        else:
            id = np.where(outVars[0] == var)
            val_stored = outVars[1][id]
            outVars = np.transpose(outVars)
            outVars = outVars.tolist()
            return val == val_stored
    return True
    # if he in text or huo in text:



def ifthen(text):
    arrif = text[text.index("if")+1:text.index("then")]
    arrthen = text[text.index("then")+1:text.index("else")]
    arrelse = text[text.index("else")+1:]
    # print(arrif)
    # print(arrthen)
    # print(arrelse)
    ast = Node(key=arrif, tp="ifthenP")
    ast.left = Node(key=arrthen, tp="ifthenL")
    ast.right = Node(key=arrelse, tp="ifthenR")
    return ast


def whiledo(text):
    arrwhile = text[text.index("while")+1:text.index("do")]
    arrdo = text[text.index("do")+1:]
    ast = Node(tp="whiledoP")
    ast.left = Node(key=arrwhile, tp="whiledoL")
    ast.right = Node(key=arrdo, tp="whiledoR")
    return ast


def parse_tree(curr):
    if curr.tp == "ifthenP":
        parse(curr.key)
        if curr.tf:
            parse(curr.left.key)
        else:
            parse(curr.right.key)
    if curr.tp == "whiledoP":
        parse(curr.left.key)
        while curr.left.tf:
            parse(curr.right.key)




def clear():
    vars.clear()
    lines.clear()


def nameVar(text):
    global outVars
    var = text[:text.index(":=")][0]
    val = text[text.index(":=")+1:][0]
    # print("var:", var)
    # print("val:", val)
    outVars = np.transpose(np.asarray(outVars))
    # print("outVars:", outVars)
    if len(outVars) == 0 or var not in outVars[0]:
        outVars = np.transpose(outVars)
        outVars = outVars.tolist()
        outVars.append([var, int(val)])
    else:
        id = np.where(outVars[0] == var)
        outVars[1][id] = val
        outVars = np.transpose(outVars)
        outVars = outVars.tolist()


def divString(text):
    count = text.count(";")
    if count == 0:
        lines.append(text)
    else:
        count = count + 1
        while count > 0:
            if ";" in text:
                subText = text[:text.index(";")]
                text = text[text.index(";")+1:]
            else:
                subText = text
            lines.append(subText)
            count = count - 1



def printAnw():
    output = ""
    if outVars:
        for var in outVars:
            output += var[0] + " → " + str(var[1]) + ", "
    output = output[:-2]
    return output

def main():
    text = input().split()
    build(text)
    parse_tree(parseTree)
    res = printAnw()
    print("{" + res + "}")

if __name__ == '__main__':
    main()
