'''
ChaCha20 Visualization Module
CS5800, Spring 2022
Professor Jamieson
Nathaniel Webb, Aaron Fihn, Prateep Malyala, Shang Xiao
'''

import time
from graphics import *
from word import Word


class ChaChaViz:
    dround_count = 0
    qround_count = 0
    is_column = False
    frame_rate = 0.2

    def __init__(self, frame_rate):
        # Set draw speed
        self.frame_rate = frame_rate

        # Create draw window
        self.win = GraphWin("ChaCha20", 1280, 660)

        # Override size and position of draw window
        w, h = 1280, 660  # Width and height.
        x, y = 100, 100  # Screen position.
        self.win.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # set draw window background color
        self.win.setBackground("white")

    # DRAWING METHODS
    def __clear(self):
        time.sleep(self.frame_rate)
        for item in self.win.items[:]:
            item.undraw()
        self.win.update()

    def __print_block(self, block, second_block, index_a = None, index_b = None, operator = None):
        for i in range(16):
            print_color = 'black'
            if i == index_a:
                print_color = 'blue' if second_block else 'green'
            elif i == index_b:
                print_color = 'red'

            x_offset = i%4
            y_offset = i//4

            x = 200 + 300 * x_offset
            y = 150 + 60 * y_offset # + block_offset

            message = Text(Point(x, y), str(block[i]))
            message.setTextColor(print_color)
            message.setSize(36)
            message.draw(self.win)

            if i == index_b and operator is not None:
                op_message = Text(Point(x - 146, y - 2), operator)
                op_message.setSize(36)
                op_message.draw(self.win)

    def __print_legend(self):
        message1 = Text(Point(640, 440), "double-round: " + str(self.dround_count))
        message1.setTextColor('black')
        message1.setSize(36)

        message2 = Text(Point(640, 560), "quarter-round: " + str(self.qround_count))
        message2.setTextColor('black')
        message2.setSize(36)

        type_string = 'Column' if self.is_column else 'Diagonal'
        message3 = Text(Point(640, 500), type_string)
        message3.setTextColor('black')
        message3.setSize(36)

        message1.draw(self.win)
        message2.draw(self.win)
        message3.draw(self.win)

    # OPERATION METHODS
    def __add(self, start_block, from_index, to_index):
        self.__print_legend()
        self.__print_block(start_block, False, from_index, to_index, '+')
        self.__clear()

    def __lrot(self, start_block, index):
        self.__print_legend()
        self.__print_block(start_block, False, index, index, '<')
        self.__clear()

    def __result(self, block, index):
        self.__print_legend()
        self.__print_block(block, True, index)
        self.__clear()

    def __xor(self, start_block, from_index, to_index):
        self.__print_legend()
        self.__print_block(start_block, False, from_index, to_index, '^')
        self.__clear()

    # PUBLIC METHODS
    def final_xor(self):
        print()

    def qround(self, y: list[Word], indices, dround_count, qround_count, is_column):
        self.dround_count = dround_count + 1
        self.qround_count = qround_count
        self.is_column = is_column

        self.__add(y, indices[1], indices[0])
        y[indices[0]] = y[indices[0]] + y[indices[1]]
        self.__result(y, indices[0])

        self.__xor(y, indices[0], indices[3])
        y[indices[3]] = y[indices[3]] ^ y[indices[0]];
        self.__result(y, indices[3])

        self.__lrot(y, indices[3])
        y[indices[3]] = y[indices[3]] << 16
        self.__result(y, indices[3])

        self.__add(y, indices[3], indices[2])
        y[indices[2]] = y[indices[2]] + y[indices[3]]
        self.__result(y, indices[2])

        self.__xor(y, indices[2], indices[1])
        y[indices[1]] = y[indices[1]] ^ y[indices[2]]
        self.__result(y, indices[1])

        self.__lrot(y, indices[1])
        y[indices[1]] = y[indices[1]] << 12
        self.__result(y, indices[1])

        self.__add(y, indices[1], indices[0])
        y[indices[0]] = y[indices[0]] + y[indices[1]]
        self.__result(y, indices[0])

        self.__xor(y, indices[0], indices[3])
        y[indices[3]] = y[indices[3]] ^ y[indices[0]]
        self.__result(y, indices[3])

        self.__lrot(y, indices[3])
        y[indices[3]] = y[indices[3]] << 8
        self.__result(y, indices[3])

        self.__add(y, indices[3], indices[2])
        y[indices[2]] = y[indices[2]] + y[indices[3]]
        self.__result(y, indices[2])

        self.__xor(y, indices[2], indices[1])
        y[indices[1]] = y[indices[1]] ^ y[indices[2]]
        self.__result(y, indices[1])

        self.__lrot(y, indices[1])
        y[indices[1]] = y[indices[1]] << 7
        self.__result(y, indices[1])