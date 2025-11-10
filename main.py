#Projet - Théorie des graphes
# ISEN - S5
# Auteur : Colin Rousseau & Gaspard Vieujean

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

Coords = Tuple[int, int]  # un simple alias de typage python

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
    
    def print(self):
        for node, succs in self.suc_list.items():
         print(f"{node} : {' -> '.join(map(str, succs))}")