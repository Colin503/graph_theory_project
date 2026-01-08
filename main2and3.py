"""
Programme basique en python3.8 permettant via matplolib de visualiser une grille hexagonale.

Elle propose simplement:
 - l'affichage des hexagones, avec des couleurs et une opacité
 - l'ajout de formes colorées sur les hexagones
 - l'ajout de liens colorés entre les hexagones

Contact: sebastien.gamblin@isen-ouest.yncrea.fr

Auteur : Colin Rousseau & Gaspard Vieujean
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
import matplotlib.colors as mcolors

#Visualisation de données / dessins / graphiques
from matplotlib.patches import RegularPolygon

#Importations de polygones réguliers
import matplotlib.pyplot as plt

#Gère propriétés de style par rapport aux formes
from matplotlib.patches import Patch

#Crée des palets de couleur spécifiques
from matplotlib.colors import LinearSegmentedColormap

#Calculs numériques & tableaux de données 
import numpy as np

# un simple alias de typage python
Coords = Tuple[int, int]  


# il y a mieux en python :
# - 3.11: Coords: AliasType = Tuple[int, int]
# - 3.12: type Coords = Tuple[int, int]


class Forme:
    """Superclasse abstraite qui sauvegarde une couleur et impose une méthode 'get' qui retourne un Patch."""

    def __init__(self, color: str = "black", edgecolor: str = None):
        #Verification de la couleur donné
        assert color in mcolors.CSS4_COLORS
        if edgecolor is not None:
            #Vérification de la couleur de la bordure donné
            assert edgecolor in mcolors.CSS4_COLORS
        self._color = color
        self._edgecolor = edgecolor

    #Méthode qui impose un Patch en retour
    @abstractmethod
    def get(self, x: float, y: float, h: int) -> Patch:
        pass


class Rect(Forme):
    """Redéfinition d'une Forme pour un rectangle."""

    def __init__(self, *args, **kwargs): #* arguments possible dans un tuple, ** argument possibles dans un dictionnaire
        super().__init__(*args, **kwargs) #Super constructeur de la classe forme

    def get(self, x: float, y: float, h: int) -> plt.Rectangle:
        return plt.Rectangle((x - h / 2, y - h / 2), h, h, facecolor=self._color, edgecolor=self._edgecolor)


