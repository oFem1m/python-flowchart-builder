from parser import CodeTreeBuilder
from graphviz import generate_graphviz_dfs

def main():
    # Пример кода для анализа
    with open("test_file.py", "r") as file:
        code = file.read()

    # Создание дерева кода
    builder = CodeTreeBuilder()
    tree = builder.build_tree(code)

    # Вывод дерева
    print("Дерево программы:")
    print(tree)
    print("Код для graphviz")
    print(generate_graphviz_dfs(tree))



if __name__ == "__main__":
    main()
