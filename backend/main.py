from parser import parse_python_code
from graphviz import Digraph

def main():
    with open("test_file.py", "r") as file:
        code = file.read()
    parsed_structure = parse_python_code(code)
    print(parsed_structure)


def draw_flowchart(root_node, output_file="flowchart"):
    dot = Digraph(comment="Python Code Flowchart")

    def add_nodes_edges(node, parent_id=None):
        node_id = str(id(node))
        dot.node(node_id, f"{node.type}\n{node.label}")

        if parent_id:
            dot.edge(parent_id, node_id)

        for child in node.children:
            add_nodes_edges(child, node_id)

    add_nodes_edges(root_node)
    dot.format = "png"
    dot.render(output_file)
    print(f"Flowchart generated and saved as {output_file}.png")

if __name__ == "__main__":
    main()
