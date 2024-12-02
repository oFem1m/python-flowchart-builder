# flowchart.py

import tkinter as tk
from typing import List, Dict
from block_parser import Block

class FlowchartDrawer:
    def __init__(self, blocks: List[Block]):
        self.blocks = blocks
        self.block_dict = {block.id: block for block in blocks}
        self.positions = {}  # block_id: (x, y)
        self.block_width = 150
        self.block_height = 60
        self.horizontal_spacing = 200
        self.vertical_spacing = 100

    def assign_positions(self):
        """
        Assigns x and y positions to each block based on its layer.
        Blocks in the same layer are placed horizontally with spacing.
        """
        layers: Dict[int, List[Block]] = {}
        for block in self.blocks:
            layers.setdefault(block.layer, []).append(block)

        sorted_layers = sorted(layers.keys())
        y_start = 50

        for layer in sorted_layers:
            blocks_in_layer = layers[layer]
            num_blocks = len(blocks_in_layer)
            # Calculate total width needed
            total_width = num_blocks * self.block_width + (num_blocks - 1) * self.horizontal_spacing
            # Starting x position
            x_start = (1920 - total_width) / 2 if num_blocks > 1 else 960
            for idx, block in enumerate(blocks_in_layer):
                x = x_start + idx * (self.block_width + self.horizontal_spacing)
                y = y_start + (layer - 1) * (self.block_height + self.vertical_spacing)
                self.positions[block.id] = (x, y)

    def draw_flowchart(self, canvas: tk.Canvas):
        """
        Draws all blocks and their connections on the canvas.
        """
        # First, assign positions to all blocks
        self.assign_positions()

        # Draw connections first to ensure arrows are beneath blocks
        for block in self.blocks:
            for conn_id in block.connections:
                if conn_id in self.positions:
                    self.draw_arrow(canvas, block, self.block_dict[conn_id])

        # Draw all blocks
        for block in self.blocks:
            self.draw_block(canvas, block)

    def draw_block(self, canvas: tk.Canvas, block: Block):
        """
        Draws a single block on the canvas based on its type.

        :param canvas: Tkinter Canvas object.
        :param block: Block to draw.
        """
        x, y = self.positions[block.id]
        w = self.block_width
        h = self.block_height

        # Define block shapes based on type
        if block.type in ['function', 'return']:
            # Oval-like shape (two arcs and a rectangle)
            radius = h / 2
            canvas.create_arc(x - w/2, y, x - w/2 + radius*2, y + h,
                             start=90, extent=180, fill='white', outline='black')
            canvas.create_arc(x + w/2 - radius*2, y, x + w/2, y + h,
                             start=-90, extent=180, fill='white', outline='black')
            canvas.create_rectangle(x - w/2 + radius, y, x + w/2 - radius, y + h,
                                    fill='white', outline='black')
        elif block.type == 'if':
            # Diamond shape
            points = [
                x, y,
                x - w/2, y + h/2,
                x, y + h,
                x + w/2, y + h/2
            ]
            canvas.create_polygon(points, fill='white', outline='black')
        elif block.type in ['while']:
            # Diamond shape similar to 'if'
            points = [
                x, y,
                x - w/2, y + h/2,
                x, y + h,
                x + w/2, y + h/2
            ]
            canvas.create_polygon(points, fill='white', outline='black')
        elif block.type == 'for':
            # Hexagon shape
            points = [
                x - w/4, y,
                x - w/2, y + h/2,
                x - w/4, y + h,
                x + w/4, y + h,
                x + w/2, y + h/2,
                x + w/4, y
            ]
            canvas.create_polygon(points, fill='white', outline='black')
        elif block.type in ['assign', 'aug_assign']:
            # Rectangle shape
            canvas.create_rectangle(x - w/2, y, x + w/2, y + h,
                                    fill='white', outline='black')
        elif block.type == 'call':
            # Procedure block (rectangle with doubled sides)
            canvas.create_rectangle(x - w/2, y, x + w/2, y + h,
                                    fill='white', outline='black')
            # Draw doubled sides
            canvas.create_line(x - w/2 + 10, y, x - w/2 + 10, y + h, fill='black')
            canvas.create_line(x + w/2 - 10, y, x + w/2 - 10, y + h, fill='black')
        else:
            # Default to rectangle
            canvas.create_rectangle(x - w/2, y, x + w/2, y + h,
                                    fill='white', outline='black')

        # Draw the label text inside the block
        canvas.create_text(x, y + h/2, text=block.label, width=w - 20)

    def draw_arrow(self, canvas: tk.Canvas, from_block: Block, to_block: Block):
        """
        Draws an arrow from one block to another with appropriate color and direction.

        :param canvas: Tkinter Canvas object.
        :param from_block: Source Block.
        :param to_block: Destination Block.
        """
        from_x, from_y = self.positions[from_block.id]
        to_x, to_y = self.positions[to_block.id]
        w = self.block_width
        h = self.block_height

        # Determine the connection points based on block types
        # For simplicity, arrows will start from the right center of from_block
        # and point to the left center of to_block

        if from_block.type in ['if', 'while']:
            # Green arrow for true branch, red for false branch
            if to_block.id in from_block.connections[:1]:
                color = 'green'  # Assuming the first connection is true
            else:
                color = 'red'    # Otherwise, false
        else:
            color = 'black'

        # Calculate start and end points
        start_x = from_x + self.block_width / 2
        start_y = from_y + self.block_height / 2
        end_x = to_x - self.block_width / 2
        end_y = to_y + self.block_height / 2

        # Draw the arrow
        canvas.create_line(start_x, start_y, end_x, end_y,
                           arrow=tk.LAST, fill=color, width=2)

def draw_flowchart(blocks: List[Block]):
    """
    Initializes the Tkinter window and draws the flowchart.

    :param blocks: List of Block objects.
    """
    root = tk.Tk()
    root.title("Flowchart")
    canvas_width = 1920
    canvas_height = 1080
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack()

    drawer = FlowchartDrawer(blocks)
    drawer.draw_flowchart(canvas)

    root.mainloop()
