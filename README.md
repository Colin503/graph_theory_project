# graph_theory_project
Projet de théorie des Graphes : Semestre 5

## Réponses aux questions :

### 1 -  Proposez une implémentation d’un graphe, qui représente une grille hexagonale et qui possède toutes les propriétés d’un graphe. 

Nous utilisons une grille hexagonale pour la représentation du graphe.

### 2 -  Proposez une extension de cette implémentation, permettant :  de labeliser les sommets par un type de terrain de votre choix (herbe, montagne, route, eau,etc...)

    On ajoute un attribut altitude dans la classe HexGridViewer, avec une variable d'altitude maximale et minimale.
    Depuis ces altitudes chaque case est déterminé avec un terrain spécifique en fonction de l'altitude qu'elle a reçu

### 3 - Tester ce programme en ajoutant des types de terrain aléatoire et des altitudes aléatoires. 

        On teste notre programme main.py, on le compile et on observe, avec une génération aléatoire du terrain.
    


### 4 - Quel algorithme utiliser pour générer une zone régulière qui s’étend sur la carte (i.e. toutes les cases à distance i d’une case) et comment l’adapter ? Implémentez-le 
        
        On va utiliser l'algorithm BFS (Breath First Search qui cherche toute les zones autour), avec une distance mise au préhalable. Avec des couleurs définies pour chaque distance

### 5 a - créer une méthode permettant de trouver le sommet le plus haut de votre carte. **
On parcoure l'attribut altitude et exécute une boucle dessus pour trouver le plus grand

### b - Quel algorithme permettrait de tracer des rivières à partir d’un point donné sur la carte, en ajoutant une contrainte d’altitude descendante en prenant le chemin le plus long possible ?

        On utilise l'algorithme DFS (Depth first Search, qui va suivre un chemin qu'on lui propose)

### c - Que pouvez-vous ajoutez pour créer des embranchements de rivières ? Quelle est cette structure obtenue ?

    TOUS les voisins valides au lieu de prendre seulement le chemin le plus bas. Soit la structure obtenue est un arbre, ou un graphe acyclique orienté

### 6 Proposez maintenant un algorithme, qui, s’inspirant des deux prédécedents, génère une carte aléatoirement, de sorte à ce que les altitudes soient "logiques" et que les types de terrains aient une cohérence, avec des rivières. Extension bonus : l’eau peut ne pas être une rivière, par exemple, avec les lacs Quelle contrainte cela ajoute au programme ? Comment faire ?
