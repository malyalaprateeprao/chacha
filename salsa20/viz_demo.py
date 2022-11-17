from chachaviz import ChaChaViz
from word import Word

def main():
    c = b'abcdefghijklmnopqrstuvwxyz123456abcdefghijklmnopqrstuvwxyz123456'
    x = bytes(c)
    
    u = [None]*16
    for i in range(16):
        j = i*4
        u[i] = Word(seq=bytes([x[j], x[j+1], x[j+2], x[j+3]]))

    visualizer = ChaChaViz()
    visualizer.add(u, u, 1, 5)
    visualizer.xor(u, u, 6, 7)
    visualizer.lrot(u, u, 3)
    visualizer.block(u)
    visualizer.end()


if __name__ == "__main__":
    main()
