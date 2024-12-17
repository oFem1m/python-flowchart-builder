class Block:
    def __init__(self, block_id: int, block_type: str, label: str):
        """
        Initialize a block.
        """
        self.id = block_id
        self.type = block_type
        self.label = label
        self.connections = []  # List of connected block IDs

    def add_connection(self, block_id: int):
        """
        Add a connection to another block.

        :param block_id: ID of the block to connect to.
        """
        if block_id not in self.connections:
            self.connections.append(block_id)

    def __repr__(self):
        """
        String representation for debugging.
        """
        return (f"Block(id={self.id}, type='{self.type}', label='{self.label}', "
                f"connections={self.connections})")


def parse_node(node, blocks, current_id):
    """
    Recursively parse the Node tree and build Blocks.

    :param node: Current Node.
    :param blocks: List of Blocks.
    :param current_id: Current block ID.
    :return: (entry_block_id, exit_block_ids, current_id)
    """
    if node.type == 'root':
        # Process children
        entry_block_id = None
        exit_block_ids = []
        for child in node.children:
            child_entry_id, child_exit_ids, current_id = parse_node(child, blocks, current_id)
            if entry_block_id is None:
                entry_block_id = child_entry_id
            else:
                # Connect previous exits to new entry
                for exit_id in exit_block_ids:
                    blocks[exit_id - 1].add_connection(child_entry_id)
            exit_block_ids = child_exit_ids
        return entry_block_id, exit_block_ids, current_id

    elif node.type == 'function':
        # Create a new block for the function definition
        block = Block(current_id, node.type, node.label)
        blocks.append(block)
        entry_block_id = current_id
        current_id += 1

        # Process the body of the function
        last_exit_ids = [entry_block_id]
        for child in node.children:
            child_entry_id, child_exit_ids, current_id = parse_node(child, blocks, current_id)
            # Connect previous exits to the current child
            for exit_id in last_exit_ids:
                blocks[exit_id - 1].add_connection(child_entry_id)
            last_exit_ids = child_exit_ids
        return entry_block_id, last_exit_ids, current_id

    elif node.type == 'branch' and node.label == 'if-else':
        # Handle 'if-else' branches
        if_node = None
        else_node = None
        for child in node.children:
            if child.type == 'if':
                if_node = child
            elif child.type == 'else':
                else_node = child

        block = Block(current_id, 'if', if_node.label)
        blocks.append(block)
        entry_block_id = current_id
        current_id += 1

        # Process true branch
        true_entry_id, true_exit_ids, current_id = parse_node(if_node, blocks, current_id)
        # Process false branch
        if else_node:
            false_entry_id, false_exit_ids, current_id = parse_node(else_node, blocks, current_id)
        else:
            false_entry_id = None
            false_exit_ids = [entry_block_id]

        # Add connections from 'if' block to true and false branches
        blocks[entry_block_id - 1].add_connection(true_entry_id)
        if false_entry_id:
            blocks[entry_block_id - 1].add_connection(false_entry_id)

        # Merge exits from both branches
        last_exit_ids = true_exit_ids + false_exit_ids
        return entry_block_id, last_exit_ids, current_id

    elif node.type == 'if':
        # Process the body of the 'if' (true branch)
        last_exit_ids = []
        entry_block_id = None
        for idx, child in enumerate(node.children):
            child_entry_id, child_exit_ids, current_id = parse_node(child, blocks, current_id)
            if entry_block_id is None:
                entry_block_id = child_entry_id
            else:
                # Connect previous exits to the current child
                for exit_id in last_exit_ids:
                    blocks[exit_id - 1].add_connection(child_entry_id)
            last_exit_ids = child_exit_ids
        if not last_exit_ids:
            last_exit_ids = [entry_block_id]
        return entry_block_id, last_exit_ids, current_id

    elif node.type == 'else':
        # Process the body of the 'else' (false branch)
        last_exit_ids = []
        entry_block_id = None
        for idx, child in enumerate(node.children):
            child_entry_id, child_exit_ids, current_id = parse_node(child, blocks, current_id)
            if entry_block_id is None:
                entry_block_id = child_entry_id
            else:
                # Connect previous exits to the current child
                for exit_id in last_exit_ids:
                    blocks[exit_id - 1].add_connection(child_entry_id)
            last_exit_ids = child_exit_ids
        if not last_exit_ids:
            last_exit_ids = [entry_block_id]
        return entry_block_id, last_exit_ids, current_id

    elif node.type in ['while', 'for']:
        # Create a block for the loop condition
        block = Block(current_id, node.type, node.label)
        blocks.append(block)
        entry_block_id = current_id
        current_id += 1

        # Process loop body
        if node.children:
            body_entry_id, body_exit_ids, current_id = parse_node(node.children[0], blocks, current_id)
            # Add connection from loop condition to body
            blocks[entry_block_id - 1].add_connection(body_entry_id)
            # Add connection from body exit back to loop condition
            for exit_id in body_exit_ids:
                blocks[exit_id - 1].add_connection(entry_block_id)

        # The loop can exit after the condition check
        exit_block_ids = [entry_block_id]
        return entry_block_id, exit_block_ids, current_id

    elif node.type == 'return':
        # Create a block for the return statement
        block = Block(current_id, node.type, node.label)
        blocks.append(block)
        entry_block_id = current_id
        current_id += 1
        # Return statements do not have exits
        exit_block_ids = []
        return entry_block_id, exit_block_ids, current_id

    else:
        # Create a block for the node
        block = Block(current_id, node.type, node.label)
        blocks.append(block)
        entry_block_id = current_id
        current_id += 1

        # Process any children sequentially
        last_exit_ids = [entry_block_id]
        for child in node.children:
            child_entry_id, child_exit_ids, current_id = parse_node(child, blocks, current_id)
            # Connect previous exits to the current child
            for exit_id in last_exit_ids:
                blocks[exit_id - 1].add_connection(child_entry_id)
            last_exit_ids = child_exit_ids
        return entry_block_id, last_exit_ids, current_id


def build_blocks(node):
    """
    Build the list of Blocks from the Node tree.

    :param node: Root Node.
    :return: List of Blocks.
    """
    blocks = []
    current_id = 1
    parse_node(node, blocks, current_id)
    return blocks
