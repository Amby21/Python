from turtle import Turtle

class Score(Turtle):

    def __init__(self):
        super().__init__()
        self.count = 0
        with open("score.txt") as file:
            high_score  = file.read()
            self.highscore = int(high_score)
        
        self.color("white")
        self.penup()
        self.goto(0,270)
        self.write (f"Score: {self.count}",  align='center', font=('Arial', 20, 'normal'))
        self.hideturtle()
    
    def update_scoreboard(self):
        self.clear()
        self.write (f"Score: {self.count} High Score: {self.highscore}",  align='center', font=('Arial', 20, 'normal'))
    
  
    def score_count(self):
        self.count += 1
        self.update_scoreboard()

    def reset(self):
        if self.count > self.highscore:
            self.highscore = self.count
            with open("score.txt",mode="w") as file:
                file.write(self.highscore)

        self.count = 0
        self.update_scoreboard()
