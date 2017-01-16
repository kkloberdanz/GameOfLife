'''
Programmer: Kyle Kloberdanz
Description: Conway's Game of Life

Notes:
    Only tested on Linux (Ubuntu GNOME 16.10)
    Probably will not work on Windows
'''
import math
import random
import hashlib
import os
import sys

from time import sleep

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def distance(self, other):
        ''' Returns Euclidean distance between 2 points '''
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

class Cell(Point):
    def __init__(self, x=0, y=0, alive=False):
        self.alive = alive
        Point.__init__(self, x, y)

    def __repr__(self):
        if self.alive:
            return bcolors.OKGREEN + "*" + bcolors.ENDC
        else:
            return " "
class Iter:
    def __init__(self, begin=0, end=0):
        if begin > end:
            raise ValueError("Iter: begin cannot be greater than end\n" + 
                    "begin = " + str(begin) + "end = " + str(end))

        else:
            self.begin = begin
            self.end   = end

    def __repr__(self):
        return str((begin, end))


class Board:

    def __init__(self, width=0, height=0):
        if width < 0 or height < 0:
            raise ValueError("Dimensions cannot be negative")

        else:
            self.board = []
            self.width = width
            self.height = height
            for i in range(self.height):
                tmp_l = []
                for j in range(self.width):
                    tmp_l.append(Cell())
                self.board.append(tmp_l)

    def __repr__(self):
        ret_s = ""

        # Draw top bar
        for j in range(self.width):
            ret_s += '--'
        ret_s += '\n' 

        for i in range(self.height):
            for j in range(self.width):
                ret_s += '|'
                ret_s += str(self.board[i][j])
            ret_s += '|\n'
            for j in range(self.width):
                ret_s += '--'
            ret_s += '\n' 

        return ret_s[:-1]

    def draw(self):
        ''' Prints Board to stdout '''
        print(self.__repr__() + "\n\n")
    
    def set_cell(self, cell):
        ''' Place a cell at Cell point 'cell' in the board '''
        self.board[cell.y][cell.x] = cell

    def get_iter_y(self, n):
        return Iter(max(n - 1, 0), 1 + min(n + 1, self.height))

    def get_iter_x(self, n):
        return Iter(max(n - 1, 0), 1 + min(n + 1, self.width))

    def get_living_neighbors(self, cell):
        ''' returns list of type Cell that 
        holds the neighbors of the given cell '''
        ret_l = []

        # contains the ranges to iterate over
        y_range = self.get_iter_y(cell.y)
        x_range = self.get_iter_x(cell.x)

        # C++ style iteration over neighbors
        for y in range(y_range.begin, y_range.end):
            for x in range(x_range.begin, x_range.end):
                if x < self.width and x >= 0 and y < self.height and y >= 0:
                    c = self.board[y][x]
                    if c.alive and c != cell:
                        ret_l.append(c)

        return ret_l

    def check_rules(self, cell):
        ''' Applies rules for Conway's Game of Life to the given cell '''
        neighbors_l = self.get_living_neighbors(cell)

        # 1. Any live cell with fewer than two live neighbours dies, 
        #    as if caused by underpopulation.
        # 2. Any live cell with two or three live neighbours lives 
        #    on to the next generation.
        if (len(neighbors_l) < 2):
            self.board[cell.y][cell.x].alive = False

        # 3. Any live cell with more than three live neighbours dies, 
        #    as if by overpopulation.
        if (len(neighbors_l) > 3):
            self.board[cell.y][cell.x].alive = False

        # 4. Any dead cell with exactly three live neighbours 
        #    becomes a live cell, as if by reproduction.
        if len(neighbors_l) == 3:
            self.board[cell.y][cell.x].alive = True

    def run(self, delay=2):
        sleep(delay)
        while True:
            old_hash = hashlib.md5(self.__repr__().encode("utf-8"))
            for y in range(self.height):
                for x in range(self.width): 
                    cell = self.board[y][x]
                    self.check_rules(cell)
            self.draw()

            new_hash = hashlib.md5(self.__repr__().encode("utf-8"))
            if old_hash.hexdigest() == new_hash.hexdigest():
                print("Simulation complete: no more movement possible")
                break

            sleep(delay)


def test():
    # TEST
    p1 = Point()

    p2 = Point(1, 3)

    print(p1)
    print(p2)

    print(p1.distance(p2))
    print(p2.distance(p2))
    print(p2.distance(p1))
    print(p1.distance(p1))

    B = Board(10, 10)
    B.draw()
    B.set_cell(Cell(1,2, alive=True))
    B.set_cell(Cell(1,3, alive=True))
    B.set_cell(Cell(1,4, alive=True))

    B.set_cell(Cell(1,5, alive=True))
    B.set_cell(Cell(3,5, alive=True))
    print("\n------------------\n")
    print(B)

    c1 = Cell(2,3, True)
    B.set_cell(c1)

    neighbors_l = B.get_living_neighbors(c1)
    for c in neighbors_l:
        print(c.x, c.y)
    print(B)

    B.run()

# Main
# x = 80
# y = 50

# set x and y to the size of the console (UNIX only)

x, y = os.popen("stty size", 'r').read().split()
x = int(x)
y = int(y) // 8

if len(sys.argv) > 1:
    p = float(sys.argv[1]) / 100
else:
    p = 0.75 # percent coverage of cells

b = Board(x, y)

print("Dimensions:", x, y)
print("Percent Coverage:", str(p * 100) + "%")
input("Press RETURN to start simulation")

for i in range(x):
    for j in range(y):
        r = random.random()
        if r < p:
            b.set_cell(Cell(i, j, alive=True))

print("Start:")
b.draw()

b.run()