class Circle(Forme):
    """Redéfinition d'une Forme pour un cercle."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, x: float, y: float, h: int) -> plt.Circle:
        return plt.Circle((x, y), h / 2, facecolor=self._color, edgecolor=self._edgecolor)


class HexGridViewer:
    """
    Classe permettant d'afficher une grille hexagonale. Elle se crée via son constructeur avec deux arguments:
    la largeur et la hauteur.
    Deux attributs gèrent l'apparence des hexagones: colors et alpha, pour respectivement représenter la
    couleur et la transparence des hexagones.
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

        # couleur des hexagones : par défaut, blanc
        self.__colors: Dict[Coords, str] = defaultdict(lambda: "white")
        
        # transparence des hexagones : par défaut, 1
        self.__alpha: Dict[Coords, float] = defaultdict(lambda: 1)
        
        # symboles sur les hexagones, par défaut, aucun symbole sur une case.
        # Limitation : un seul symbole par case !
        self.__symbols: Dict[Coords, Forme | None] = defaultdict(lambda: None)
        
        # liste de liens à affichager entre les cases.
        self.__links: List[Tuple[Coords, Coords, str, int]] = []

        #Altitudes du terrain
        self.__altitude: Dict[Coords, float] = defaultdict(lambda: 0.0)

        #Types de terrain
        self.__terrain: Dict[Coords, str] = defaultdict(lambda: "inconnu")

    def get_width(self) -> int:
        """Retourne la largeur (nombre de colonnes)."""
        return self.__width

    def get_height(self) -> int:
        """Retourne la hauteur (nombre de lignes)."""
        return self.__height

    def add_color(self, x: int, y: int, color: str) -> None:
        """Ajoute une couleur à la coordonnée (x, y) en vérifiant qu'elle est valide."""
        assert color in mcolors.CSS4_COLORS, \
            f"self.__colors type must be in matplotlib colors. What is {color} ?"
        self.__colors[(x, y)] = color

    def add_alpha(self, x: int, y: int, alpha: float) -> None:
        """Ajoute un indice d'opacité (alpha) entre 0 et 1 pour la case (x, y)."""
        assert 0 <= alpha <= 1, f"alpha value must be between 0 and 1. What is {alpha} ?"
        self.__alpha[(x, y)] = alpha

    def add_symbol(self, x: int, y: int, symbol: Forme) -> None:
        """Place un symbole (`Forme`) au centre de la case (x, y)."""
        self.__symbols[(x, y)] = symbol

    def add_link(self, coord1: Coords, coord2: Coords, color: str = None, thick=2) -> None:
        """Ajoute un lien visuel entre deux cases (coord1 -> coord2).
        `color` et `thick` définissent l'apparence du segment.
        """
        self.__links.append((coord1, coord2, color if color is not None else "black", thick))

    def get_color(self, x: int, y: int) -> str:
        """Retourne la couleur de la case (x, y)."""
        return self.__colors[(x, y)]

    def get_alpha(self, x: int, y: int) -> float:
        """Retourne l'opacité (alpha) de la case (x, y)."""
        return self.__alpha[(x, y)]

    def get_neighbours(self, x: int, y: int) -> List[Coords]:

        """
        Retourne la liste des coordonnées des hexagones voisins de l'hexagone en coordonnées (x,y).
        """

        if y % 2 == 0:
            res = [(x + dx, y + dy) for dx, dy in ((1, 0), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1))]
        else:
            res = [(x + dx, y + dy) for dx, dy in ((1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (1, -1))]
        return [(dx, dy) for dx, dy in res if 0 <= dx < self.__width and 0 <= dy < self.__height]
    
    def add_altitude(self, x: int, y: int, alt: float) -> None:
        """Ajoute une altitude à la case (x, y)."""
        self.__altitude[(x,y)] = alt

    def get_altitude(self, x: int, y: int) -> float:
        """Obtient l'altitude d'une certaine case"""
        return self.__altitude[(x,y)]
    
    def add_terrain(self, x:int, y:int, terrain: str) -> None:
        """Ajoute un terrain à la case (x, y)."""
        self.__terrain[(x,y)] = terrain

        #Attribuer la couleur selon le terrain
        terrain_colors = {
            "eau": "dodgerblue",
            "sable" : "sandybrown",
            "herbe" : "lightgreen",
            "foret" : "darkgreen",
            "montagne" : "lightgray"
        }

        if terrain in terrain_colors:
            self.add_color(x,y,terrain_colors[terrain])
    
    def get_terrain(self, x: int, y: int) -> str:
        """Retourne le type de terrain d'une case"""
        return self.__terrain[(x,y)]

    def get_all_coords(self) -> List[Coords]:
        """Retourne la liste de toutes les coordonnées de la grille."""
        return [(x, y) for x in range(self.__width) for y in range(self.__height)]
    
    def attribute_alpha_by_terrain(self) -> None:
        """
        Calcule et attribue la transparence (alpha) pour chaque type de terrain
        en fonction de l'altitude au sein de ce terrain.
        Alpha varie de 0.4 (altitude la plus basse du terrain) à 1.0 (altitude la plus haute). Sauf pour l'eau
        """

        # Dictionnaire pour regrouper les cases par terrain
        terrain_cases = defaultdict(list)

        # Regrouper les cases par type de terrain avec leurs altitudes
        for (x, y), terrain in self.__terrain.items():
            altitude = self.__altitude[(x, y)]
            terrain_cases[terrain].append(((x, y), altitude))

        # Calculer et attribuer l'alpha pour chaque terrain
        for terrain, cases in terrain_cases.items():
            altitudes = [alt for (_, alt) in cases]
            min_alt = min(altitudes)
            max_alt = max(altitudes)

            for (x, y), altitude in cases:
                if max_alt == min_alt:
                    alpha = 1.0  
                else:
                    alpha = 0.4 + 0.6 * (altitude - min_alt) / (max_alt - min_alt)
                self.add_alpha(x, y, alpha)

    def generate_terrain(self, altitudes) -> None:
        """Assigne les terrains selon l'altitude (par quantiles)."""

        quantiles = np.quantile(altitudes, [0.15, 0.35, 0.65, 0.85])

        for x in range(self.__width):
            for y in range(self.__height):
                altitude = self.get_altitude(x, y)

                if altitude < quantiles[0]:
                    self.add_terrain(x, y, "eau") 
                elif altitude < quantiles[1]:
                    self.add_terrain(x, y, "sable")
                elif altitude < quantiles[2]:
                    self.add_terrain(x, y, "herbe")
                elif altitude < quantiles[3]:
                    self.add_terrain(x, y, "foret")
                else:
                    self.add_terrain(x, y, "montagne")

    def generate_random_map(self) -> None:
        """Génère une carte aléatoire pour avoir une visualisation des altitudes et terraines"""
        for x in range(self.__width):
            for y in range(self.__height):
                alt = random.uniform(0, 100)
                self.add_altitude(x, y, alt)
        self.generate_terrain([self.get_altitude(x, y) for x in range(self.__width) for y in range(self.__height)])
        self.attribute_alpha_by_terrain()


    def show(self, alias: Dict[str, str] = None, debug_coords: bool = False) -> None:
        """
        Affiche la grille hexagonale via `matplotlib`.

        :param alias: dictionnaire qui permet de renommer les labels de la légende
                      Ex: {"white": "snow"}
        :param debug_coords: si True, affiche les coordonnées (x,y) au centre des hexagones.

        Remarque: l'affichage du texte dépend de la taille de la figure et des dimensions de la grille.
        """

        #Modifier le label d'une couleur
        if alias is None:
            alias = {}

        fig, ax = plt.subplots(figsize=(8, 8))

        #Permettre que l'axe x et y soient pareille        
        ax.set_aspect('equal')

        h = self.__hexsize
        coords = {}
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
                if debug_coords:
                    text = f"({row}, {col})"  # Le texte que vous voulez afficher
                    ax.annotate(text, xy=center, ha='center', va='center', fontsize=6, color='black')

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

    size = 33
    center = (size-1)//2
    distance = 3

    # CREATION D'UNE GRILLE TAILLE SIZE
    hex_grid = HexGridViewer(33, 33)

    # GENERATION D'UNE CARTE ALEATOIRE
    hex_grid.generate_random_map()

    # AFFICHAGE DE LA GRILLE
    # alias permet de renommer les noms de la légende pour des couleurs spécifiques.
    # debug_coords permet de modifier l'affichage des coordonnées sur les cases.
    hex_grid.show(alias={"dodgerblue": "water", "sandybrown": "sable", "lightgreen": "grass", "darkgreen": "forest", "lightgray": "montagne", "cyan": "river"}, debug_coords=False)


if __name__ == "__main__":
    main()

