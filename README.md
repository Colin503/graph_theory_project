# graph_theory_project
graph theory project during my S5 at ISEN

# Réponses aux questions :
    ** 1 -  Proposez une implémentation d’un graphe, qui représente une grille hexagonale et qui possède toutes les propriétés d’un graphe.**

    Comme il nous ai déjà donné on utilise la représentation en grille hexagonale.


    ** 2 -  Proposez une extension de cette implémentation, permettant :  de labeliser les sommets par un type de terrain de votre choix (herbe, montagne, route, eau,etc...) **

    On ajoute un attribut altitude dans la classe HexGridViewer, avec une variable d'altitude maximale et minimale.
    Depuis ces altitudes chaque case est déterminé avec un terrain spécifique en fonction de l'altitude qu'elle a reçu


    ** 3 Tester ce programme en ajoutant des types de terrain aléatoire et des altitudes aléatoires.
        Vous pouvez afficher le résultat grâce au programme hexgrid_viewer.py, en utilisant les couleurs
        pour signifier les terrains et la transparence pour signifier l’altitude **
    
    On compile et on observe.

    ** 4  Quel algorithme utiliser pour générer une zone régulière qui s’étend sur la carte (i.e. toutes
        les cases à distance i d’une case) et comment l’adapter ? Implémentez-le **
        
        On va utiliser l'algorithm BFS (Breath First Search qui cherche toute les zones autour), avec une distance mise au préhalable

    ** 5 a - créer une méthode permettant de trouver le sommet le plus haut de votre carte. **
        On parcoure l'attribut altitude et exécute une boucle dessus pour trouver le plus grand

        b - Quel algorithme permettrait de tracer des rivières à partir d’un point donné sur la carte, en
        ajoutant une contrainte d’altitude descendante en prenant le chemin le plus long possible ?

        On utilise l'algorithme DFS (Depth first Search, qui va suivre un chemin qu'on lui propose)

        c - Que pouvez-vous ajoutez pour créer des embranchements de rivières ? Quelle est cette structure obtenue ?

        TOUS les voisins valides au lieu de prendre seulement le chemin le plus bas. Soit la structure obtenue est un arbre, ou un graphe acyclique orienté

    ** 6 Proposez maintenant un algorithme, qui, s’inspirant des deux prédécedents, génère une carte aléatoirement, de sorte à ce que les altitudes soient "logiques" et que les types de terrains aient une cohérence, avec des rivières.
    Extension bonus : l’eau peut ne pas être une rivière, par exemple, avec les lacs Quelle contrainte cela ajoute au programme ? Comment faire ?
