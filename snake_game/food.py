from turtle import Turtle
import random
class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(stretch_len=0.5,stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        self.penup()
        self.refresh()

    def refresh(self):
        randomx=random.randint(-280,280)
        randomy=random.randint(-280,280)
        self.goto(randomx,randomy)
