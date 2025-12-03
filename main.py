#Projet - Théorie des graphes
# ISEN - S5
# Auteur : Colin Rousseau & Gaspard Vieujean

"""=====================================Importation des librairies nécessaires====================================="""
from __future__ import annotations

from abc import abstractmethod
from collections import defaultdict

import random
from typing import Dict, Tuple, List

import matplotlib.colors as mcolors
from matplotlib.patches import RegularPolygon
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

"""==============================================================================================================="""

Coords = Tuple[int, int]  # un simple alias de typage python

"""======================================Défintion des classes géométriques======================================"""

class Forme:
    """Superclasse abstraite qui sauvegarde une couleur et impose une méthode 'get' qui retourne un Patch."""

    def __init__(self, color: str = "black", edgecolor: str = None):
        assert color in mcolors.CSS4_COLORS #vérification que la couleur est bien valide
        if edgecolor is not None:
            assert edgecolor in mcolors.CSS4_COLORS #vérification que la couleur est bien valide
        self._color = color
        self._edgecolor = edgecolor

    @abstractmethod
    def get(self, x: float, y: float, h: int) -> Patch:
        pass


class Rect(Forme):
    """Redéfinition d'une Forme pour un rectangle."""

    def __init__(self, *args, **kwargs): # *args et **kwargs quand on cherche a récupérer des arguments non spécifiés
        super().__init__(*args, **kwargs)

    def get(self, x: float, y: float, h: int) -> plt.Rectangle:
        """Retourne un Patch rectangle centré en (x,y) de hauteur h.""" 
        return plt.Rectangle((x - h / 2, y - h / 2), h, h, facecolor=self._color, edgecolor=self._edgecolor)
    
