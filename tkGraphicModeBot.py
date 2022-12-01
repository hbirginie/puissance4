from GameState import *
import tkinter as tk
from tkinter import ttk
from random import randint

import sys

class GameFrame(tk.Tk):
    """Fenetre principale, responsable de l'affichage de la barre de statut
    Attributs: 
    ----------
    statusbar: wx.StatusBar
       La barre de statut
    board: Board (voir ci-dessous)
       le plateau de jeu
    
    Méthodes: 
    ---------
    initUI()
       met en place l'interface utilisateur
    makeMenuBar()
        Crée la barre de menu.
    onRestart(e)
        Fonction de réaction aux évènements du Menu
        
    updateStatus(board)
       met à jour la barre de statut en fonction de l'état du plateau <board>
    """
    def __init__(self):
        super().__init__()
        self.title("tkPuissance4")
        self.option_add('*tearOff', False)
        
        self.initUI()
        
    def initUI(self):
        """Met en place l'interface utilisateur."""
        self.frame = tk.Frame(self)
        self.frame.grid(column=0, row=0, columnspan=8)
        self.board = Board(self.frame)
        self.board.grid(column=0, row=0)
        self.makeMenuBar()
        self.makeStatusBar()
        
    def makeMenuBar(self):
        """Crée la barre de menu."""
        menubar = tk.Menu(self)
        self['menu'] = menubar
        menu_main = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_main, label="Main")
        menu_main.add_command(label="Restart", command=self.onRestart)
        menu_main.add_command(label="Undo", command=self.onUndo)
        
    def onRestart(self):
        """Fonction de réaction aux évènements du Menu."""
        self.board.restartGame()
        
    def onUndo(self):
        """Fonction de réaction aux évènements du Menu."""
        self.board.undo()
    
    def playerColor(self,player):
        """Fonction qui renvoie la couleur du joueur."""
        if player==1:
            return 'YELLOW'
        if player==2:
            return 'RED'
    
    def makeStatusBar(self):
        """Met en place la barre de statut."""

        ttk.Label(self, text="Scores: ").grid(column=0, row=1, padx=3, sticky=tk.W)
        ttk.Label(self, text="%s: " % self.playerColor(1)).grid(column=1, row=1, padx=3, sticky=tk.W)
        ttk.Label(self, textvariable=self.board.scores[0]).grid(column=2, row=1, padx=3, sticky=tk.W)
        ttk.Label(self, text="  %s: " % self.playerColor(2)).grid(column=3, row=1, padx=3, sticky=tk.W)
        ttk.Label(self, textvariable=self.board.scores[1]).grid(column=4, row=1, padx=3, sticky=tk.W)
        ttk.Label(self, text="Current Player: ").grid(column=0, row=2, padx=3, sticky=tk.W)
        ttk.Label(self, textvariable=self.board.currentPlayerSymbol).grid(column=1, row=2, padx=3, sticky=tk.W)
        ttk.Label(self, textvariable=self.board.winnerText).grid(column=0, row=3, padx=3, columnspan=4, sticky=tk.W)
        
