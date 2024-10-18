#%%
import turtle
import pandas as pd
#%%
screen = turtle.Screen()
screen.title('U.S. States Game')
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)
states_data = pd.read_csv("50_states.csv")
all_states = states_data['state'].to_list()
score = 0
while score < 50:
    answer_state = screen.textinput( title = f"{score}/50", prompt="What is another state name?" ).title()
    if answer_state in all_states:
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_corr = None
        state_corr = states_data[states_data.state == answer_state]
        score += 1
        
        x = int(state_corr.x.item())
        y = int(state_corr.y.item())
        # print(x,y) 
        t.goto(x,y)
        t.pendown()
        t.write(answer_state,align="center")
        
screen.exitonclick()
# %%
