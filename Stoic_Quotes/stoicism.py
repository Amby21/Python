from tkinter import *
import PIL
from PIL import ImageTk, Image
import requests
import json
import time
#--------------------CONSTANTS------------------------------ #
FONT_NAME = "Georgia"
QUOTE_COLOR = "#DAFFFB"
ALT_BG = "#1D495C"
#-------------------API CALL-------------------------------- #
def stoic_call():
    response = requests.get("https://stoic.tekloon.net/stoic-quote")
    # print(response.content)
    json_data = json.loads(response.content)
    quote = json_data["quote"]
    quote = quote.replace("@", "")
    print("Quote:", quote)
    canvas.itemconfig(quote_text,text=quote)
    window.after(10000, stoic_call)
# ------------------- UI SETUP------------------------------ #


window = Tk()

window.title ("Stoicism")
window.config(bg="#001C30")

#Title config
title_label = Label(text="Stoic Quotes", fg=QUOTE_COLOR,bg="#001C30",font=(FONT_NAME,30))
title_label.grid(column=0,row=0)

#Load Stoic Image
stoic_img = Image.open("stoic.png")
tk_img = ImageTk.PhotoImage(stoic_img)

#Canvas width and height measurements in Pixels
canvas = Canvas(width=680, height=450,background="#001C30",highlightthickness=0)
#Left Aligned image
canvas.create_image(10,250 ,image=tk_img, anchor="w")
canvas.grid(column=0,row=1)
quote_text = canvas.create_text(600,250,text="Stoic Quote",fill=QUOTE_COLOR, font=(FONT_NAME,15,"bold"), anchor="e",width=300)


#API function call.
stoic_call()
window.mainloop()