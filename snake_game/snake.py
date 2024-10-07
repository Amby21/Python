from turtle import Screen,Turtle
X_POSITIONS = [(0,0),(-20,0),(-40,0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0
class Snake(Turtle):

    def __init__(self):
        super().__init__()
        self.turtles = []
        self.create_snake()
        self.head = self.turtles[0]

    def create_snake(self):
        for i in X_POSITIONS:
            print(i)
            self.add_turtle(i)

    def add_turtle(self,position):
            new_turtle = Turtle()
            new_turtle.shape("square")
            new_turtle.color("white")
            new_turtle.penup()
            new_turtle.goto(x=position[0] , y= position[1])
            self.turtles.append(new_turtle)

    def extend(self):
        self.add_turtle(self.turtles[-1].position())

    def move(self):
        for turtle_num in range(len(self.turtles)-1,0,-1):
            new_x = self.turtles[turtle_num - 1].xcor()
            new_y = self.turtles[turtle_num - 1].ycor()
            self.turtles[turtle_num].goto(new_x,new_y)
        self.turtles[0].forward(MOVE_DISTANCE)
    
    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)
    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)
    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)
    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)       

<<<<<<< HEAD
    def reset(self):
        for turtle in self.turtles:
            turtle.goto(1000,1000)    
        self.turtles.clear()
        self.create_snake()
        self.head = self.turtles[0]
        
    

=======
>>>>>>> 62bcf6f72043afa7fd97b491578ba20565b4cad9
    
    # self.turtles[0].left(90) 