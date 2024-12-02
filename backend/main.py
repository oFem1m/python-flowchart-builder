import tkinter as tk
from block_parser import build_blocks
from parser import CodeTreeBuilder


def main():
    # Парсинг кода
    with open("test_file.py", "r") as file:
        code = file.read()
    builder = CodeTreeBuilder()

    tree = builder.build_tree(code)
    print("полное дерево: ", tree)

    # Создание блоков
    blocks = build_blocks(tree)
    for block in blocks:
        print(block)


    # Генерация блок-схемы
    # layout = FlowchartLayout(tree)
    # layout.layout()

    # Отрисовка
    # root = tk.Tk()
    # root.title("Flowchart")
    # canvas = tk.Canvas(root, width=1920, height=1080, bg="white")
    # canvas.pack()
    #
    # layout.render(canvas)
    # root.mainloop()


if __name__ == "__main__":
    main()
