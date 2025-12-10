"""
Programme basique en python3.8 permettant via matplolib de visualiser une grille hexagonale.

Elle propose simplement:
 - l'affichage des hexagones, avec des couleurs et une opacité
 - l'ajout de formes colorées sur les hexagones
 - l'ajout de liens colorés entre les hexagones

Contact: sebastien.gamblin@isen-ouest.yncrea.fr
"""



#Enlève les "" des objet qu'on peut avoir
from __future__ import annotations

#Permet la création de classes abstraites & méthodes abstraites
from abc import abstractmethod

#Permet d'initialiser une valeur par défault pour des clés qui n'ont pas été définies
from collections import defaultdict

#Intégration du hasard
import random

#Importations basiques de python pour inclure dictionnaire, tuples, et des listes
from typing import Dict, Tuple, List

#Visualisation de données / dessins / graphiques
import matplotlib.pyplot as plt

#Importations des couleurs avec une précision
import matplotlib.colors as mcolors

#Importations de polygones régulier
from matplotlib.patches import RegularPolygon

#Gère propriétés de style par rapport aux formes
from matplotlib.patches import Patch

#Crée des palets de couleur spécifiques
from matplotlib.colors import LinearSegmentedColormap

#Calculs numériques & tableaux de données 
import numpy as np

#Importer la dequeue en python
from collections import deque

# un simple alias de typage python : type (x,y)
Coords = Tuple[int, int]  

# il y a mieux en python :
# - 3.11: Coords: AliasType = Tuple[int, int]
# - 3.12: type Coords = Tuple[int, int]


class Forme:
    """Superclasse abstraite qui sauvegarde une couleur et impose une méthode 'get' qui retourne un Patch."""

    def __init__(self, color: str = "black", edgecolor: str = None):
        assert color in mcolors.CSS4_COLORS #vérification de la couleur donné
        if edgecolor is not None:
            assert edgecolor in mcolors.CSS4_COLORS #vérification de la couleur de bordure donné
        #Affectation
        self._color = color
        self._edgecolor = edgecolor


    #Méthode get qui impose un Patch en retour
    @abstractmethod
    def get(self, x: float, y: float, h: int) -> Patch:
        pass


class Rect(Forme):
    """Redéfinition d'une Forme pour un rectangle."""

    def __init__(self, *args, **kwargs): #* arguments possible dans un tuple, ** argument possibles dans un dictionnaire
        super().__init__(*args, **kwargs) #Super constructeur de la classe forme

    def get(self, x: float, y: float, h: int) -> plt.Rectangle: #Méthode get : rectangle
        #plt.Rectangle(cordonnées de création,taille,couleur,couleur des bordures)
        return plt.Rectangle((x - h / 2, y - h / 2), h, h, facecolor=self._color, edgecolor=self._edgecolor)


