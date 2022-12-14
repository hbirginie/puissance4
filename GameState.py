class GameState:
    """ Cette classe contient toutes les informations sur l'état d'une partie.
    Attributs: 
    ----------
    grid : 7x6 array 
        la grille de jeu. Chaque position peut être None si aucun joueur n'y a joué, 
        ou le numéro du joueur qui y a joué.
    highPlayed : list of int
        Liste d'entiers qui contient le plus haut pion déjà jouer par colonnes,
        None si aucun pion n'a été joué.
    hasWon : 
        L'identifiant du joueur gagnant s'il existe.
    winningLine : list of (int,int)
        identifie la ligne gagnante si elle existe, None sinon
    nbRemainingMoves : int
        nombre de coups qu'il reste à jouer
    possibleLines : list of list of (int, int)
        Liste des lignes qui permettent de gagner:
        si il existe i tel que toutes les positions de possibleLines[i] sont occupées
        par le même joueur, alors ce joueur a gagné. 

    Méthodes: 
    ---------
    play(player, x)
       Joue un coup pour le joueur <player> dans la colonne <x>.
    canBePlayed(x)
       Renvoie True si la colonne <x> est jouable, False sinon.
    winner():
        Renvoie l'identifiant du gagnant s'il existe, None sinon.
    isTie():
        Renvoie True si la partie s'est terminé sur un match nul.
    getCell(x, y):
        Renvoie l'identifiant du joueur qui a joué en position <x, y>.
    setCell(x, y, v):
        Change l'identifiant du joueur qui a joué en position <x, y>.
    playerSymbol(player):
        Renvoie le symbole du joueur dont l'identifiant est <player>.
    textDisplay():
        Affiche l'état de la partie (en mode texte) dans le terminal.
    displayWinner():
        Affiche le gagnant de la partie dans le terminal.
    """
    
    possibleLines = [[(j, i) for j in range(0, 4)]  for i in range(0, 6) ] # les 24 façons de gagner en horizontale : 6 par lignes
    possibleLines += [[(j, i) for j in range(1, 5)]  for i in range(0, 6) ]
    possibleLines += [[(j, i) for j in range(2, 6)]  for i in range(0, 6) ]
    possibleLines += [[(j, i) for j in range(3, 7)]  for i in range(0, 6) ]
    
    possibleLines += [[(i, j) for j in range(0, 4)]  for i in range(0, 7) ] # les 21 façons de gagner en verticale : 7 par lignes
    possibleLines += [[(i, j) for j in range(1, 5)]  for i in range(0, 7) ]
    possibleLines += [[(i, j) for j in range(2, 6)]  for i in range(0, 7) ]
    
    possibleLines += [ [(i, i) for i in range(0, 4)], [(i, i+1) for i in range(0, 4)], [(i, i+2) for i in range(0, 4)] ] # les 24 façons de gagner en diagonales : 3 par lignes
    possibleLines += [ [(i, i-1) for i in range(1, 5)], [(i, i) for i in range(1, 5)], [(i, i+1) for i in range(1, 5)] ]
    possibleLines += [ [(i, i-2) for i in range(2, 6)], [(i, i-1) for i in range(2, 6)], [(i, i) for i in range(2, 6)] ]
    possibleLines += [ [(i, i-3) for i in range(3, 7)], [(i, i-2) for i in range(3, 7)], [(i, i-1) for i in range(3, 7)] ]
    
    possibleLines += [ [(5-i, i) for i in range(5, 1, -1)], [(4-i, i) for i in range(4, 0, -1)], [(3-i, i) for i in range(3, -1, -1)] ] 
    possibleLines += [ [(6-i, i) for i in range(5, 1, -1)], [(5-i, i) for i in range(4, 0, -1)], [(4-i, i) for i in range(3, -1, -1)] ]
    possibleLines += [ [(7-i, i) for i in range(5, 1, -1)], [(6-i, i) for i in range(4, 0, -1)], [(5-i, i) for i in range(3, -1, -1)] ]
    possibleLines += [ [(8-i, i) for i in range(5, 1, -1)], [(7-i, i) for i in range(4, 0, -1)], [(6-i, i) for i in range(3, -1, -1)] ]

    """ Constructeur de la classe, pour initialiser les variables """
    def __init__(self):
        self.grid = [ [None]*6 for i in range(0, 7) ]
        self.highPlayed = [6]*7
        self.hasWon = None
        self.winningLine = None
        self.nbRemainingMoves = 42
        self.lastPlayed = None
        self.hasUndo = False

    def play(self, player, colonne):
        """Joue un coup pour <player> dans la colonne <x>
        Parametres: 
        player : 
          un identifiant du joueur
        x: int
        
        Lève Exception si la position a déjà été jouée.
        Renvoie l'identifiant du gagnant s'il existe après ce coup, None sinon.
        """
        self.hasUndo = False
        
        if colonne >= 7:
            raise Exception
        
        ligne=self.highPlayed[colonne]-1
            
        if self.grid[colonne][ligne]:
            raise Exception

        if self.canBePlayed(colonne):
            self.grid[colonne][ligne] = player
            self.lastPlayed = [(colonne,ligne)]
            self.highPlayed[colonne] -= 1
            self.nbRemainingMoves -= 1
            return self.winner()

    def canBePlayed(self, colonne):
        """Renvoie True si la colonne <x> est jouable, False sinon."""
        
        ligne=self.highPlayed[colonne]-1
        return not self.grid[colonne][ligne]
    
    def undo(self):
        """Revient au coup précédent."""
        if self.hasUndo:
            return
        self.hasUndo = True
        colonne = self.lastPlayed[0][0]
        ligne = self.lastPlayed[0][1]
        self.grid[colonne][ligne] = None
        self.highPlayed[colonne] += 1
        self.nbRemainingMoves += 1
    
    def winner(self):
        """Renvoie l'identifiant du gagnant s'il existe, None sinon. """
        if(self.hasWon):
            # Si on connait déjà le gagnant, on le renvoie
            return self.hasWon
        # Sinon on vérifie s'il y a un gagnant
        for line in self.possibleLines:
            present = set(self.grid[colonne][ligne] for (colonne, ligne) in line)
            if len(present) == 1:
                w = present.pop()
                if w:
                    self.winningLine = line
                    self.hasWon = w
                    return w
        return None

    def isTie(self):
        """Renvoie True si la partie s'est terminé sur un match nul."""
        return not self.winner() and not self.nbRemainingMoves
    
    def getCell(self, ligne, colonne):
        """Renvoie l'identifiant du joueur qui a joué en position <x, y>, 
           None si personne n'y a joué.
        """
        return self.grid[colonne][ligne]

    def setCell(self, ligne, colonne, valeur):
        """Change l'identifiant du joueur qui a joué en position <x, y>
        en lui affectant la valeur <v>.
        
        Attention, l'utilisation de cette méthode risque de rendre
        l'état de la partie incohérent. Pour jouer un coup, utiliser play()
        """
        self.grid[colonne][ligne] = valeur
    
    def playerSymbol(self, player):
        """Renvoie le symbole du joueur dont l'identifiant est <player>.
        Utilise les entiers 1 et 2 pour identifier les joueurs, ou
        None pour "aucun joueur". 
        """
        if player == 1:
            return "O"
        elif player == 2:
            return "X"
        else:
            assert(player == None)
            return " "
        
    def textDisplay(self):
        """Affiche l'état de la partie (en mode texte) dans le terminal."""
        print("\n- - - - - - -\n".join("|".join(self.playerSymbol(self.grid[i][j]) for i in range(0, 7)) for j in range(0, 6)))

    def displayWinner(self):
        """Affiche le gagnant de la partie dans le terminal."""
        w = self.winner()
        if w:
            if self.playerSymbol(w)=='O':
                print("The winner is: O")
            else:
                print("The winner is: X")
        else:
            print("The game continues...")
            
    def copyGame(self):
        """Créer une nouvelle partie avec l'état du jeu actuel."""
        copy = GameState()
        copy.grid = self.grid
        copy.highPlayed = self.highPlayed
        copy.hasWon =self.hasWon
        copy.winningLine = self.winningLine
        copy.nbRemainingMoves = self.nbRemainingMoves
        copy.lastPlayed = self.lastPlayed
        copy.hasUndo = self.hasUndo
        return copy

# Quelques tests pour s'assurer que tout cela fonctionne correctement
if __name__ == "__main__":
    
    state = GameState()
    state.play(1,3)
    state.play(2,3)
    state.textDisplay()
    state.displayWinner()
    state.undo()
    state.textDisplay()
    print("copy")
    copystate=state.copyGame()
    copystate.textDisplay()