class Circle(Forme):
    """Redéfinition d'une Forme pour un cercle."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, x: float, y: float, h: int) -> plt.Circle:
        """Retourne un Patch cercle centré en (x,y) de rayon h/2."""
        return plt.Circle((x, y), h / 2, facecolor=self._color, edgecolor=self._edgecolor)



"""=====================================Définition de la classe HexGridViewer======================================"""

class HexGridViewer:
    """
    Classe permettant d'afficher une grille hexagonale. Elle se crée via son constructeur avec deux arguments: la largeur et la hauteur.
    Deux attributs gèrent l'apparence des hexagones: colors et alpha (couleur, transparence).
    Chaque hexagone est représenté par une tuple : (x, y) spécifique dans la grille. Ces tuples sont les clés
    des dictionnaires colors et alpha, que vous pouvez modifier via les méthodes add_color et add_alpha.

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
        
        # Dictionnaire des éléments du terrain (couleurs CSS valides)
        # On conserve uniquement : water, sand, grass, forest, mountain
        self.terrain: Dict[str, str] = {
            "water": "blue",
            "sand": "yellow",
            "grass": "yellowgreen",
            "forest": "darkgreen",
            "mountain": "gray",
        }

        # couleur des hexagones : par défaut, blanc
        #self.__colors: Dict[Coords, str] = defaultdict(lambda: self.terrain["forest"])
        self.__colors: Dict[Coords, str] = defaultdict(lambda: "white")

        #Altitude des éléments du terrain : par défaut, 0.0 niveau de la mer
        #Altitude Max : 500(montagne)
        self.altitude: Dict[Coords, int]= defaultdict(lambda: 0)

        # transparence des hexagones : par défaut, 1
        self.__alpha: Dict[Coords, float] = defaultdict(lambda: 1)

        # symboles sur les hexagones, par défaut, aucun symbole sur une case.
        # Limitation : un seul symbole par case !
        self.__symbols: Dict[Coords, Forme | None] = defaultdict(lambda: None)

        # liste de liens à affichager entre les cases.
        self.__links: List[Tuple[Coords, Coords, str, int]] = []

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height

    def add_color(self, x: int, y: int, color: str) -> None:
        assert self.__colors[(x, y)] in mcolors.CSS4_COLORS, \
            f"self.__colors type must be in matplotlib colors. What is {self.__colors[(x, y)]} ?"
        self.__colors[(x, y)] = color

    def add_alpha(self, x: int, y: int, alpha: float) -> None:
        assert 0 <= self.__alpha[
            (x, y)] <= 1, f"alpha value must be between 0 and 1. What is {self.__alpha[(x, y)]} ?"
        self.__alpha[(x, y)] = alpha

    def add_symbol(self, x: int, y: int, symbol: Forme) -> None:
        self.__symbols[(x, y)] = symbol

    def add_link(self, coord1: Coords, coord2: Coords, color: str = None, thick=2) -> None:
        self.__links.append((coord1, coord2, color if color is not None else "black", thick))

    def get_color(self, x: int, y: int) -> str:
        return self.__colors[(x, y)]

    def get_alpha(self, x: int, y: int) -> float:
        return self.__alpha[(x, y)]
    
    
    def update_color_from_altitude(self, x: int, y: int, alt: int) -> None:
        """
        Définit la couleur en fonction de l'altitude (valeurs en mètres, 0-500).

        Seuils ajustés pour réduire la proportion d'eau :
        - 0   - 40  : water (blue)
        - 41  - 80  : sand (yellow)
        - 81  - 220 : grass (yellowgreen)
        - 221 - 380 : forest (darkgreen)
        - 381 - 500 : mountain (gray)
        """
        # Clamp altitude to expected range
        alt = max(0, min(int(alt), 500))

        if alt <= 40:
            terrain_type = "water"
        elif alt <= 80:
            terrain_type = "sand"
        elif alt <= 220:
            terrain_type = "grass"
        elif alt <= 380:
            terrain_type = "forest"
        else:
            terrain_type = "mountain"

        # Appliquer la couleur si elle est définie
        color = self.terrain.get(terrain_type)
        if color is not None:
            self.__colors[(x, y)] = color

    def add_altitude(self, x:int, y:int, alt:int) -> None:
        alt = max(0,min(alt,500)) #Eviter les cas extrême
        self.altitude[(x,y)] = alt
        self.update_color_from_altitude(x,y,alt)

    def get_neighbours(self, x: int, y: int) -> List[Coords]:

        """
        Retourne la liste des coordonnées des hexagones voisins de l'hexagone en coordonnées (x,y).
        """

        if y % 2 == 0:
            res = [(x + dx, y + dy) for dx, dy in ((1, 0), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1))]
        else:
            res = [(x + dx, y + dy) for dx, dy in ((1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (1, -1))]
        return [(dx, dy) for dx, dy in res if 0 <= dx < self.__width and 0 <= dy < self.__height]


    def show(self, alias: Dict[str, str] = None, debug_coords: bool = False) -> None:
        """
        Permet d'afficher via matplotlib la grille hexagonale. 
        :param alias: dictionnaire qui permet de modifier le label d'une couleur. Ex: {"white": "snow"} 
        :param debug_coords: booléen pour afficher les coordonnées des cases.
        
        Attention, le texte est succeptible de plus ou moins bien s'afficher en fonction de la taille de la
        fenêtre matplotlib et des dimensions de la grille.
        """

        if alias is None:
            alias = {}

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect('equal')

        h = self.__hexsize
        coords = {}
        for row in range(self.__height):
            for col in range(self.__width):
                x = col * 1.5 * h
                y = row * np.sqrt(3) * h
                if col % 2 == 1:
                    y += np.sqrt(3) * h / 2
                # coords[(row, col)] = (x, y)

                center = (x, y)
                hexagon = RegularPolygon(center, numVertices=6, radius=h, orientation=np.pi / 6,
                                         edgecolor="black")
                hexagon.set_facecolor(self.__colors[(row, col)])
                hexagon.set_alpha(self.__alpha[(row, col)])

                # Ajoute du texte à l'hexagone
                if debug_coords:
                     text = f"({row}, {col})"  # Le texte que vous voulez afficher
                     ax.annotate(text, xy=center, ha='center', va='center', fontsize=8, color='black')

                # ajoute l'hexagone
                ax.add_patch(hexagon)

                # gestion des Formes additionnelles
                forme = self.__symbols[(row, col)]
                if forme is not None:
                    ax.add_patch(forme.get(x, y, h))

        for coord1, coord2, color, thick in self.__links:
            if coord1 not in coords or coord2 not in coords:
                continue
            x1, y1 = coords[coord1]
            x2, y2 = coords[coord2]
            plt.gca().add_line(plt.Line2D([x1, x2], [y1, y2], color=color, linewidth=thick))

        ax.set_xlim(-h, self.__width * 1.5 * h + h)
        ax.set_ylim(-h, self.__height * np.sqrt(3) * h + h)
        ax.axis('off')

        ks, vs = [], []
        for color in set(self.__colors.values()):
            if color in alias:
                ks.append(alias[color])
            else:
                ks.append(color)
            vs.append(color)

        gradient_cmaps = [
            LinearSegmentedColormap.from_list('custom_cmap', ['white', vs[i]]) for i in range(len(vs))]
        # Créez une liste de patch à partir des polygones
        legend_patches = [
            Patch(label=ks[i], edgecolor="black", linewidth=1, facecolor=gradient_cmaps[i](0.9), )
            for i in range(len(ks))]
        # Ajoutez la légende à la figure
        ax.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()

"""==============================================================================================================="""


class Graph:
    """Classe représentant un graphe sous une liste de sucesseurs"""

    def __init__(self, n: int):
        self.succ = defaultdict(list) # dictionnaire des listes de successeurs, si on accède à une clé inexistante, on crée une liste vide
        for i in range(n):
            for j in range(n):
                self.succ[(i, j)] = []

    def add_edge(self, from_node, to_node):
        """Ajoute une arête entre from_node et to_node"""
        self.succ[from_node].append(to_node)
        self.succ[to_node].append(from_node)  # graphe non orienté

    def add_node(self, node):
        """Ajoute un noeud au graphe"""
        self.succ[node] = []

    def has_edge(self, from_node, to_node) -> bool:
        """Retourne True si une arête existe entre from_node et to_node, False sinon"""
        if from_node not in self.succ or to_node not in self.succ:
            return False
        return to_node in self.succ[from_node]
    
    def bfs(self, start_node, distance: int = None) -> Dict[Coords, int]:
        """
        Algorithme BFS (Breadth-First Search) qui retourne un dictionnaire avec les distances 
        de chaque noeud au noeud de départ.
        
        :param start_node: le noeud de départ
        :param distance: si spécifié, retourne seulement les noeuds à cette distance exacte
        :return: dictionnaire {noeud: distance} ou {noeud: distance} filtré si distance est spécifié
        """
        distances = {start_node: 0}
        queue = [start_node]
        
        while queue:
            current = queue.pop(0)
            current_distance = distances[current]
            
            for neighbor in self.succ[current]:
                if neighbor not in distances:
                    distances[neighbor] = current_distance + 1
                    queue.append(neighbor)
        
        if distance is not None:
            return {node: dist for node, dist in distances.items() if dist == distance}
        return distances

"""=====================================Main=========================================================================="""

def main():
    """
    Fonction exemple pour présenter le programme ci-dessus.
    """
    # CREATION D'UNE GRILLE 17x17
    hex_grid = HexGridViewer(17, 17)
    size = 17
    
    # Créer le graphe de la grille hexagonale
    graph = Graph(size)
    
    # applique les altitudes et crée les arêtes du graphe
    for i in range(size):
        for j in range(size):
            hex_grid.add_altitude(i, j, random.randint(0, 500))
            # Ajouter les arêtes entre voisins
            for neighbor in hex_grid.get_neighbours(i, j):
                if not graph.has_edge((i, j), neighbor):
                    graph.add_edge((i, j), neighbor)

    # BFS : Afficher toutes les zones à distance i d'une case de départ
    start_x, start_y = 8, 8
    distance_target = 3
    
    # Récupérer tous les noeuds à la distance cible
    nodes_at_distance = graph.bfs((start_x, start_y), distance=distance_target)
    
    # Colorer le noeud de départ en rouge
    hex_grid.add_color(start_x, start_y, "red")
    
    # Colorer tous les noeuds à la distance cible en violet
    for (x, y) in nodes_at_distance.keys():
        hex_grid.add_color(x, y, "purple")

    # AFFICHAGE DE LA GRILLE
    alias = {
        "blue": "Mer",
        "yellow": "Sable",
        "yellowgreen": "Prairie",
        "darkgreen": "Forêt",
        "gray": "Montagne",
        "red": "Départ",
        "purple": f"Distance {distance_target}"
    }
    hex_grid.show(alias=alias, debug_coords=False)


if __name__ == "__main__":
    main()

# # Quel algorithme utiliser pour générer une zone régulière qui s'étend sur la carte (i.e. toutes les cases à
# distance $i$ d'une case)?
#L'algorithm BFS

# # Quel algorithme permettrait de tracer des rivières à partir d'un point donné sur la carte, en ajoutant une
# contrainte d'altitude descendante en prenannt le chemin le plus long possible ?

# # Quel algorithme utiliser pour aller d'un point A à un point B ?
# BFS

# # Quel algorithme utiliser pour créer un réseau de routes le moins couteux possible entre x villes, pour qu'elles
# sont toutes interconnectées ?
#Kruskal

##