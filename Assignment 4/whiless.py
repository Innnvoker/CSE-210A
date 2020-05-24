#!/usr/bin/env python3
import numpy as np
import copy
import sys

class Node:
    def __init__(self, key=None, tf=True, tp=None):
        self.left = None
        self.right = None
        self.key = key
        self.tf = tf
        self.tp = tp

    def printNode(self):
        print(" key: ", self.key, " tf: ", self.tf, " type: ", self.tp)

count = 0
flag = 0
outVars = [[],[]]
lines = []
whileArr = []
outLines = ""
preState = ""
postState = ""
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
    global lines, count, preState, postState, flag, outLines
    divString(text)
    for i in range(len(lines)):
        if lines[i-1] and len(lines) > 1:
            if no_if_while(lines[i]):
                postState = build_define(lines[i:])
            else:
                if is_define(lines[i-1]):
                    postState = build_if(lines[i])

                    print_after()

        split(lines[i])
    add_state(0)
    add_state(1)
    if flag != 1:
        print("⇒ " + outLines)
    outLines = ''


def split(text):
    global parseTree, postState, preState, count, outLines, flag
    flag = 0
    if "?" in text:
        parseTree = ternary(text)
    elif text[0] == "if":
        parseTree = ifthen(text)
    elif text[0] == "while":
        preState = build_while(text)[1]
        postState = build_while(text)[0]
        parseTree = whiledo(text)
    elif text[0] == "skip":
        flag = 1
        pass
    else:
        if count > 0:
            print_after()

        parse(text)
        count += 1


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
    global outVars, outLines, preState, postState
    if curr.tp == "ifthenP":
        curr.tf = parse(curr.key)
        if curr.tf:
            if curr.left.tp == "whiledoP":
                parse_tree(curr.left)
            else:
                str = listToString(curr.left.key)
                outLines += restore(str)
                add_state(1)
                print("⇒ " + outLines)
                outLines = ''
                end()

                parse(curr.left.key)


        else:
            if curr.right.tp == "whiledoP":
                parse_tree(curr.right)
            else:
                str = listToString(curr.right.key)
                outLines += restore(str)
                add_state(1)
                print("⇒ " + outLines)
                outLines = ''
                end()

                parse(curr.right.key)

    if curr.tp == "whiledoP":
        curr.left.tf = parse(curr.left.key)
        while curr.left.tf:

            outLines += preState + "; " + postState
            add_state(1)
            print("⇒ " + outLines)
            outLines = ''
            end()

            before = copy.deepcopy(outVars)
            if curr.right.tp == "ifthenP":
                parse_tree(curr.right)
                curr.left.tf = parse(curr.left.key)
            else:
                parse(curr.right.key)
                curr.left.tf = parse(curr.left.key)
            after = copy.deepcopy(outVars)
            if before == after:
                break

            print_after()


def listToString(ls):
    string = ""
    for a in ls:
        if a == None:
            string += " "
        else:
            string += (str(a))
    return string


def nameVar(text):
    # print(text)
    global outVars
    var = text[:text.index(":=")][0]
    val = text[text.index(":=")+1:]
    for i in range(0, len(val)):
        val[i] = read_val(val[i])
    val = eval(listToString(val))
    check_exist(var, val)
    return True


def divString(text):
    txt = []
    if text[0] == "{":
        txt += text[text.index("{") + 1:text.index("}")]
        if text.index("}") != len(text)-1:
            txt += text[text.index("}")+1:]
        text = txt

    if "{" in text and "while" not in text:
        if text.index("{") != 0:
            txt += text[:text.index("{")]
        txt += text[text.index("{") + 1:text.index("}")]
        if text.index("}") != len(text)-1:
            txt += text[text.index("}")+1:]
        text = txt

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


def printVar():
    global outVars
    vars = list(map(list, zip(*sorted(zip(*outVars)))))
    output = ""
    if vars:
        for i in range(len(vars[0])):
            output += vars[0][i] + " → " + str(vars[1][i]) + ", "
    output = output[:-2]
    return "{" + output + "}"


def printLines():
    pass


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def check_exist(var, val):
    global outVars
    if len(outVars[0]) == 0 or var not in outVars[0]:
        outVars[0].append(var)
        outVars[1].append(val)
    else:
        id = outVars[0].index(var)
        outVars[1][id] = val


def read_val(var):
    global outVars, signs
    if is_int(var):
        return int(var)
    elif var in signs:
        return var
    else:
        if len(outVars[0]) == 0 or var not in outVars[0]:
            return 0
        else:
            id = outVars[0].index(var)
            val = outVars[1][id]
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


def restore(str):
    if len(str) == 4:
        return str[0] + " := " + str[3]
    else:
        return str[0] + " := (" + str[3:] + ")"


