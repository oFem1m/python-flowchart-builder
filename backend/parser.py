import ast


class Node:
    def __init__(self, type, label, children=None):
        self.type = type
        self.label = label
        self.children = children if children else []

    def __repr__(self):
        return f" {{\"type\": \"{self.type}\", \"label\": \"{self.label}\", \"children\": {str(self.children).replace('[', '[').replace(']', ']')}\n}}"


class CodeTreeBuilder(ast.NodeVisitor):
    def build_tree(self, code):
        """Парсинг строки с кодом и построение дерева."""
        tree = ast.parse(code)
        return self.visit(tree)

    def visit(self, node):
        """Обработка узла AST."""
        if isinstance(node, ast.Module):
            return self.visit(node.body[0])

        elif isinstance(node, ast.FunctionDef):
            return Node(
                type="function",
                label=f"def {node.name}({', '.join(arg.arg for arg in node.args.args)}):",
                children=[self.visit(stmt) for stmt in node.body],
            )

        elif isinstance(node, ast.If):
            children = [Node(type="if", label="if", children=[self.visit(stmt) for stmt in node.body])]
            if node.orelse:
                children.append(Node(type="else", label="else:", children=[self.visit(stmt) for stmt in node.orelse]))
            else:
                children.append(Node(type="null_else", label="else:", children=[]))
            return Node(type="branch", label=f"if {self.visit(node.test).label}:", children=children)

        elif isinstance(node, ast.While):
            children = [Node(type="while", label="while", children=[self.visit(stmt) for stmt in node.body])]
            if node.orelse:
                children.append(Node(type="else-loop", label="else:", children=[self.visit(stmt) for stmt in node.orelse]))
            else:
                children.append(Node(type="else-loop", label="else:", children=[Node(type="null", label="null", children=[])]))
            return Node(type="loop", label=f"while {self.visit(node.test).label}:", children=children)

        elif isinstance(node, ast.For):
            children = [Node(type="for", label="for", children=[self.visit(stmt) for stmt in node.body])]
            if node.orelse:
                children.append(Node(type="else-loop", label="else:", children=[self.visit(stmt) for stmt in node.orelse]))
            else:
                children.append(Node(type="else-loop", label="else:", children=[Node(type="null", label="null", children=[])]))
            return Node(type="loop", label=f"for {self.visit(node.target).label} in {self.visit(node.iter).label}:", children=children)

        elif isinstance(node, ast.Break):
            return Node(type="break", label="break", children=[])

        elif isinstance(node, ast.Continue):
            return Node(type="continue", label="continue", children=[])

        elif isinstance(node, ast.Return):
            if node.value is None:
                label = "return"
            elif isinstance(node.value, ast.Tuple):
                elements = ", ".join(self.visit(elt).label for elt in node.value.elts)
                label = f"return {elements}"
            else:
                label = f"return {self.visit(node.value).label}"
            return Node(type="return", label=label, children=[])

        elif isinstance(node, ast.Assign):
            targets = ", ".join(self.visit(t).label for t in node.targets)
            value = self.visit(node.value).label
            return Node(type="assign", label=f"{targets} = {value}", children=[])

        elif isinstance(node, ast.AugAssign):
            target = self.visit(node.target).label
            op = self.get_operator(node.op)
            value = self.visit(node.value).label
            return Node(type="aug_assign", label=f"{target} {op}= {value}", children=[])

        elif isinstance(node, ast.Expr):
            return self.visit(node.value)

        elif isinstance(node, ast.Call):
            func_name = self.visit(node.func).label
            args = ", ".join(self.visit(arg).label for arg in node.args)
            return Node(type="call", label=f"{func_name}({args})", children=[])

        elif isinstance(node, ast.Attribute):
            value = self.visit(node.value).label
            return Node(type="attribute", label=f"{value}.{node.attr}", children=[])

        elif isinstance(node, ast.Name):
            return Node(type="name", label=node.id, children=[])

        elif isinstance(node, ast.Constant):
            return Node(type="constant", label=repr(node.value), children=[])

        elif isinstance(node, ast.List):
            elements = [self.visit(e).label for e in node.elts]
            return Node(type="list", label=f"[{', '.join(elements)}]", children=[])

        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                operand = self.visit(node.operand)
                if isinstance(node.operand, ast.Constant) and isinstance(node.operand.value, (int, float)):
                    return Node(type="constant", label=repr(-node.operand.value), children=[])
                return Node(type="unaryop", label=f"-{operand.label}", children=[])
            return Node(type="unaryop", label=f"<{type(node.op).__name__}>", children=[])

        elif isinstance(node, ast.BinOp):
            left = self.visit(node.left).label
            op = self.get_operator(node.op)
            right = self.visit(node.right).label
            return Node(type="binop", label=f"({left} {op} {right})", children=[])

        elif isinstance(node, ast.Compare):
            left = self.visit(node.left).label
            ops = [self.get_operator(op) for op in node.ops]
            comparators = [self.visit(comp).label for comp in node.comparators]
            return Node(type="compare", label=f"{left} {' '.join(ops)} {' '.join(comparators)}", children=[])

        elif isinstance(node, ast.BoolOp):
            values = [self.visit(v).label for v in node.values]
            op = self.get_operator(node.op)
            return Node(type="boolop", label=f" {op} ".join(values), children=[])

        else:
            return Node(type="unknown", label=f"<{type(node).__name__}>", children=[])

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
