import tkinter as tk

class FlowchartLayout:
    def __init__(self, tree):
        self.tree = tree.children[0]  # Дерево кода
        self.layers = []  # Слои блоков
        self.positions = {}  # Координаты каждого узла

    def create_layers(self, node, depth=0):
        """Разбивает дерево на слои."""
        if len(self.layers) <= depth:
            self.layers.append([])
        self.layers[depth].append(node)

        for child in node.children:
            self.create_layers(child, depth + 1)

    def calculate_positions(self, layer_height=150, block_width=150, block_spacing=50):
        """Вычисляет позиции блоков."""
        y = 50  # Начальная координата по вертикали
        for depth, layer in enumerate(self.layers):
            x = 50  # Начальная координата по горизонтали
            for node in layer:
                self.positions[node] = (x, y)
                x += block_width + block_spacing
            y += layer_height

    def get_connections(self):
        """Генерирует линии переходов между узлами."""
        connections = []
        for parent in self.positions:
            for child in parent.children:
                connections.append((self.positions[parent], self.positions[child]))
        return connections

    def layout(self):
        """Основной метод для расчета расположения узлов."""
        self.create_layers(self.tree)
        self.calculate_positions()

    def render(self, canvas):
        """Рисует блок-схему на холсте."""
        for node, (x, y) in self.positions.items():
            self.draw_block(canvas, node, x, y)

        for start, end in self.get_connections():
            self.draw_line(canvas, start, end)

    def draw_block(self, canvas, node, x, y):
        """Рисует блоки в зависимости от типа узла."""
        block_width, block_height = 150, 50
        if node.type == "function" or node.type == "return":
            canvas.create_oval(
                x, y, x + block_width, y + block_height, fill="lightblue"
            )
        elif node.type in {"if", "while"}:
            canvas.create_polygon(
                x + block_width // 2,
                y,
                x,
                y + block_height // 2,
                x + block_width // 2,
                y + block_height,
                x + block_width,
                y + block_height // 2,
                fill="lightyellow",
            )
        elif node.type == "for":
            canvas.create_polygon(
                x + 20,
                y,
                x + block_width - 20,
                y,
                x + block_width,
                y + block_height // 2,
                x + block_width - 20,
                y + block_height,
                x + 20,
                y + block_height,
                x,
                y + block_height // 2,
                fill="lightgreen",
            )
        else:
            canvas.create_rectangle(
                x, y, x + block_width, y + block_height, fill="lightgray"
            )
        canvas.create_text(x + block_width // 2, y + block_height // 2, text=node.label)

    def draw_line(self, canvas, start, end):
        """Рисует линии переходов между блоками."""
        x1, y1 = start
        x2, y2 = end
        canvas.create_line(x1 + 75, y1 + 50, x2 + 75, y2, arrow=tk.LAST)
