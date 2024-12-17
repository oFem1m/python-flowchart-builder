from parser import CodeTreeBuilder


def main():
    # Парсинг кода
    with open("test_files/test_file2.py", "r") as file:
        code = file.read()
    builder = CodeTreeBuilder()

    tree = builder.build_tree(code)
    print("полное дерево: ", tree)


if __name__ == "__main__":
    main()