class Circle(Forme):
    """Redéfinition d'une Forme pour un cercle."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, x: float, y: float, h: int) -> plt.Circle:
        #plt.Circle(cordonnées de création, taille, couleur, couleur des bordures)
        return plt.Circle((x, y), h / 2, facecolor=self._color, edgecolor=self._edgecolor)


class HexGridViewer:
    """
    Classe permettant d'afficher une grille hexagonale. Elle se crée via son constructeur avec deux arguments:
    la largeur et la hauteur.
    Deux attributs gèrent l'apparence des hexagones: colors et alpha, pour respectivement représenter la
    couleur et la transparence des hexagones.
    Chaque hexagone est représenté par une tuple : (x, y) spécifique dans la grille. 
    Ces tuples sont les clés des dictionnaires colors et alpha, que vous pouvez modifier via les méthodes add_color et add_alpha.

    Il est aussi possible d'ajouter des symboles Rectangle ou Circle au milieu des hexagones, ainsi que des liens
    entre les centres des hexagones.

    Pour s'informer sur les HexGrid:
    Voir : https://www.redblobgames.com/grids/hexagons/#coordinates-offset pour plus d'informations.
    """

    def __init__(self, width: int, height: int):

        self.__width = width  # largueur de la grille hexagonale, i.e. ici "nb_colonnes"
        self.__height = height  # hauteur de la grille hexagonale, i.e. ici "nb_lignes"

        # modifié par défaut par matplolib, la modification ne sert à rien
        # mais est nécessaire pour calculer les points
        self.__hexsize = 10

        # couleur des hexagones : par défaut, blanc
        #Lorsqu'on accède à une coordonnée qui n'a pas de couleur affecté, ce sera blanc
        self.__colors: Dict[Coords, str] = defaultdict(lambda: "white")

        # transparence des hexagones : par défaut, 1
        #De même que les couleurs
        self.__alpha: Dict[Coords, float] = defaultdict(lambda: 1)

        # symboles sur les hexagones, par défaut, aucun symbole sur une case.
        # Limitation : un seul symbole par case !
        #Le symbole est soit une forme ou soit None
        self.__symbols: Dict[Coords, Forme | None] = defaultdict(lambda: None)

        # liste de liens à affichager entre les cases.
        self.__links: List[Tuple[Coords, Coords, str, int]] = []

        #Elements du terrain
        self.__ground = {
            "herbe" : "limegreen",
            "montagne" : "darkgrey",
            "route" : "wheat",
            "eau" : "dodgerblue" 
        }

        #Altitudes du terrain
        self.__altitude: Dict[Coords, int] = defaultdict(lambda: 1)

    #Retourne la largeur
    def get_width(self) -> int:
        return self.__width

    #Retour la longueur
    def get_height(self) -> int:
        return self.__height

    #Ajouter une couleur en vérifiant qu'elle existe bien dans mcolors
    def add_color(self, x: int, y: int, color: str) -> None:
        assert self.__colors[(x, y)] in mcolors.CSS4_COLORS, \
            f"self.__colors type must be in matplotlib colors. What is {self.__colors[(x, y)]} ?"
        self.__colors[(x, y)] = color

    #Ajouter un indice alpha à des coordonnées 
    def add_alpha(self, x: int, y: int, alpha: float) -> None:
        assert 0 <= self.__alpha[
            (x, y)] <= 1, f"alpha value must be between 0 and 1. What is {self.__alpha[(x, y)]} ?"
        self.__alpha[(x, y)] = alpha

    #Ajouter un symbole à des coordonnées
    def add_symbol(self, x: int, y: int, symbol: Forme) -> None:
        self.__symbols[(x, y)] = symbol

    #Ajoute un lien entre deux cases, soit 4 coordonnées
    def add_link(self, coord1: Coords, coord2: Coords, color: str = None, thick=2) -> None:
        self.__links.append((coord1, coord2, color if color is not None else "black", thick))

    #Obtient la couleur de coordonnées précise
    def get_color(self, x: int, y: int) -> str:
        return self.__colors[(x, y)]

    #Obtient l'alpha de coordonnées précise
    def get_alpha(self, x: int, y: int) -> float:
        return self.__alpha[(x, y)]

    #Obtient tout les voisins d'une case hexagone renvoie une liste de coordonnées [(x,y),(x,y)]
    def get_neighbours(self, x: int, y: int) -> List[Coords]:

        """
        Retourne la liste des coordonnées des hexagones voisins de l'hexagone en coordonnées (x,y).
        """


        if y % 2 == 0:
            #Cas ou y est paire, res [(2,0)...]
            res = [(x + dx, y + dy) for dx, dy in ((1, 0), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1))]
        else:
            #Cas ou y est impaire
            res = [(x + dx, y + dy) for dx, dy in ((1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (1, -1))]
            #Return des voisins en vérifiant qu'ils sont bien dans les limites 
        return [(dx, dy) for dx, dy in res if 0 <= dx < self.__width and 0 <= dy < self.__height]

    #Ajouter une altitude a des coordonnées
    def add_altitude(self, x: int, y:int, alt) -> None:
        if 1 <= alt <= 12:
            self.__altitude[(x,y)] = alt
            self.update_color_altitude(x,y)
        else :
            print("The altitude is too big\n")

    #Get the altitude
    def get_altitude(self, x:int, y:int) -> int:
        return self.__altitude[(x,y)]

    #Add the color of the ground based on the altitude
    def update_color_altitude(self, x:int, y:int) -> None:
        """
        Scale based on 100
        ->  4,12,6 : water
        ->  2,7,8 : grass
        ->  1,11,9 : path
        ->  3,5,10 : moutain
        """
        altitude = self.get_altitude(x,y)
        if  altitude == 4 or altitude == 12 or altitude == 6:
            color = self.__ground["eau"]
        elif altitude == 2 or altitude == 7 or altitude == 8 :
            color = self.__ground["herbe"]
        elif altitude == 1 or altitude == 11 or altitude == 9 :
            color = self.__ground["route"]
        elif altitude == 3 or altitude == 5 or altitude == 10:
            color = self.__ground["montagne"]
        if color is not None:
            self.__colors[(x,y)] = color

    #Implementation of the BFs on the graph based on the coords and distance
    def Bfs(self,case_depart: Coords, distance: int) -> List[Coords]:
        file = deque([(case_depart,0)])
        visites = {case_depart: 0}
        cases_pardistance = {}

        while file:
            (x,y), dist = file.popleft()

            if dist not in cases_pardistance:
                cases_pardistance[dist] = []
            cases_pardistance[dist].append((x,y))

            if dist < distance :
                for vx, vy in self.get_neighbours(x,y):
                    if (vx,vy) not in visites :
                        visites[(vx,vy)] = dist+1
                        file.append(((vx,vy), dist+1))
        #print(cases_pardistance)
        return cases_pardistance
    
    def highest_altitude(self) -> Coords:
        pass
        
                


    def show(self, alias: Dict[str, str] = None, debug_coords: bool = False) -> None:
        """
        Permet d'afficher via matplotlib la grille hexagonale. 
        :param alias: dictionnaire qui permet de modifier le label d'une couleur. Ex: {"white": "snow"} 
        :param debug_coords: booléen pour afficher les coordonnées des
        cases. 
        Attention, le texte est succeptible de plus ou moins bien s'afficher en fonction de la taille de la
        fenêtre matplotlib et des dimensions de la grille.
        """
        #Modifier le label d'une couleur
        if alias is None:
            alias = {}

        #Crée une figure carré de 8x8 et un axe de 8 sur 8
        fig, ax = plt.subplots(figsize=(8, 8))

        #Permettre que l'axe x et y soient pareille        
        ax.set_aspect('equal')

        #Hauteur de la taille du hexsize prédfini
        h = self.__hexsize

        #Définition du dictionnaire des coordonnées
        coords = {}

        #Création de la grille hexagonale en Flatop
        for row in range(self.__height):
            for col in range(self.__width):
                x = col * 1.5 * h #1,5 fois la taille * la hauteur de 10
                y = row * np.sqrt(3) * h #racine de 3 fois la colonne

                #Colonne impaire
                if col % 2 == 1:
                    #Ajout d'un petit décalage pour faire une grille hexgonale
                    y += np.sqrt(3) * h / 2

                #Association colonnes et coordonnées 
                coords[(row, col)] = (x, y)

                #Définition du centre
                center = (x, y)

                #Création du polygone = hexagone en radian
                hexagon = RegularPolygon(center, numVertices=6, radius=h, orientation=np.pi / 6, edgecolor="black")

                #Mettre les couleurs en fonction de celle prédéfini
                hexagon.set_facecolor(self.__colors[(row, col)])

                #De même pour le alpha
                hexagon.set_alpha(self.__alpha[(row, col)])

                # Ajoute du texte à l'hexagone
                #if debug_coords:
                #    text = f"({row}, {col})"  # Le texte que vous voulez afficher
                #    ax.annotate(text, xy=center, ha='center', va='center', fontsize=8, color='black')

                # ajoute l'hexagone
                ax.add_patch(hexagon)

                # gestion des Formes additionnelles
                forme = self.__symbols[(row, col)]
                if forme is not None:
                    ax.add_patch(forme.get(x, y, h))

        for coord1, coord2, color, thick in self.__links:
            #Vérifié si deux cases ne sont pas déja connecté
            if coord1 not in coords or coord2 not in coords:
                continue
            x1, y1 = coords[coord1]
            x2, y2 = coords[coord2]
            #Liaison entre deux case
            plt.gca().add_line(plt.Line2D([x1, x2], [y1, y2], color=color, linewidth=thick))

        ax.set_xlim(-h, self.__width * 1.5 * h + h)
        ax.set_ylim(-h, self.__height * np.sqrt(3) * h + h)
        ax.axis('off')

        ks, vs = [], []
        for color in set(self.__colors.values()):
            if color in alias:
                ks.append(alias[color])
            else:
                #légende
                ks.append(color)
            #couleur
            vs.append(color)

        #Création de la légende couleur/ terrain
        gradient_cmaps = [
            LinearSegmentedColormap.from_list('custom_cmap', ['white', vs[i]]) for i in range(len(vs))]
        
        # Créez une liste de patch à partir des polygones
        legend_patches = [
            Patch(label=ks[i], edgecolor="black", linewidth=1, facecolor=gradient_cmaps[i](0.5), )
            for i in range(len(ks))]
        
        # Ajoutez la légende à la figure
        ax.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()



def main():
    """
    Fonction exemple pour présenter le programme ci-dessus.
    """
    size = 17
    center = (size-1)/2
    # CREATION D'UNE GRILLE TAILLE SIZE
    hex_grid = HexGridViewer(size, size)

    for i in range(17):
        for j in range (17):
            hex_grid.add_altitude(i,j,random.randint(1,12))

    #Implémentation BFS
    #result = hex_grid.Bfs((center,center),3)
    #colors = ["red","orange","yellow","green"]
    #for dist, cases in result.items():
    #    for x,y in cases:
    #        if dist < len(colors):
    #            hex_grid.add_color(x,y,colors[dist])

    

    # MODIFICATION DE LA COULEUR D'UNE CASE
    # hex_grid.add_color(X, Y, color) où :
    # - X et Y sont les coordonnées de l'hexagone et color la couleur associée à cet hexagone.
    #hex_grid.add_color(5, 5, "purple")
    #hex_grid.add_color(1, 0, "red")

    # MODIFICATION DE LA TRANSPARENCE D'UNE CASE
    # hex_grid.add_alpha(X, Y, alpha) où :
    # - X et Y sont les coordonnées de l'hexagone et alpha la transparence associée à cet hexagone.
    #hex_grid.add_alpha(5, 5, 0.7)

    # RECUPERATION DES VOISINS D'UNE CASE : ils sont entre 2 et 6.
    # hex_grid.get_neighbours(X, Y)

    #for _x, _y in hex_grid.get_neighbours(5, 5):
    #    hex_grid.add_color(_x, _y, "blue")
    #    hex_grid.add_alpha(_x, _y, random.uniform(0.2, 1))

    #for _x, _y in hex_grid.get_neighbours(1, 0):
    #    hex_grid.add_color(_x, _y, "pink")
    #    hex_grid.add_alpha(_x, _y, random.uniform(0.2, 1))

    # AJOUT DE SYMBOLES SUR LES CASES : avec couleur et bordure
    # hex_grid.add_symbol(X, Y, FORME)
    #    hex_grid.add_symbol(10, 8, Circle("red"))
    #    hex_grid.add_symbol(9, 8, Rect("green"))
    #    hex_grid.add_symbol(3, 4, Rect("pink", edgecolor="black"))

    # AJOUT DE LIENS ENTRE LES CASES : avec couleur
    #hex_grid.add_link((5, 5), (6, 6), "red")
    #hex_grid.add_link((8, 8), (7, 8), "purple", thick=4)

    # AFFICHAGE DE LA GRILLE
    # alias permet de renommer les noms de la légende pour des couleurs spécifiques.
    # debug_coords permet de modifier l'affichage des coordonnées sur les cases.
    hex_grid.show(alias={"dodgerblue": "water", "limegreen": "grass", "darkgrey": "moutain", "wheat" : "path"}, debug_coords=True)





#Eviter d'éxécuter tout le code de la page si le fichier est importer
if __name__ == "__main__":
    main()

#Question 1 :
#Déjà faites avec le code qui est donné

#Question 2 :
#Labeliser un sommet par un type de terrain : (herbe,montagne,route,eau)
#Labeliser par une altitude : donc pour chaque coordonnée elle a une altitude prédéfinie pour laquel on associe un terrain
#On update la couleur en fonction du terrain

#Question 3 :
#Test des implémentations qu'on a pu faire

#Question 4 :
#Algorithme BFS et on l'adapte avec une distance au préhalable sur laquel on colorie dans le main

#Question 5 :
#a) On

