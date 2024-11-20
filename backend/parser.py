import ast

class Node:
    def __init__(self, type, label, children=None):
        self.type = type
        self.label = label
        self.children = children if children else []

    def __repr__(self):
        return f"Node(type='{self.type}', label='{self.label}', children={self.children})"

def parse_python_code(code):
    tree = ast.parse(code)
    root_node = Node(type="root", label="root")
    process_node(tree, root_node)
    return root_node

def process_node(tree, parent_node):
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            label = f"def {node.name}({', '.join(arg.arg for arg in node.args.args)}):"
            function_node = Node(type="function", label=label)
            parent_node.children.append(function_node)
            process_node(node, function_node)

        elif isinstance(node, ast.If):
            condition = ast.unparse(node.test)
            if_node = Node(type="if", label=f"if {condition}:")
            parent_node.children.append(if_node)
            process_node_list(node.body, if_node)
            if node.orelse:
                else_node = Node(type="else", label="else:")
                parent_node.children.append(else_node)
                process_node_list(node.orelse, else_node)

        elif isinstance(node, ast.For):
            target = ast.unparse(node.target)
            iter_ = ast.unparse(node.iter)
            for_node = Node(type="for", label=f"for {target} in {iter_}:")
            parent_node.children.append(for_node)
            process_node_list(node.body, for_node)

        elif isinstance(node, ast.While):
            condition = ast.unparse(node.test)
            while_node = Node(type="while", label=f"while {condition}:")
            parent_node.children.append(while_node)
            process_node_list(node.body, while_node)

        elif isinstance(node, ast.Break):
            break_node = Node(type="break", label="break")
            parent_node.children.append(break_node)

        elif isinstance(node, ast.Continue):
            continue_node = Node(type="continue", label="continue")
            parent_node.children.append(continue_node)

        elif isinstance(node, ast.Assign):
            targets = ", ".join(ast.unparse(t) for t in node.targets)
            value = ast.unparse(node.value)
            assign_node = Node(type="assign", label=f"{targets} = {value}")
            parent_node.children.append(assign_node)

        elif isinstance(node, ast.AugAssign):
            target = ast.unparse(node.target)
            op = ast.unparse(node.op)
            value = ast.unparse(node.value)
            assign_node = Node(type="assign", label=f"{target} {op}= {value}")
            parent_node.children.append(assign_node)

        elif isinstance(node, ast.Return):
            value = ast.unparse(node.value) if node.value else "None"
            return_node = Node(type="return", label=f"return {value}")
            parent_node.children.append(return_node)

        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = ast.unparse(node.value)
            call_node = Node(type="call", label=call)
            parent_node.children.append(call_node)

        elif isinstance(node, ast.Expr):
            expr = ast.unparse(node.value)
            expr_node = Node(type="expr", label=expr)
            parent_node.children.append(expr_node)

def process_node_list(nodes, parent_node):
    for node in nodes:
        process_node(node, parent_node)
