# Puissance4

## Documentation utilisateur

Pour le mode texte (TextMode), il suffit d'écrire dans la console un entier entre 0 et 6. Le joueur qui doit jouer est marqué dans la console. A la fin de la partie le score est comptabilisé. Si égalité, le score ne change pas. Le premier à 5 est le gagnant.

```
 | | | | | | 
- - - - - - -
 | | | | | | 
- - - - - - -
 | | | | | | 
- - - - - - -
 | | | | | | 
- - - - - - -
 | | | | | | 
- - - - - - -
 | | | | | | 
O: 0 wins, X: 0 wins
Player O: your move? 
```

Pour le mode graphique (tkGraphicMode), il suffit de cliquer sur les flèches de couleurs en haut du jeu. Chaque flèche correspond à une colonne. Le jeton va être inséré le plus bas possible. La couleur indiquée en haut correspond à la couleur du jeton qui va être joué. A la fin de la partie le score est comptabilisé. Si égalité, le score ne change pas. A tout moment le jeu peut être réinitialisé. Une fonction undo est disponible pour annuler le dernier coup. Ces deux fonctionnalitées sont disponible dans l'onglet Main en haut à gauche de la fenêtre.

[Mode graphique au début de la partie](https://ibb.co/7Gqjd0S)

Pour le mode graphique contre l'ordinateur (tkGraphicModeBot), il suffit de cliquer sur les flèches de couleurs en haut du jeu. Chaque flèche correspond à une colonne. Le jeton va être inséré le plus bas possible. Vous êtes le joueur jaune et l'ordinateur est le joueur rouge. Il jouera instantanément après votre coup joué. A la fin de la partie le score est comptabilisé. Si égalité, le score ne change pas. A tout moment le jeu peut être réinitialisé. Cette fonctionnalitée est disponible dans l'onglet Main en haut à gauche de la fenêtre.

[Exemple d'une partie contre l'ordinateur](https://ibb.co/d4Lb1J0)

## Documentation développeur

Le code du puissance4 est répartie en 4 fichiers :

*Gamestate.py*

Ce fichier contient la classe Gamestate qui contient toutes les informations sur l'état d'une partie.

*TextMode.py*

Ce fichier contient le code pour l'affichage du jeu dans la console.

*tkGraphicMode.py*

Ce fichier contient le code pour l'affichage graphique du jeu. La partie graphique est codée avec tkInter.

*tkGraphicModeBot.py*

Ce fichier contient le code pour l'affichage graphique du jeu. La partie graphique est codée avec tkInter. Ce fichier contient aussi l'implémentation du bot.

Résumé de l'algorithme du bot :

Premier algorithme : regarder si le bot peut gagner au prochain coup
```
pour chaque colonne :
    si le bot peut jouer dans cette colonne :
        faire jouer le bot
        si il y a un gagnant :
            retenir cette colonne comme coup gagnant
        annuler le coup du bot
```
Le bot va alors jouer dans cette colonne pour gagner.

Deuxième algorithme : regarder si le bot peut perdre au prochain coup
```
pour chaque colonne :
    si le joueur peut jouer dans cette colonne :
        faire jouer le joueur
        si il y a un gagnant :
            retenir cette colonne comme coup perdant
        annuler le coup du joueur
```
Le bot va alors jouer dans cette colonne pour éviter de perdre au prochain tour.

Le bot contient d'autres algorithmes dont l'un qui regarde si un coup est perdant à 2 coups d'avance.