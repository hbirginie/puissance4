from GameState import *
import tkinter as tk
from tkinter import ttk

import sys

class GameFrame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("tkMorpion")
        self.option_add('*tearOff', False)
        
        self.initUI()
        
    def initUI(self):
        self.frame = tk.Frame(self)
        self.frame.grid(column=0, row=0, columnspan=8)
        self.board = Board(self.frame)
        self.board.grid(column=0, row=0)
        self.makeMenuBar()
        self.makeStatusBar()
        
    def makeMenuBar(self):
        menubar = tk.Menu(self)
        self['menu'] = menubar
        menu_main = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_main, label="Main")
        menu_main.add_command(label="Restart", command=self.onRestart)
        
    def onRestart(self):
        self.board.restartGame()
        
    def makeStatusBar(self):
        
        def playerSymbol(p):
            if p==1:
                return 'YELLOW'
            if p==2:
                return 'RED'

        ttk.Label(self, text="Scores: ").grid(column=0, row=1, padx=3, sticky=tk.W)
        ttk.Label(self, text="%s: " % playerSymbol(1)).grid(column=1, row=1, padx=3, sticky=tk.W)
        ttk.Label(self, textvariable=self.board.scores[0]).grid(column=2, row=1, padx=3, sticky=tk.W)
        ttk.Label(self, text="  %s: " % playerSymbol(2)).grid(column=3, row=1, padx=3, sticky=tk.W)
        ttk.Label(self, textvariable=self.board.scores[1]).grid(column=4, row=1, padx=3, sticky=tk.W)
        ttk.Label(self, text="Current Player: ").grid(column=0, row=2, padx=3, sticky=tk.W)
        ttk.Label(self, textvariable=self.board.currentPlayer).grid(column=1, row=2, padx=3, sticky=tk.W)
        ttk.Label(self, textvariable=self.board.winnerText).grid(column=0, row=3, padx=3, columnspan=4, sticky=tk.W)
        
class Board(tk.Canvas):
    def __init__(self, *args, **kw):
        super(Board, self).__init__(*args,width=700,height=700,**kw,bg='blue')
         
        self.scores = [tk.IntVar(value=0), tk.IntVar(value=0)]
        self.currentPlayer = tk.IntVar(value=1)
        self.currentPlayerSymbol = tk.StringVar()
        self.currentPlayer.trace("w", lambda *args:self.currentPlayerSymbol.set(self.game.playerSymbol(self.currentPlayer.get())))
        self.winnerText = tk.StringVar()
        self.lastStarter = 1

        self.initUI()
        self.restartGame()
        
    def initUI(self):
        self.drawGrid()
        self.cells =[None]*7
        self.makeArrows()
        
    def newGame(self):
        self.winnerText.set("")
        self.game = GameState()
        self.lastStarter = 3 - self.lastStarter
        self.currentPlayer.set(self.lastStarter)
        self.drawGrid()
        self.makeArrows()
        
    def restartGame(self):
        self.newGame()
        self.scores[0].set(0)
        self.scores[1].set(0)
        self.currentPlayer.set(1)
        self.lastStarter = 1
    
    def drawGrid(self):
        for i in range(7):
            for j in range(6): 
                self.create_oval(i*100+5,j*100+105,i*100+95,j*100+195,fill='white')
        
    def makeArrows(self):
        for i in range(7):
            self.cells[i] = self.create_line(i*100+50,10,i*100+50,90,width=20,arrow='last',arrowshape=(20,20,10))
            self.tag_bind(self.cells[i], "<Button-1>",lambda event, i=i:self.onClick(event,i))
        
    def deleteArrows(self):
        for i in range(7):
            self.itemconfig(self.cells[i],fill='blue')
        
    
    def drawCircle(self,i,j,color):
        self.create_oval(i*100+5,j*100+105,i*100+95,j*100+195,fill=color)
        
    def playCircle(self,colonne):
        if self.currentPlayer.get()==1:
            self.drawCircle(colonne,self.game.highPlayed[colonne],'yellow')
        if self.currentPlayer.get()==2:
            self.drawCircle(colonne,self.game.highPlayed[colonne],'red')
            
    def hideCell(self, i, j):
        self.drawCircle(i,j,'white')
        
    def showCell(self, i, j):
        if self.game.winner()==1:
            self.drawCircle(i,j,'yellow')
        if self.game.winner()==2:
            self.drawCircle(i,j,'red')
          
    def hideWinningLine(self):
        for cell in self.game.winningLine:
            self.hideCell(cell[0], cell[1])
        self.after(250, self.showWinningLine)

    def showWinningLine(self):
        for cell in self.game.winningLine:
            self.showCell(cell[0], cell[1])
        self.nbFlashesRemaining -= 1
        if self.nbFlashesRemaining:
            self.after(250, self.hideWinningLine)
        else:
            self.newGame()
            
    def onClick(self, event, i):
        if not self.game.canBePlayed(i):
            print("Vous ne pouvez pas jouer dans la colonne",i)
        else:
            winner=self.game.play(self.currentPlayer.get(), i)
            self.playCircle(i)
            self.currentPlayer.set(3 - self.currentPlayer.get())

            if winner:
                # En cas de gagnant, on fait clignoter la ligne gagnante 4 fois
                self.deleteArrows()
                self.scores[winner-1].set(self.scores[winner-1].get() + 1)
                self.winnerText.set("Player %s wins!" % self.game.playerSymbol(winner))
                self.nbFlashesRemaining = 4
                self.after(250, self.hideWinningLine)
            elif self.game.isTie():
                # En cas de match nul, on attend une seconde avant de lancer une nouvelle partie
                self.winnerText.set("Tie !")
                self.after(1000, self.newGame)
                self.currentPlayer.set(3 - self.currentPlayer.get())
                
def main():
    """Fonction principale, qui crée la fenêtre de jeu et lance l'exécution."""
    app = GameFrame()
    app.mainloop()

if __name__ == '__main__':
    main()        