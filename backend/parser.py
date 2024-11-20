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
            function_node = Node(type="function", label=node.name)
            parent_node.children.append(function_node)
            process_node(node, function_node)

        elif isinstance(node, ast.If):
            if_node = Node(type="if", label="if")
            parent_node.children.append(if_node)
            process_node_list(node.body, if_node)
            if node.orelse:
                else_node = Node(type="else", label="else")
                parent_node.children.append(else_node)
                process_node_list(node.orelse, else_node)

        elif isinstance(node, ast.For):
            for_node = Node(type="for", label="for")
            parent_node.children.append(for_node)
            process_node_list(node.body, for_node)

        elif isinstance(node, ast.While):
            while_node = Node(type="while", label="while")
            parent_node.children.append(while_node)
            process_node_list(node.body, while_node)

        elif isinstance(node, ast.Break):
            break_node = Node(type="break", label="break")
            parent_node.children.append(break_node)

        elif isinstance(node, ast.Continue):
            continue_node = Node(type="continue", label="continue")
            parent_node.children.append(continue_node)

        elif isinstance(node, ast.Assign):
            assign_node = Node(type="assign", label="assignment")
            parent_node.children.append(assign_node)

        elif isinstance(node, ast.AugAssign):
            assign_node = Node(type="assign", label="augmented assignment")
            parent_node.children.append(assign_node)

        elif isinstance(node, ast.Return):
            return_node = Node(type="return", label="return")
            parent_node.children.append(return_node)

        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call_node = Node(type="call", label="function call")
            parent_node.children.append(call_node)

        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            output_node = Node(type="output", label="output")
            parent_node.children.append(output_node)

        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Name):
            var_node = Node(type="variable", label="variable")
            parent_node.children.append(var_node)

def process_node_list(nodes, parent_node):
    for node in nodes:
        process_node(node, parent_node)
