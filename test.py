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

# un simple alias de typage python : type (x,y)
Coords = Tuple[int, int] 


