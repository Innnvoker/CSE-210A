import numpy as np

class Node:
    def __init__(self, key=None, tf=True, tp=None):
        self.left = None
        self.right = None
        self.key = key
        self.tf = tf
        self.tp = tp

    def printNode(self):
        print(" key: ", self.key, " tf: ", self.tf, " type: ", self.tp)

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

    # if len(text) == 3 and "<" in text and is_int(text[0]) and is_int(text[2]):
    #     return int(text[0]) < int(text[2])
    # if len(text) == 3 and ">" in text and is_int(text[0]) and is_int(text[2]):
    #     return int(text[0]) > int(text[2])
    # if len(text) == 3 and "=" in text and is_int(text[0]) and is_int(text[2]):
    #     return int(text[0]) == int(text[2])

    if len(text) == 3:
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

    if "{" and "}" in arrdo:
        arrdo = arrdo[1:len(arrdo) - 1]
        if arrdo[0] == "if":
            ast.right = ifthen(arrdo)
    else:
        ast.right = Node(key=arrdo, tp="whiledoR")
    return ast


def parse_tree(curr):
    global outVars
    if curr.tp == "ifthenP":
        curr.tf = parse(curr.key)
        # print(curr.tf)
        if curr.tf:
            parse(curr.left.key)
        else:
            parse(curr.right.key)
    if curr.tp == "whiledoP":
        curr.left.tf = parse(curr.left.key)
        while curr.left.tf:
            before = outVars
            print("before: ", before)
            if curr.right.tp == "ifthenP":
                parse_tree(curr.right)
                curr.left.tf = parse(curr.left.key)
            else:
                curr.left.tf = parse(curr.right.key)
            after = outVars
            print("after: ", after)
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
        val = read_val(val)
    elif len(val) == 3:
        val_a = read_val(val[0])
        val_b = read_val(val[2])
        if val[1] == add:
            val = val_a + val_b
        elif val[1] == minus:
            val = val_a - val_b
        elif val[1] == multi:
            val = val_a * val_b
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


def read_val(var):
    global outVars
    if is_int(var):
        return int(var)
    else:
        outVars = np.transpose(np.asarray(outVars))
        if len(outVars) == 0 or var not in outVars[0]:
            outVars = np.transpose(outVars)
            outVars = outVars.tolist()
            return 0
        else:
            id = np.where(outVars[0] == var)
            val = outVars[1][id]
            outVars = np.transpose(outVars)
            outVars = outVars.tolist()
            return int(val)


def compare(a, b, sign):
    if is_int(a):
        val_a = int(a)
        val_b = read_val(b)
    elif is_int(b):
        val_a = read_val(a)
        val_b = int(b)
    else:
        val_a = read_val(a)
        val_b = read_val(b)

    if sign == "=":
        return val_a == val_b
    elif sign == "<":
        return val_a < val_b
    elif sign == ">":
        return val_a > val_b

    return False


def print_tree(curr):
    if curr:
        print_tree(curr.left)
        curr.printNode()
        print_tree(curr.right)


def main():
    text = input().split()
    build(text)
    parse_tree(parseTree)
    print_tree(parseTree)
    res = printAnw()
    print("{" + res + "}")

if __name__ == '__main__':
    main()
