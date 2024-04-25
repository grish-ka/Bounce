# read README.txt
# before launching
# python=3.11
from tkinter import *
import random
import time

class rectangel:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(10, 10, 50, 50, fill=color)
    def drew(self, coler):
        self.canvas.itemconfigure(self.id, fill=coler)
        #self.canvas.move(self.id, 10, 10)


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        pos = self.canvas.coords(self.id)
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False
    
    def draw(self):
        self.hit_bottom = False
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.y = -3
            if pos[3] >= self.canvas_height:
                self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

class Score:
    def __init__(self, canvas, win=3):
        self.score = 0
        self.win = win
        self.canvas = canvas
        self.id = canvas.create_text(30, 10, text="score = %s/3"% self.score)

    def draw(self):
        self.canvas.itemconfigure(self.id, text="score = %s/3"% self.score)

    def increase(self):
        self.score = self.score + 1

    def winsys(self):
        return self.score >= self.win

class Fails:
    def __init__(self, canvas, fails=3):
        self.fail = 0
        self.fails =fails
        self.canvas =canvas
        self.id = canvas.create_text(100, 10, text="fails = %s/3"% self.fail)

    def drew(self):
        self.canvas.itemconfigure(self.id, text="fails %s/3"% self.fail)

    def increase(self):
        self.fail = self.fail + 1

    def losesys(self):
        return self.fail >= self.fails

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -5
    
    def turn_right(self, evt):
        self.x = 5
tk = Tk()

tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')
score = Score(canvas, 3)
failsv = Fails(canvas, 3)
rec = rectangel(canvas, 'blue')

while 1:
    if ball.hit_paddle(0):
        score.increase()
    
    if ball.hit_bottom == True:
        failsv.increase()
    
    if score.winsys() == True:
        canvas.create_text(245, 100, text= "You Won")
        tk.update()
        time.sleep(5)
        break
    elif failsv.losesys() == True:
        score.score = 0
        failsv.fail = 0
    
    # elif ball.hit_bottom == False:
    ball.draw()
    paddle.draw()
    score.draw()
    failsv.drew()
    rec.drew('blue')
    # else:
    #     score.score = 0


    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
