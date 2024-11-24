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
        """Парсинг строки с кодом и построение дерева."""
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

        elif isinstance(node, ast.While):
            return Node(
                type="while",
                label=f"while {self.visit(node.test)}:",
                children=[self.visit(stmt) for stmt in node.body],
            )

        elif isinstance(node, ast.For):
            return Node(
                type="for",
                label=f"for {self.visit(node.target)} in {self.visit(node.iter).label}:",
                children=[self.visit(stmt) for stmt in node.body],
            )

        elif isinstance(node, ast.Return):
            return Node(type="return", label=f"return {self.visit(node.value)}", children=[])

        elif isinstance(node, ast.Assign):
            targets = ", ".join(self.visit(t) for t in node.targets)
            value = self.visit(node.value)
            return Node(type="assign", label=f"{targets} = {value}", children=[])

        elif isinstance(node, ast.AugAssign):
            target = self.visit(node.target)
            op = self.get_operator(node.op)
            value = self.visit(node.value)
            return Node(type="aug_assign", label=f"{target} {op}= {value}", children=[])

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

        elif isinstance(node, ast.BinOp):
            left = self.visit(node.left)
            op = self.get_operator(node.op)
            right = self.visit(node.right)
            return f"({left} {op} {right})"

        elif isinstance(node, ast.Compare):
            left = self.visit(node.left)
            ops = [self.get_operator(op) for op in node.ops]
            comparators = [self.visit(comp) for comp in node.comparators]
            return f"{left} {' '.join(ops)} {' '.join(comparators)}"

        elif isinstance(node, ast.BoolOp):
            values = [self.visit(v) for v in node.values]
            op = self.get_operator(node.op)
            return f" {op} ".join(values)

        else:
            return f"<unknown {type(node).__name__}>"

    def visit_list(self, nodes):
        """Обработка списка узлов."""
        return [self.visit(node) for node in nodes]

    def get_operator(self, op):
        """Возвращает строковое представление оператора."""
        return {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/",
            ast.Mod: "%",
            ast.Pow: "**",
            ast.Lt: "<",
            ast.Gt: ">",
            ast.LtE: "<=",
            ast.GtE: ">=",
            ast.Eq: "==",
            ast.NotEq: "!=",
            ast.And: "and",
            ast.Or: "or",
        }.get(type(op), "<unknown op>")
