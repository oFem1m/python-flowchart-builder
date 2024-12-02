class Block:
    def __init__(self, block_id: int, block_type: str, label: str):
        """
        Инициализация блока.
        """
        self.id = block_id
        self.type = block_type
        self.label = label
        self.connections = []  # Список соседей (связей) блока

    def add_connection(self, block_id: int):
        """
        Добавить соединение с другим блоком.

        :param block_id: ID блока, с которым устанавливается связь.
        """
        if block_id not in self.connections:
            self.connections.append(block_id)

    def __repr__(self):
        """
        Удобное строковое представление для вывода блока.
        """
        return f"Block(id={self.id}, type='{self.type}', label='{self.label}', connections={self.connections})"


# Создаем блоки
block1 = Block(1, "def", "def sample_function(x)")
block2 = Block(2, "process", "Обработать данные")
block3 = Block(3, "decision", "Условие проверки")
block4 = Block(4, "end", "Конец")

# Добавляем связи между блоками
block1.add_connection(2)
block2.add_connection(3)
block3.add_connection(4)

# Вывод блоков
print(block1)
print(block2)
print(block3)
print(block4)

# for i in xs:
#     if x % 2 == 0:
#         print("найдено четное")
#         break
#     else:
#         print("все нечетные")
