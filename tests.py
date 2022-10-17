import tkinter as tk
from tkinter import *

fenetre = tk.Tk()
fenetre.title("puissance 4")
canvas = tk.Canvas(fenetre, width=700, height=600, bg='blue')
canvas.pack()

def draw_circle(x,y,color):
    canvas.create_oval(x*100+5,y*100+5,x*100+95,y*100+95,fill=color)
    
for i in range(7):
    for j in range(6):
        draw_circle(i,j,'white')
              
def play(x,y,player):
    if player==0:
        draw_circle(x,y,'yellow')
    if player==1:
        draw_circle(x,y,'red')
    
play(3,5,0)
play(4,5,1)
play(4,4,0)
play(3,4,1)
play(5,5,0)
play(4,3,1)
play(3,3,0)
play(2,5,1)
play(2,4,0)
play(2,3,1)
play(2,2,0)

def win_line(x1,y1,x2,y2):
    canvas.create_line(x1*100+50,y1*100+50,x2*100+50,y2*100+50,fill='black',width=5)
    
win_line(2,2,5,5)
    
fenetre.mainloop()


"""
for i in range(1,7):
    canvas.create_line(100*i,0,100*i,600,fill='black',width=2)
for j in range(1,6):
    canvas.create_line(0,100*j,700,100*j,fill='black',width=2)
"""