def add_state(num):
    global outLines
    # 0 means skip
    if num == 0:
        outLines += "skip"
    # 1 means var declare
    elif num == 1:
        if len(outLines) > 0:
            outLines += ", " + printVar()


def build_state(num):
    pass


def build_if(text):
    arrif = text[text.index("if")+1:text.index("then")]
    arrthen = text[text.index("then")+1:text.index("else")]
    arrelse = text[text.index("else")+1:]
    if len(arrif) == 1 or no in arrif:
        pass
    else:
        dex = 0
        if "<" in arrif:
            dex = arrif.index("<")
        if ">" in arrif:
            dex = arrif.index(">")
        if "=" in arrif:
            dex = arrif.index("=")

        if len(arrif) > dex + 3:
            arrif.insert(dex+1, lp)
            arrif.insert(len(arrif), rp)

        if arrif[0] != "(":
            arrif.insert(0, lp)
            arrif.insert(len(arrif), rp)

    if arrthen[0] != "{":
        arrthen.insert(0, "{")
        arrthen.insert(len(arrthen), "}")
    dex = arrthen.index(":=")
    arrthen.insert(dex, None)
    arrthen.insert(dex+2, None)
    if arrthen.index("}") - arrthen.index(":=") > 3:
        arrthen.insert(arrthen.index(":=")+2, lp)
        arrthen.insert(arrthen.index("}"), rp)
    arrthen.insert(arrthen.index("{")+1, None)
    arrthen.insert(arrthen.index("}"), None)

    if arrelse[0] != "{":
        arrelse.insert(0, "{")
        arrelse.insert(len(arrelse), "}")
    dex = arrelse.index(":=")
    arrelse.insert(dex, None)
    arrelse.insert(dex+2, None)
    if arrelse.index("}") - arrelse.index(":=") > 3:
        arrelse.insert(arrelse.index(":=")+2, lp)
        arrelse.insert(arrelse.index("}"), rp)
    arrelse.insert(arrelse.index("{")+1, None)
    arrelse.insert(arrelse.index("}"), None)

    if_state = "if " + listToString(arrif) + " then " + listToString(arrthen) + " else " + listToString(arrelse)
    return if_state


def build_while(text):
    arrwhile = text[text.index("while") + 1:text.index("do")]
    arrdo = text[text.index("do") + 1:]
    if len(arrwhile) == 1 or no in arrwhile:
        pass
    else:
        dex = 0
        if "<" in arrwhile:
            dex = arrwhile.index("<")
        if ">" in arrwhile:
            dex = arrwhile.index(">")
        if "=" in arrwhile:
            dex = arrwhile.index("=")

        if len(arrwhile) > dex + 3:
            arrwhile.insert(dex+1, lp)
            arrwhile.insert(len(arrwhile), rp)

        if arrwhile[0] != "(":
            arrwhile.insert(0, lp)
            arrwhile.insert(len(arrwhile), rp)

    if arrdo[0] != "{":
        arrdo.insert(0, "{")
        arrdo.insert(len(arrdo), "}")
    dex = arrdo.index(":=")
    arrdo.insert(dex, None)
    arrdo.insert(dex+2, None)
    if arrdo.index("}") - arrdo.index(":=") > 3:
        arrdo.insert(arrdo.index(":=")+2, lp)
        arrdo.insert(arrdo.index("}"), rp)
    arrdo.insert(arrdo.index("{")+1, None)
    arrdo.insert(arrdo.index("}"), None)
    while_state = "while " + listToString(arrwhile) + " do " + listToString(arrdo)
    do_state = listToString(arrdo)
    do_state = do_state[2:len(do_state)-2]
    return while_state, do_state


def build_define(ls):
    output = []
    for ele in ls:
        if no_if_while(ele):
            output.append(ele[0])
            output.append(None)
            output.append(ele[1])
            output.append(None)
            output.append(ele[2])
            output.append(";")
            output.append(None)
        if "while" in ele:
            output.append(build_while(ele)[0])
    return listToString(output)[:-2]


def no_if_while(ls):
    if "if" in ls:
        return False
    if "while" in ls:
        return False
    return True


def is_define(ls):
    if ls[1] == ":=":
        return True
    return False


def end():
    global count
    count += 1
    if count == 10000:
        sys.exit()


def print_after():
    global outLines
    add_state(0)
    outLines += "; " + postState
    add_state(1)
    print("⇒ " + outLines)
    outLines = ''
    end()

    outLines += postState
    add_state(1)
    print("⇒ " + outLines)
    outLines = ''
    end()


def main():
    text = input().split()
    build(text)



if __name__ == '__main__':
    main()