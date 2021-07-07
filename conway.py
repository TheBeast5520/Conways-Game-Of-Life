from tkinter import *
import numpy as np
import time


class Cell(Canvas):

    def __init__(self, master, row, column, alive=False):
        self.row = row
        self.column = column
        self.alive = alive
        Canvas.__init__(self, master, width=25, height=25,
                        bg=self.color(), highlightthickness=0, relief=RAISED)
        self.bind('<Button-1>', self.toggle_alive)
        self.future_alive = False

    def toggle_alive(self, event=None):
        if self.alive:
            self.alive = False
            self['bg'] = 'gray'
        else:
            self.alive = True
            self['bg'] = 'green'

    def make_alive(self):
        self.alive = True
        self['bg'] = 'green'

    def make_dead(self):
        self.alive = False
        self['bg'] = 'gray'

    def color(self): return ('green' if self.alive else 'gray')


class Grid(Frame):

    def __init__(self, master):
        self.root = Tk()
        Frame.__init__(self, master)
        self.grid()

        self.width = 20
        self.height = 20

        self.cells = [[Cell(self, i, j) for j in range(self.width)]
                      for i in range(self.height)]
        for i in self.cells:
            for j in i:
                j.grid(row=j.row, column=j.column)


        self.button = Button(master=self, command=self.step, text="STEP")
        self.button.grid(row=self.height + 1, column=0, columnspan=self.width)
        self.button1 = Button(master=self, command=self.run, text="RUN")
        self.button1.grid(row=self.height+1, column=5, columnspan=self.width)

    def num_neighbors(self, row, column):
        counter = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                if row + i >= 0 and row + i < self.height and column + j >= 0 and column + j < self.width:
                    counter += (1 if self.cells[row + i]
                                [column + j].alive else 0)
        return counter

    def step(self):
        '''performs one generation'''
        for i in range(self.height):
            for j in range(self.width):
                x = self.num_neighbors(i, j)
                if (self.cells[i][j].alive and (x < 2 or x > 3)) or (self.cells[i][j].alive == False and x != 3):
                    self.cells[i][j].future_alive = False
                else:
                    self.cells[i][j].future_alive = True
        for i in range(self.height):
            for j in range(self.width):
                if self.cells[i][j].future_alive:
                    self.cells[i][j].make_alive()
                else:
                    self.cells[i][j].make_dead()

    def run(self):
        self.step()
        self.root.after(100, self.run)

def start_conway():
    root = Tk()
    game = Grid(root)
    root.mainloop()


start_conway()
