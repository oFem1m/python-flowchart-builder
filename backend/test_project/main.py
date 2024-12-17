from backend.trash.block_parser2 import build_blocks
from parser import CodeTreeBuilder
from blocks_creator import build_blocks


code = '''
def sample_function(x):
    if x < 0:
        x += 5
    elif x == 0:
        s = 0
        while s < 3:
            s += 1
        return 0
    else:
        for i in range(5):
            print(i)
        x -= 5
    y = 6
    return x

'''

def main():


    # Парсинг кода и построение дерева
    builder = CodeTreeBuilder()
    ast_tree = builder.build_tree(code)
    print(ast_tree)

    # Создание блоков
    blocks = build_blocks(ast_tree)
    print(blocks)

    # root = tk.Tk()
    # root.title("Flowchart")
    # canvas = tk.Canvas(root, width=1000, height=800, bg="white")
    # canvas.pack()
    #
    # layout = FlowchartLayout(blocks)
    # layout.layout()
    # layout.render(canvas)
    #
    # root.mainloop()

if __name__ == "__main__":
    main()
