# import tkinter as tk
# from parser import CodeTreeBuilder
# from block_parser import build_blocks, Block
# from flowchart import calculate_layout, draw_blocks
#
# def main():
#     # Parsing code
#     with open("test_file.py", "r") as file:
#         code = file.read()
#     builder = CodeTreeBuilder()
#     tree = builder.build_tree(code)
#
#     # Building blocks
#     blocks = build_blocks(tree)
#     Block1 = Block(1, 'function', 'def sample_function(x):', 1)
#     Block1.connections = [2]
#     Block2 = Block(2, 'if', 'if x < 0:', 2)
#     Block2.connections = [3, 6]
#     Block3 = Block(3, 'aug_assign', 'x += 5', 3)
#     Block3.connections = [4]
#     Block4 = Block(4, 'aug_assign', 'y = 6', layer=8)
#     Block4.connections = [5]
#     Block5 = Block(5, 'return', 'return x', layer=9)
#     Block5.connections = []
#     Block6 = Block(6, 'if', 'if x == 0:', layer=3)
#     Block6.connections = [7, 11]
#     Block7 = Block(7, 'aug_assign', 's = 0', layer=4)
#     Block7.connections = [8]
#     Block8 = Block(8, 'while', 'while s < 3:', layer=5)
#     Block8.connections = [9, 10]
#     Block9 = Block(9, 'aug_assign', 's += 1', layer=6)
#     Block9.connections = [8]
#     Block10 = Block(10, 'return', 'return 0', layer=7)
#     Block10.connections = []
#     Block11 = Block(11, 'for', 'for i in range(5):', layer=4)
#     Block11.connections = [12, 13]
#     Block12 = Block(12, 'call', 'print(i)', layer=5)
#     Block12.connections = [11]
#     Block13 = Block(13, 'aug_assign', 'x -= 5', layer=6)
#     Block13.connections = [4]
#
#     blocks = [
#         Block1,
#         Block2,
#         Block3,
#         Block4,
#         Block5,
#         Block6,
#         Block7,
#         Block8,
#         Block9,
#         Block10,
#         Block11,
#         Block12,
#         Block13,
#     ]
#
#
#
#     for block in blocks:
#         print(block)  # For debugging purposes
#
#     # Calculate layout
#     calculate_layout(blocks)
#
#     # Drawing
#     root = tk.Tk()
#     root.title("Flowchart")
#     canvas = tk.Canvas(root, width=1920, height=1080, bg="white")
#     canvas.pack()
#
#     draw_blocks(canvas, blocks)
#     root.mainloop()
#
# if __name__ == "__main__":
#     main()


# main.py

import tkinter as tk
from parser import CodeTreeBuilder
from block_parser import build_blocks, Block
from flowchart import draw_flowchart

def main():
    # Парсинг кода из файла test_file.py
    with open("test_file.py", "r") as file:
        code = file.read()

    # Построение дерева Node с помощью CodeTreeBuilder
    builder = CodeTreeBuilder()
    tree = builder.build_tree(code)
    print("Node Tree:")
    print(tree)

    # Конвертация дерева Node в список блоков
    blocks = build_blocks(tree)

    print("\nBlocks:")
    for block in blocks:
        print(block)



    # Отрисовка блок-схемы
    draw_flowchart(blocks)

if __name__ == "__main__":
    main()
