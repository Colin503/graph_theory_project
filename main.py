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
import matplotlib.pyplot as plt

#Importations des couleurs avec une précision
import matplotlib.colors as mcolors

#Importations de polygones réguliers
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

        #Altitudes du terrain
        self.__altitude: Dict[Coords, float] = defaultdict(lambda: 0)

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
            #Cas ou y est paire, res [(2,0)...]
            res = [(x + dx, y + dy) for dx, dy in ((1, 0), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1))]
        else:
            #Cas ou y est impaire
            res = [(x + dx, y + dy) for dx, dy in ((1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (1, -1))]
        #Return des voisins en vérifiant qu'ils sont bien dans les limites 
        return [(dx, dy) for dx, dy in res if 0 <= dx < self.__width and 0 <= dy < self.__height]

    def add_altitude(self, x: int, y: int, alt: float) -> None:
        """Définit l'altitude d'une case."""
        self.__altitude[(x, y)] = alt

    def get_altitude(self, x: int, y: int) -> float:
        """Obtient l'altitude d'une case."""
        return self.__altitude[(x, y)]
    
    def highest_altitude(self) -> float:
        """Retourne l'altitude avec ses coordonnées la plus haute de la grille"""
        high_alt = -1.0
        Coordinates = (-1, -1)
        for x in range(self.__width):
            for y in range(self.__height):
                alt = self.get_altitude(x, y)
                if alt > high_alt:
                    high_alt = alt
                    Coordinates = (x, y)
        return high_alt, Coordinates

    def add_terrain(self, x: int, y: int, terrain: str) -> None:
        """Définit le type de terrain d'une case."""
        self.__terrain[(x, y)] = terrain
        
        # Attribuer la couleur selon le terrain
        terrain_colors = {
            "eau": "dodgerblue",
            "sable": "sandybrown",
            "herbe": "lightgreen",
            "foret": "darkgreen",
            "montagne": "lightgray"
        }

        if terrain in terrain_colors:
            self.add_color(x, y, terrain_colors[terrain])

    def get_terrain(self, x: int, y: int) -> str:
        """Obtient le type de terrain d'une case."""
        return self.__terrain[(x, y)]

    def get_all_coords(self) -> List[Coords]:
        """Retourne toutes les coordonnées de la grille."""
        return [(x, y) for x in range(self.__width) for y in range(self.__height)]

    def generate_terrain(self, allaltitudes) -> None:
        """Assigne les terrains selon l'altitude (par quantiles)."""
        
        # Calculer les seuils, permet d'avoir des meilleurs seuil et donc une meilleure répartition des terrain
        allquantiles = np.quantile(allaltitudes, [0.15, 0.35, 0.65, 0.85])

        #Pour assigner terrain et alpha :
        terrain_groups = defaultdict(list)

        for vertex in self.get_all_coords():
            x, y = vertex
            altitude = self.get_altitude(x, y)
            if altitude < allquantiles[0]:  
                terrain = "eau"
                self.add_terrain(x, y, terrain)
            elif altitude < allquantiles[1]: 
                terrain = "sable"
                self.add_terrain(x, y, terrain)
            elif altitude < allquantiles[2]:  
                terrain = "herbe"
                self.add_terrain(x, y, terrain)
            elif altitude < allquantiles[3]:  
                terrain = "foret"
                self.add_terrain(x, y, terrain)
            else:  
                terrain = "montagne"
                self.add_terrain(x, y, terrain)
            
            terrain_groups[terrain].append((x,y, altitude)) # {"montagne" : [(1,3,23)]}
        
        for terrain_type, cells in terrain_groups.items():
            if not cells:
                continue
            
            altitudes = [cell[2] for cell in cells]
            min_alt = min(altitudes)
            max_alt = max(altitudes)

            if max_alt != min_alt:
                altitude_range = max_alt - min_alt 
            else: #cas ou les altitudes max et min sont les mêmes
                altitude_range = 1

            is_water = (terrain_type == "eau") #Vrai ou Faux

            for x, y, altitude in cells:

                #calcul et assignation de la normalisation, plus une altitude est grande plus sa normalisationest grande
                normal = (altitude - min_alt) / altitude_range

                #Inversion de l'alpha en fonction de si c'est de l'eau, garde la plage de 0.4 à 1.0
                if is_water:
                    alpha = (1.0 - normal * 0.6)
                else:
                    alpha = (0.4 + normal * 0.6)
                    self.add_alpha(x,y,alpha)
                


    def fixHeightAlonePoints(self) -> None:
        """Lisse les points isolés en moyennant avec leurs voisins."""
        new_altitudes = {}
        
        for vertex in self.get_all_coords():
            neighbours = self.get_neighbours(*vertex)
            if neighbours:

                # Moyenne entre altitude actuelle et moyenne des voisins
                avg_altitude = sum(self.get_altitude(*n) for n in neighbours) / len(neighbours)
                current = self.get_altitude(*vertex)
                new_altitudes[vertex] = (current + avg_altitude) / 2
            else:
                new_altitudes[vertex] = self.get_altitude(*vertex)
        
        # Appliquer les nouvelles altitudes
        for vertex, altitude in new_altitudes.items():
            self.add_altitude(*vertex, altitude)        



    def generate_river_with_branches(self, current_coord: Coords, branch_probability=0.2, visited=None) -> List[Tuple[Coords, Coords]]:
        """
        Génère une rivière avec des embranchements.
        Retourne une liste de segments (tuple de deux coordonnées).
        """
        if visited is None:
            visited = set()
        
        if current_coord in visited:
            return []
        
        visited.add(current_coord)
        
        x, y = current_coord
        current_alt = self.get_altitude(x, y)
        neighbors = self.get_neighbours(x, y)
        
        # Voisins strictement plus bas
        downhill = [n for n in neighbors if self.get_altitude(n[0], n[1]) < current_alt and n not in visited]
        
        if not downhill:
            return []

        links = []
        # Choisir le voisin le plus bas pour la direction principale
        best_neighbor = min(downhill, key=lambda n: self.get_altitude(n[0], n[1]))
        links.append((current_coord, best_neighbor))
        links.extend(self.generate_river_with_branches(best_neighbor, branch_probability, visited))

        # Chance d'embranchements multiples
        if len(downhill) > 1:
            other_neighbors = [n for n in downhill if n != best_neighbor]
            for neighbor in other_neighbors:
                if random.random() < branch_probability:
                    links.append((current_coord, neighbor))
                    links.extend(self.generate_river_with_branches(neighbor, branch_probability * 0.7, visited))
                
        return links

    
    def display_rivers(self, rivers: List[Tuple[Coords, Coords]]) -> None:
        """Affiche les rivières sur la carte."""
        for start, end in rivers:
            self.add_color(start[0], start[1], "dodgerblue")

    def generate_coherent_map(self) -> None:
        """
        Génère une carte avec altitudes et terrains cohérents
        via l'algorithme Diamond-Square.
        """
        
        # Initialisation : tout à 0
        for x in range(self.get_width()):
            for y in range(self.get_height()):
                self.add_altitude(x, y, 0)

        # Initialiser les 4 coins
        self.add_altitude(0, 0, random.randint(50, 150))
        self.add_altitude(self.get_width() - 1, 0, random.randint(50, 150))
        self.add_altitude(0, self.get_height() - 1, random.randint(50, 150))
        self.add_altitude(self.get_width() - 1, self.get_height() - 1, random.randint(50, 150))

        randomness = 120
        tileWidth = min(self.get_width(), self.get_height()) - 1
        step = 1
        while step < tileWidth:
            step *= 2
        step //= 2

        while step > 0:
            halfStep = step // 2
            if halfStep <= 0:
                break
            
            # Diamond step
            for x in range(0, self.get_width(), step):
                for y in range(0, self.get_height(), step):
                    x2 = (x + step) % self.get_width()
                    y2 = (y + step) % self.get_height()
                    c1 = self.get_altitude(x, y)
                    c2 = self.get_altitude(x2, y)
                    c3 = self.get_altitude(x, y2)
                    c4 = self.get_altitude(x2, y2)
                    avg = (c1 + c2 + c3 + c4) / 4.0
                    avg += random.uniform(-randomness, randomness)
                    xm = (x + halfStep) % self.get_width()
                    ym = (y + halfStep) % self.get_height()
                    self.add_altitude(xm, ym, avg)
            
            # Square step
            for x in range(0, self.get_width(), halfStep):
                for y in range((x + halfStep) % step, self.get_height(), step):
                    neighbors = []
                    if self.get_altitude(x, (y - halfStep) % self.get_height()) is not None:
                        neighbors.append(self.get_altitude(x, (y - halfStep) % self.get_height()))
                    if self.get_altitude(x, (y + halfStep) % self.get_height()) is not None:
                        neighbors.append(self.get_altitude(x, (y + halfStep) % self.get_height()))
                    if self.get_altitude((x - halfStep) % self.get_width(), y) is not None:
                        neighbors.append(self.get_altitude((x - halfStep) % self.get_width(), y))
                    if self.get_altitude((x + halfStep) % self.get_width(), y) is not None:
                        neighbors.append(self.get_altitude((x + halfStep) % self.get_width(), y))
                    if neighbors:
                        avg = sum(neighbors) / len(neighbors)
                        avg += random.uniform(-randomness, randomness)
                        self.add_altitude(x, y, avg)
            
            randomness *= 0.6
            step //= 2

        # Lissage
        for _ in range(3):
            self.fixHeightAlonePoints()

        # Génération des terrains
        allaltitudes = [self.get_altitude(*v) for v in self.get_all_coords()]
        allquantiles = np.quantile(allaltitudes, [0.15, 0.35, 0.65, 0.85])
        self.generate_terrain(allaltitudes)


        # ===== GÉNÉRATION AMÉLIORÉE DES RIVIÈRES =====
        # Identifier les points hauts (foret et montagne)
        high_points = [v for v in self.get_all_coords()
                    if self.get_terrain(*v) in ["foret", "montagne"]]
        
        # Filtrer pour ne garder que les points vraiment hauts
        altitude_threshold = np.percentile(allaltitudes, 70)
        high_points = [v for v in high_points if self.get_altitude(*v) > altitude_threshold]
        
        # Augmenter le nombre de rivières : environ 1 pour 30-50 points hauts
        num_rivers = max(3, len(high_points) // 40)
        
        print(f"Génération de {num_rivers} rivières depuis {len(high_points)} points hauts")
        
        # Générer plusieurs rivières indépendantes
        used_starts = set()
        for _ in range(num_rivers):
            if high_points:
                # Sélectionner un point de départ non utilisé
                available_starts = [p for p in high_points if p not in used_starts]
                if not available_starts:
                    break
                    
                start = random.choice(available_starts)
                used_starts.add(start)
                
                # Générer la rivière avec plus d'embranchements
                rivers = self.generate_river_with_branches(start, branch_probability=0.25)
                self.display_rivers(rivers)
                
                # Marquer une zone autour du départ pour éviter des rivières trop proches
                for neighbor in self.get_neighbours(*start):
                    used_starts.add(neighbor)

    def bfs(self, start_x: int, start_y: int, max_distance: int) -> Dict[int, List[Coords]]:
            """Implémentation du BFS sur le graphe."""
            start = (start_x, start_y)
            visited = {start: 0}
            queue = deque([(start, 0)])
            case_per_distance = {}
            
            while queue:
                (x, y), distance = queue.popleft()

                if distance not in case_per_distance:
                    case_per_distance[distance] = []
                case_per_distance[distance].append((x, y))

                if distance < max_distance:
                    neighbors = self.get_neighbours(x, y)
                    for neighbor in neighbors:
                        if neighbor not in visited:
                            visited[neighbor] = distance + 1
                            queue.append((neighbor, distance + 1))
            return case_per_distance

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
    center = (size - 1) // 2
    distance = 3

    # CREATION D'UNE GRILLE TAILLE SIZE
    hex_grid = HexGridViewer(size, size)
    
    #Génération du terrain aléatoire
    #for i in range(size):
    #    for j in range(size):
    #        hex_grid.add_altitude(i, j, random.randint(0, 100))
    
    #Génération de la carte cohérente
    hex_grid.generate_coherent_map()

    #BFS
    #colors = ["black", "red", "orange", "yellow"]
    #case_per_distance = hex_grid.bfs(center, center, distance)
    #for d in range(distance+1):
    #    coords_list = case_per_distance.get(d, [])
    #    if d < len(colors):
    #        color = colors[d]
    #    else: 
    #        colors[-1]
    #    for x, y in coords_list:
    #        hex_grid.add_color(x, y, color)
    #        hex_grid.add_alpha(x, y, 1.0)


    # AFFICHAGE DE LA GRILLE
    # alias permet de renommer les noms de la légende pour des couleurs spécifiques.
    # debug_coords permet de modifier l'affichage des coordonnées sur les cases.
    hex_grid.show(alias={"dodgerblue": "water", "sandybrown": "sable", "lightgreen": "grass", "darkgreen": "forest", "lightgray": "montagne", "cyan": "river"}, debug_coords=False)


#Eviter d'éxécuter tout le code de la page si le fichier est importer
if __name__ == "__main__":
    main()