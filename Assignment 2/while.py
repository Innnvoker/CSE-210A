import numpy as np

class Node:
    def __init__(self, key=None, num=0, tf=True, tp=None):
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
    if text[1] == ":=":
        nameVar(text)

    if "∨" in text:
        return parse(text[:text.index("∨")]) or parse(text[text.index("∨")+1:])
    if "∧" in text:
        return parse(text[:text.index("∧")]) and parse(text[text.index("∧")+1:])

    if len(text) == 3 and "<" in text and is_int(text[0]) and is_int(text[2]):
        return int(text[0]) < int(text[2])
    if len(text) == 3 and ">" in text and is_int(text[0]) and is_int(text[2]):
        return int(text[0]) > int(text[2])
    if len(text) == 3 and "=" in text and is_int(text[0]) and is_int(text[2]):
        return int(text[0]) == int(text[2])

    if len(text) == 3 and ("<" or ">") in text:
        return compare(text[0], text[2], text[1])


    if text[1] == "=":
        var = text[:text.index("=")][0]
        val = text[text.index("=") + 1:]
        if len(val) == 1:
            val = val[0]
        if len(val) == 3 and is_int(val[0]) and is_int(val[2]):
            if val[1] == add:
                val = int(val[0]) + int(val[2])
            elif val[1] == minus:
                val = int(val[0]) - int(val[2])
            elif val[1] == multi:
                val = int(val[0]) * int(val[2])

        return compare(var, val, "=")
    return True


def ifthen(text):
    arrif = text[text.index("if")+1:text.index("then")]
    arrthen = text[text.index("then")+1:text.index("else")]
    arrelse = text[text.index("else")+1:]
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
    global outVars
    if curr.tp == "ifthenP":
        curr.tf = parse(curr.key)
        if curr.tf:
            parse(curr.left.key)
        else:
            parse(curr.right.key)
    if curr.tp == "whiledoP":
        curr.left.tf = parse(curr.left.key)
        while curr.left.tf:
            before = outVars
            curr.left.tf = parse(curr.right.key)
            after = outVars
            if before == after:
                break


def clear():
    vars.clear()
    lines.clear()


def nameVar(text):
    global outVars
    var = text[:text.index(":=")][0]
    val = text[text.index(":=")+1:]
    if len(val) == 1:
        val = val[0]
    if len(val) == 3:
        if val[1] == add:
            val = int(val[0]) + int(val[2])
        elif val[1] == minus:
            val = int(val[0]) - int(val[2])
        elif val[1] == multi:
            val = int(val[0]) * int(val[2])
    check_exist(var, val)



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


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def check_exist(var, val):
    global outVars
    outVars = np.transpose(np.asarray(outVars))
    if len(outVars) == 0 or var not in outVars[0]:
        outVars = np.transpose(outVars)
        outVars = outVars.tolist()
        outVars.append([var, val])
    else:
        id = np.where(outVars[0] == var)
        outVars[1][id] = val
        outVars = np.transpose(outVars)
        outVars = outVars.tolist()


def compare(a, b, sign):
    global outVars
    outVars = np.transpose(np.asarray(outVars))

    if is_int(a):
        var = b
    else:
        var = a

    if len(outVars) == 0 or var not in outVars[0]:
        outVars = np.transpose(outVars)
        outVars = outVars.tolist()
        if is_int(a):
            if sign == "<":
                return int(a) < 0
            elif sign == ">":
                return int(a) > 0
            elif sign == "=":
                return 0 == int(a)
        else:
            if sign == "<":
                return 0 < int(b)
            elif sign == ">":
                return 0 > int(b)
            elif sign == "=":
                return 0 == int(b)
    else:
        id = np.where(outVars[0] == var)
        val = outVars[1][id][0]
        outVars = np.transpose(outVars)
        outVars = outVars.tolist()
        if is_int(a):
            if sign == "<":
                return int(a) < int(val)
            elif sign == ">":
                return int(a) > int(val)
            elif sign == "=":
                return int(val) == int(a)
        else:
            if sign == "<":
                return int(val) < int(b)
            elif sign == ">":
                return int(val) > int(b)
            elif sign == "=":
                return int(val) == int(b)
    return False


def main():
    text = input().split()
    build(text)
    parse_tree(parseTree)
    res = printAnw()
    print("{" + res + "}")

if __name__ == '__main__':
    main()
