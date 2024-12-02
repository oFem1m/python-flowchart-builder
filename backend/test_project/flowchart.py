import tkinter as tk


def draw_line(canvas, start, end):
    """Рисует линии переходов между блоками."""
    x1, y1 = start
    x2, y2 = end
    canvas.create_line(x1 + 75, y1 + 50, x2 + 75, y2, arrow=tk.LAST)


def draw_block(canvas, block, x, y):
    """Рисует блоки в зависимости от типа блока."""
    block_width, block_height = 150, 50
    if block.type == "function" or block.type == "return":
        canvas.create_oval(
            x, y, x + block_width, y + block_height, fill="lightblue"
        )
    elif block.type in {"if", "while"}:
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
    elif block.type == "for":
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
    canvas.create_text(x + block_width // 2, y + block_height // 2, text=block.label)


class FlowchartLayout:
    def __init__(self, blocks):
        self.blocks = blocks  # Список блоков
        self.positions = {}  # Координаты каждого блока
        self.connections = []  # Список соединений между блоками
        self.visited = set()  # Для отслеживания обработанных блоков
        self.grid = {}  # Сетка для размещения узлов: (x, y) -> блок
        self.current_x = 10  # Горизонтальное смещение
        self.current_y = 10  # Вертикальное смещение
        self.level_width = 200  # Ширина уровня между узлами
        self.vertical_spacing = 100  # Вертикальное расстояние между уровнями

    def calculate_positions(self, block_id, parent_position=None):
        """Рекурсивный DFS для вычисления позиций блоков."""
        if block_id in self.visited:
            return
        self.visited.add(block_id)

        # Устанавливаем позицию текущего блока
        x, y = self.current_x, self.current_y
        while (x, y) in self.grid:
            x += self.level_width
        self.positions[block_id] = (x, y)
        self.grid[(x, y)] = block_id

        # Если есть родительская позиция, добавляем соединение
        if parent_position:
            self.connections.append((parent_position, (x, y)))

        # Получаем текущий блок
        block = next(b for b in self.blocks if b.id == block_id)

        # Обрабатываем связи
        for connection_id in block.connections:
            self.current_y += self.vertical_spacing
            self.calculate_positions(connection_id, parent_position=(x, y))

    def layout(self):
        """Запуск расчета позиций."""
        # Ищем первый блок (начальный)
        start_block = next(b for b in self.blocks if b.type == "function")
        self.calculate_positions(start_block.id)

    def render(self, canvas):
        """Рисует блок-схему на холсте."""
        for block_id, (x, y) in self.positions.items():
            block = next(b for b in self.blocks if b.id == block_id)
            draw_block(canvas, block, x, y)

        for start, end in self.connections:
            draw_line(canvas, start, end)

