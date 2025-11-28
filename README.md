# graph_theory_project
graph theory project during my S5 at ISEN

# Réponses aux questions :
    ** 1 -  Proposez une implémentation d’un graphe, qui représente une grille hexagonale et qui possède toutes les propriétés d’un graphe.**

    On va se tourner vers une liste de sucesseurs car un hexagone contient 6 côtés il a donc 6 voisins (sucesseurs) pour les algos.
    Une matrice d'adjacence aurait été un peu grossse |S^2| en taille ce qui peut faire beaucoup pour notre graphe.
    Sinon on va utiliser une grille pour représenter le graphe.


    ** 2 -  Proposez une extension de cette implémentation, permettant :  de labeliser les sommets par un type de terrain de votre choix (herbe, montagne, route, eau,etc...) **

    Dictionnaire d'un élément du terrain avec sa couleur : "sand" : jaune


    **Labéliser les sommets par une altitude **
    L'altitude qui est défini à 0 et qui est update en fonction du choix du terrain avec sa couleur

    ** 3 Tester ce programme en ajoutant des types de terrain aléatoire et des altitudes aléatoires.
        Vous pouvez afficher le résultat grâce au programme hexgrid_viewer.py, en utilisant les couleurs
        pour signifier les terrains et la transparence pour signifier l’altitude **
    
    Test

    ** 4  Quel algorithme utiliser pour générer une zone régulière qui s’étend sur la carte (i.e. toutes
        les cases à distance i d’une case) et comment l’adapter ? Implémentez-le **
        
        On va utiliser l'algorithme diamond square, génération de fractales etc...
        Obligation d'avoir des côtés de 2**n+1 pour pouvoir le faire marcher
        Meilleure solution faire d'abord l'algorithm sur un carré et application ensuite sur les hexagones