def main():
    text = input().split()
    ast = build(text)
    result = str(calculate(ast))
    print("{ ", result, " }")


if __name__ == '__main__':
    main()

vars = []
outVars = []
lines = []
add = "+"
minus = "-"
multi = "*"
equal = ":="
he = "∧"
huo = "∨"
no = "¬"
equalout = "→"


def calculate(ast):
    for var in outVars:


def build(text):
    divString(text)
    for line in lines:
        parse(line)


def parse(text):
    if text[0] == "if":
        ifthen(text)
    elif text[0] == "while":
        whiledo(text)
    elif text[0] == "skip":
        pass
    else:
        nameVar(text)


def ifthen(text):
    arrif = text[text.index("if")+1:text.index("then")]
    arrthen = text[text.index("then")+1:text.index("else")]
    arrelse = text[text.index("else")+1:]
    return arrif, arrthen, arrelse


def whiledo(text):
    arrwhile = text[text.index("while")+1:text.index("do")]
    arrdo = text[text.index("do")+1:]
    return arrwhile, arrdo


class Node :
    def __init__(self, key, num=0, tf=True):
        self.left = None
        self.right = None
        self.num = num
        self.key = key
        self.tf = tf

    def printNode(self):
        print("num: ", num, " key: ", key, " tf: ", tf)


def clear():
    vars.clear()
    lines.clear()


def nameVar(text):
    var = text[:text.index("=")][0]
    val = text[text.index("=")+1:][0]
    vars.append([var, int(val)])


def divString(text):
    count = text.count(";")
    if count > 0:
        count = count + 1
    while count > 0:
        if ";" in text:
            subText = text[:text.index(";")]
            text = text[text.index(";")+1:]
        else:
            subText = text
        lines.append(subText)
        count = count - 1