def generate_graphviz_dfs(node, graph=None, node_id=0, parent_id=None):
    """
    Преобразует структуру Node в код Graphviz (DOT формат) в стиле DFS.

    :param node: Корневой узел типа Node.
    :param graph: Список строк с описанием узлов и связей (накопитель).
    :param node_id: Текущий идентификатор узла.
    :param parent_id: Идентификатор родительского узла (для соединений).
    :return: Готовый код Graphviz в формате строки.
    """
    if graph is None:
        graph = []

    current_id = f"node{node_id}"
    graph.append(f'{current_id} [label="{node.label}", shape=box];')

    if parent_id is not None:
        graph.append(f'{parent_id} -> {current_id};')

    # Обработка детей узла (DFS)
    last_child_id = current_id
    loop_start_id = None  # Сохраним начальный узел цикла для возврата
    for child in node.children:
        node_id += 1
        child_id = f"node{node_id}"

        # Если узел цикл, фиксируем его начальный ID
        if child.type in {"while", "for"}:
            loop_start_id = child_id

        graph.append(f'{last_child_id} -> {child_id};')  # Связываем текущий с ребенком
        node_id = generate_graphviz_dfs(child, graph, node_id, last_child_id)
        last_child_id = child_id

    # Если узел цикл, добавляем возврат на начало цикла
    if node.type in {"while", "for"} and loop_start_id:
        graph.append(f'{last_child_id} -> {current_id} [label="loop end", style=dotted];')

    return node_id if parent_id else "digraph G {\n" + "\n".join(graph) + "\n}"
