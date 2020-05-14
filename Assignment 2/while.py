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
equal = "="
define = ":="
no = "¬"
lp = "("
rp = ")"
more = ">"
less = "<"
he = "∧"
huo = "∨"
signs = [add, minus, multi, equal, define, no, lp, rp, more, less, he, huo]
compare_sign = [more, less, equal]

def build(text):
    divString(text)
    for line in lines:
        split(line)


def split(text):
    global parseTree
    if "?" in text:
        parseTree = ternary(text)
    elif text[0] == "if":
        parseTree = ifthen(text)
    elif text[0] == "while":
        parseTree = whiledo(text)
    elif text[0] == "skip":
        pass
    else:
        parse(text)
    parse_tree(parseTree)


def parse(text):
    global outVars
    if text[0] == "(" and text[len(text)-1] == ")":
        text = text[1:len(text) - 1]
    if text[0] == no:
        return not parse(text[1:])
    if len(text) == 1 and not is_int(text[0]):
        if text[0] == "true":
            return True
        else:
            return False
    if len(text) == 1 and is_int(text[0]):
        return read_val(text[0])

    if "∨" in text:
        return parse(text[:text.index("∨")]) or parse(text[text.index("∨")+1:])
    if "∧" in text:
        return parse(text[:text.index("∧")]) and parse(text[text.index("∧")+1:])

    if "(" in text:
        newText = []
        if "(" != text[0]:
            for i in range(0, text.index("(")):
                newText.append(text[i])
        prText = text[text.index("(")+1:text.index(")")]
        newText.append(parse(prText))
        for i in range(text.index(")") + 1, len(text)):
            newText.append(text[i])
        return parse(newText)

    if len(text) == 3 and (text[1] == add or text[1] == minus or text[1] == multi):
        if text[1] == add:
            return read_val(text[0]) + read_val(text[2])
        elif text[1] == minus:
            return read_val(text[0]) - read_val(text[2])
        elif text[1] == multi:
            return read_val(text[0]) * read_val(text[2])

    if text[1] == ":=":
        return nameVar(text)

    if len(text) == 3:
        return compare(text[0], text[2], text[1])

    if check_same(text, compare_sign)[0]:
        dex = check_same(text, compare_sign)[1]
        left = text[:dex]
        right = text[dex + 1:]
        return compare_more(left, right, text[dex])

    return True


def check_same(list1, list2):
    for i in range(len(list1)):
        for j in range(len(list2)):
            if list1[i] == list2[j]:
                return True, i
    return False


def ifthen(text):
    arrif = text[text.index("if")+1:text.index("then")]
    arrthen = text[text.index("then")+1:text.index("else")]
    arrelse = text[text.index("else")+1:]
    ast = Node(key=arrif, tp="ifthenP")
    ast.left = Node(key=arrthen, tp="ifthenL")
    if arrelse[0] == "while":
        ast.right = whiledo(arrelse)
    else:
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
    else:
        ast.right = Node(key=arrdo, tp="whiledoR")
    return ast


def ternary(text):
    arrif = text[:text.index("?")]
    arrthen = text[text.index("?")+1:text.index(":")]
    arrelse = text[text.index(":")+1:]
    ast = Node(key=arrif, tp="ifthenP")
    ast.left = Node(key=arrthen, tp="ifthenL")
    ast.right = Node(key=arrelse, tp="ifthenR")
    return ast


def parse_tree(curr):
    global outVars
    if curr.tp == "ifthenP":
        curr.tf = parse(curr.key)
        if curr.tf:
            if curr.left.tp == "whiledoP":
                parse_tree(curr.left)
            else:
                parse(curr.left.key)
        else:
            if curr.right.tp == "whiledoP":
                parse_tree(curr.right)
            else:
                parse(curr.right.key)
    if curr.tp == "whiledoP":
        curr.left.tf = parse(curr.left.key)
        while curr.left.tf:
            before = outVars
            # print("before: ", before)
            if curr.right.tp == "ifthenP":
                parse_tree(curr.right)
                curr.left.tf = parse(curr.left.key)
            else:
                parse(curr.right.key)
                curr.left.tf = parse(curr.left.key)
            after = outVars
            # print("after: ", after)
            if before == after:
                break


def listToString(ls):
    string = ""
    for a in ls:
        string += (str(a))
    return string


def nameVar(text):
    global outVars
    var = text[:text.index(":=")][0]
    val = text[text.index(":=")+1:]
    for i in range(0, len(val)):
        val[i] = read_val(val[i])
    val = eval(listToString(val))
    check_exist(var, val)
    return True


def divString(text):
    if "{" in text:
        bText = text[text.index("{"):text.index("}")]
        if ";" in bText:
            text[text.index("{")+bText.index(";")] = "∧"

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
    global outVars
    if len(outVars) > 1:
        if outVars[1][0] == "fact":
            sub = outVars[0]
            outVars[0] = outVars[1]
            outVars[1] = sub
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
    global outVars, signs
    if is_int(var):
        return int(var)
    elif var in signs:
        return var
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


def compare_more(a, b, sign):
    for i in range(0, len(a)):
        a[i] = read_val(a[i])
    val_a = eval(listToString(a))
    for i in range(0, len(b)):
        b[i] = read_val(b[i])
    val_b = eval(listToString(b))

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
    res = printAnw()
    res = "{" + res + "}"
    print(res)


if __name__ == '__main__':
    main()