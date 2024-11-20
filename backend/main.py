from parser import CodeTreeBuilder, tree_to_graphviz

def main():
    # Пример кода для анализа
    code = """
def sample_function(x):
    if x > 0:
        for i in range(x):
            print(i)
    else:
        while x < 5:
            x += 1
    return x
    """

    # Создание дерева кода
    builder = CodeTreeBuilder()
    tree = builder.build_tree(code)

    # Вывод дерева
    print("Дерево программы:")
    print(tree)

    # Преобразование в граф для Graphviz
    graph = tree_to_graphviz(tree)
    print(graph)
    # graph.render("code_tree", format="png", cleanup=True)
    print("Граф сохранен в 'code_tree.png'.")


if __name__ == "__main__":
    main()
