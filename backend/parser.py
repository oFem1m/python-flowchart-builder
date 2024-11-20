import ast


class Node:
    def __init__(self, type, label, children=None):
        self.type = type
        self.label = label
        self.children = children if children else []

    def __repr__(self):
        return f"Node(type={self.type!r}, label={self.label!r}, children={self.children})"


class CodeTreeBuilder(ast.NodeVisitor):
    def build_tree(self, code):
        # Парсинг кода в AST
        tree = ast.parse(code)
        return self.visit(tree)

    def visit(self, node):
        """Обработка узла AST."""
        if isinstance(node, ast.Module):
            return Node(type="root", label="root", children=[self.visit(stmt) for stmt in node.body])
        elif isinstance(node, ast.FunctionDef):
            return Node(
                type="function",
                label=f"def {node.name}({', '.join(arg.arg for arg in node.args.args)}):",
                children=[self.visit(stmt) for stmt in node.body],
            )
        elif isinstance(node, ast.If):
            children = [Node(type="if", label=f"if {self.visit(node.test)}:",
                             children=[self.visit(stmt) for stmt in node.body])]
            if node.orelse:
                children.append(Node(type="else", label="else:", children=[self.visit(stmt) for stmt in node.orelse]))
            return Node(type="branch", label="if-else", children=children)
        elif isinstance(node, ast.For):
            return Node(
                type="for",
                label=f"for {node.target.id} in {self.visit(node.iter)}:",
                children=[self.visit(stmt) for stmt in node.body],
            )
        elif isinstance(node, ast.While):
            return Node(
                type="while",
                label=f"while {self.visit(node.test)}:",
                children=[self.visit(stmt) for stmt in node.body],
            )
        elif isinstance(node, ast.Expr):
            return self.visit(node.value)
        elif isinstance(node, ast.Call):
            func_name = self.visit(node.func)
            args = ", ".join(self.visit(arg) for arg in node.args)
            return Node(type="call", label=f"{func_name}({args})", children=[])
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.Return):
            return Node(type="return", label=f"return {self.visit(node.value)}", children=[])
        elif isinstance(node, ast.Assign):
            targets = ", ".join(self.visit(t) for t in node.targets)
            value = self.visit(node.value)
            return Node(type="assign", label=f"{targets} = {value}", children=[])
        else:
            return f"<unknown {type(node).__name__}>"


def tree_to_graphviz(node, graph=None, parent_id=None, node_id=0):
    """
    Преобразует дерево Node в формат для graphviz.
    """
    from graphviz import Digraph

    if graph is None:
        graph = Digraph()

    # Добавляем текущий узел
    current_id = node_id
    if isinstance(node, Node):
        graph.node(str(current_id), label=f"{node.type}: {node.label}")
    else:
        # Если узел — это строка, добавляем его как терминальный узел
        graph.node(str(current_id), label=str(node))

    if parent_id is not None:
        graph.edge(str(parent_id), str(current_id))

    # Добавляем детей, если это Node
    next_id = current_id  # Отслеживаем id узлов
    if isinstance(node, Node):  # Только для объектов Node
        for child in node.children:
            next_id += 1
            next_id = tree_to_graphviz(child, graph, current_id, next_id)  # Передаем обновленный next_id

    print(graph)
    return next_id


