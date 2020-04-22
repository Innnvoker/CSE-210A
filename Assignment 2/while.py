def main():
    text = input()
    ast = parser(text)
    result = str(eval(ast.build_ast()))
    print(result)

if __name__ == '__main__':
    main()