class Board(tk.Canvas):
    """ Le plateau de jeu. Chargé de l'affichage et du déroulement du jeu.

    Attributs:
    ----------
    game: GameState
       l'état courant du jeu (cf GameState.py)
    scores: list of two ints
       le nombre de parties gagnées par chaque joueur
    currentPlayer: int
       le joueur dont c'est le tour de jouer
    lastStarter: int
       le joueur qui a commencé la partie en cours
    margin: int
       taille de la marge (en nombre de pixels)
    spacing: int
       taille d'une cellule (en nombre de pixels)
    min_spacing: int
       taille minimale d'une cellule pour que le dessin reste lisible
    cells: 3x3 array of tkInter objects
       les objets contenus dans chaque case du jeu:
         + soit un rectangle transparent sur lequel on peut cliquer
         + soit une croix (un tuple de deux lignes)
         + soit un cercle

    Méthodes:
    ---------
    initUI()
       Initialise l'interface utilisateur
    newGame()
       Commence une nouvelle partie
    restartGame()
       Recommence la partie à zéro, en effaçant les scores
    drawGrid()
        Dessine la grille du jeu
    drawCircle(i, j)
        Dessine un cercle en position <i,j> et le rajoute dans self.cells
    makeCell(i, j)
        Construit le rectangle à mettre dans la cellule <i,j> pour 
        réagir aux clics de souris
    makeAllCells()
        Construit toutes les cellules
    positionToCell(pos)
        Convertit une position sur le plateau (en pixels) en position sur la grille.
    applyCell(i, j, func)
        Applique la fonction func aux objets en position <i,j>
    deleteCell(i, j)
    hideCell(i, j)
    showCell(i, j)
        Efface/Montre/Cache les objets présents dans la case <i,j>
    onClick()
        Cette fonction est appelée à chaque clic sur une case non remplie
    """
    def __init__(self, *args, **kw):
        super(Board, self).__init__(*args,width=700,height=700,**kw,bg='blue')
         
        self.scores = [tk.IntVar(value=0), tk.IntVar(value=0)]
        self.currentPlayer = tk.IntVar(value=1)
        self.currentPlayerSymbol = tk.StringVar()
        self.currentPlayer.trace("w", lambda *args:self.currentPlayerSymbol.set(self.playerColor()))
        self.winnerText = tk.StringVar()
        self.lastStarter = 1
        self.winner = False

        self.initUI()
        self.restartGame()
        
    def initUI(self):
        """ Initialise l'interface utilisateur."""
        self.drawGrid()
        self.cells =[None]*7
        self.makeArrows()
        
    def newGame(self):
        """Commence une nouvelle partie."""
        self.winnerText.set("")
        self.game = GameState()
        self.drawGrid()
        self.makeArrows()
        self.lastStarter = 3 - self.lastStarter
        self.currentPlayer.set(self.lastStarter)
        
    def restartGame(self):
        """Recommence la partie à zéro, en effaçant les scores."""
        self.newGame()
        self.scores[0].set(0)
        self.scores[1].set(0)
        self.currentPlayer.set(1)
        self.lastStarter = 1
        self.makeArrows()
    
    def undo(self):
        """Revient au coup précédent."""
        if self.game.hasUndo:
            self.winnerText.set("Vous ne pouvez pas undo 2 fois d'affiler !")
        else:
            i = self.game.lastPlayed[0][0]
            j = self.game.lastPlayed[0][1]
            self.drawCircle(i,j,'white')
            self.currentPlayer.set(3 - self.currentPlayer.get())
            self.game.undo()
            self.makeArrows()
    
    def drawGrid(self):
        """Dessine la grille du jeu."""
        for i in range(7):
            for j in range(6): 
                self.create_oval(i*100+5,j*100+105,i*100+95,j*100+195,fill='white')
        
    def makeArrows(self):
        for i in range(7):
            self.cells[i] = self.create_line(i*100+50,10,i*100+50,90,width=20,arrow='last',arrowshape=(20,20,10),fill=self.playerColor())
            self.tag_bind(self.cells[i], "<Button-1>",lambda event, i=i:self.onClick(event,i))
            
    def colorArrows(self):
        for i in range(7):
            if self.currentPlayer.get()==1:
                self.itemconfig(self.cells[i],fill='yellow')
            if self.currentPlayer.get()==2:
                self.itemconfig(self.cells[i],fill='red')
        
    def drawCircle(self,i,j,color):
        """Dessine un cercle en position <i,j>"""
        self.create_oval(i*100+5,j*100+105,i*100+95,j*100+195,fill=color)
        
    def playCircle(self,colonne):
        if self.currentPlayer.get()==1:
            self.drawCircle(colonne,self.game.highPlayed[colonne],'yellow')
        if self.currentPlayer.get()==2:
            self.drawCircle(colonne,self.game.highPlayed[colonne],'red')
            
    def playerColor(self):
        """Fonction qui renvoie la couleur du joueur."""
        if self.currentPlayer.get()==1:
            return 'YELLOW'
        if self.currentPlayer.get()==2:
            return 'RED'
            
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
            self.winner = False
            self.newGame()
            
    def bot(self):
        """Bot
        1) Joue un coup aléatoire
        """
        # si personne n'a joue au milieu : jouer au milieu
        # 
        
        
        play=randint(0,6)
        while not self.game.canBePlayed(play):
            play=randint(0,6)
        print("Le bot joue dans la colonne",play)
        #self.game.play(self.currentPlayer.get(),play)
        #self.playCircle(play)
            
    def onClick(self, event, i):
        """Fonction de réaction à l'évènement <Button-1> sur un rectangle
        Cet évènement arrive quand on clique avec la souris sur un
        rectangle dessiné sur le Canvas. Cette fonction vérifie qu'on
        peut jouer, et prend en compte le coup s'il est valide.
        """
        if self.currentPlayer.get() == 1:
            self.bot()
        
        if not self.winner:
            if not self.game.canBePlayed(i):
                self.winnerText.set("Vous ne pouvez pas jouer dans la colonne !")
            else:
                self.winnerText.set("")
                winner=self.game.play(self.currentPlayer.get(), i)
                self.playCircle(i)
                self.currentPlayer.set(3 - self.currentPlayer.get())
                self.colorArrows()

                if winner:
                    # En cas de gagnant, on fait clignoter la ligne gagnante 4 fois
                    self.winner = True
                    self.scores[winner-1].set(self.scores[winner-1].get() + 1)
                    if self.game.playerSymbol(winner) == 'O':
                        self.winnerText.set("Player YELLOW wins!")
                    else:
                        self.winnerText.set("Player RED wins!")
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