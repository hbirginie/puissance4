#!/usr/bin/env python3

from GameState import *
import sys

# goal : int
# le nombre de parties gagnantes à atteindre pour terminer le jeu
# peut être fourni en ligne de commande, valeur par défaut: 5
goal = int(sys.argv[1]) if len(sys.argv) >= 2 else 5

def inputStringToMove(str):
    """Convertit une chaîne de caractères donnée par l'utilisateur en position à jouer
    
    Format attendu: un entier
    Renvoit None si l'entrée est invalide.
    """
    try:
        words = [w for w in str.split(" ") if w]
        if len(words) > 1:
            return None
        x = int(words[0])
        if x in range(0, 7):
            return x
        return None
    except Exception:
        return None

# Variables pour stocker l'état actuel du jeu
winner = None
game = GameState()
currentPlayer = 1
scores = [0, 0]
lastStarter = 1

# Boucle principale: afficher le jeu, demander un coup, le jouer s'il
# est valide En cas de victoire, relancer une partie si le nombre de
# victoires n'est pas atteint.
while True:
    game.textDisplay()
    print("%s: %d wins, %s: %d wins" % (game.playerSymbol(1), scores[0],
                                        game.playerSymbol(2), scores[1]))
    try:
        move = None
        while move is None:
            string = input("Player %s: your move? " % game.playerSymbol(currentPlayer))
            move = inputStringToMove(string.strip())
            if move is None:
                print("Incorrect entry! Expected format: <x>, from 0 to 6.")
            elif not game.canBePlayed(move):
                print("Invalid move!")
                move = None
        w = game.play(currentPlayer, move)
        currentPlayer = 3-currentPlayer
        if w:
            print("Player %s wins!" % game.playerSymbol(w))
            scores[w-1] += 1
            if scores[w-1] >= goal:
                print("Congratulations Player %s !" % game.playerSymbol(w))
                exit(0)
            game = GameState()
            lastStarter = 3 - lastStarter
            currentPlayer = lastStarter
    except EOFError:
        print("Game ended prematurely. Current state:")
        game.textDisplay()
        exit(0)
        