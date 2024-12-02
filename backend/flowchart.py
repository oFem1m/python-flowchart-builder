import tkinter as tk


def draw_line(canvas, start, end):
    """Рисует линии переходов между блоками."""
    x1, y1 = start
    x2, y2 = end
    canvas.create_line(x1 + 75, y1 + 50, x2 + 75, y2, arrow=tk.LAST)


def draw_block(canvas, node, x, y):
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


class FlowchartLayout:
    def __init__(self, tree):
        self.tree = tree.children[0]  # Начинаем с первого узла после root (предполагается, что это функция)
        self.positions = {}  # Координаты каждого узла
        self.connections = []  # Список соединений между блоками
        self.visited = set()  # Для отслеживания узлов в DFS
        self.grid = {}  # Используем сетку для размещения узлов: (x, y) -> узел
        self.current_x = 10  # Горизонтальное смещение
        self.current_y = 10  # Вертикальное смещение
        self.level_width = 200  # Ширина уровня между узлами
        self.vertical_spacing = 100  # Вертикальное расстояние между уровнями

    def calculate_positions(self, node, parent=None, x=0, y=0):
        """Рекурсивный DFS для вычисления позиций узлов."""
        # if node in self.visited:
        #     return
        # self.visited.add(node)

        # Устанавливаем позицию текущего узла, избегая коллизий
        while (x, y) in self.grid:
            x += self.level_width

        self.positions[node] = (x, y)
        self.grid[(x, y)] = node

        # Если есть родитель, добавляем соединение
        if parent:
            print("У ноды", node.label, "есть родитель", parent.label)
            self.connections.append((self.positions[parent], (x, y)))

        # Обрабатываем детей
        if node.type in {"if", "while"}:
            # Узлы с ветвлением
            true_child = node.children[0] if node.children else None
            false_child = node.children[1] if len(node.children) > 1 else None

            if true_child:
                self.calculate_positions(
                    true_child, parent=node, x=x, y=y + self.vertical_spacing
                )

            if false_child:
                # Для ветви False переходим вправо и вниз
                false_x = x + self.level_width
                self.calculate_positions(
                    false_child, parent=node, x=false_x, y=y + self.vertical_spacing
                )

        else:
            # Для остальных узлов обрабатываем детей последовательно
            child_x = x
            child_y = y + self.vertical_spacing
            for child in node.children:
                print(child)
                self.calculate_positions(child, parent=node, x=child_x, y=child_y)
                child_x += self.level_width

    def layout(self):
        """Запуск расчета позиций."""
        self.calculate_positions(self.tree, x=self.current_x, y=self.current_y)

    def render(self, canvas):
        """Рисует блок-схему на холсте."""
        for node, (x, y) in self.positions.items():
            draw_block(canvas, node, x, y)

        for start, end in self.connections:
            draw_line(canvas, start, end)
