# Projet de Théorie des Graphes — Semestre 5

> **Sujet :** Modélisation et génération procédurale d’une carte sur **grille hexagonale**, avec terrains, altitudes et rivières.

---

## 📌 Objectifs du projet

* Implémenter un **graphe** représentant une **grille hexagonale**
* Étendre le modèle avec des **altitudes** et des **types de terrains**
* Tester la génération **aléatoire**
* Utiliser des **algorithmes de parcours de graphe** (BFS, DFS)
* Générer une carte **cohérente** avec rivières (et lacs en extension)

---

## 🧱 1. Implémentation d’un graphe hexagonal

Nous utilisons une **grille hexagonale** pour représenter le graphe.

### Propriétés respectées

* Chaque **case** est un **sommet**
* Les **arêtes** relient les cases voisines (6 voisins possibles)
* Le graphe est :

  * non orienté
  * connexe
  * parcourable

Cette structure respecte toutes les propriétés fondamentales d’un graphe.

---

## 🏔️ 2. Extension : Altitudes et types de terrains

Nous avons étendu l’implémentation en ajoutant :

* Un attribut `altitude` pour chaque sommet
* Une altitude **minimale** et **maximale** dans la classe `HexGridViewer`

### Détermination du terrain

Le type de terrain d’une case est déduit de son altitude, par exemple :

| Altitude | Terrain  |
| -------- | -------- |
| Basse    | Eau      |
| Moyenne  | Herbe    |
| Élevée   | Montagne |

---

## 🎲 3. Tests avec génération aléatoire

* Les **altitudes** sont générées aléatoirement
* Les **terrains** sont automatiquement assignés
* Le programme est testé via le fichier `main.py`

La visualisation permet de vérifier la cohérence du terrain généré.

---

## 🟦 4. Génération de zones régulières

### Algorithme utilisé

👉 **BFS (Breadth-First Search)**

### Principe

* À partir d’une case source
* On explore toutes les cases à distance `i`
* Chaque distance peut être associée à une **couleur différente**

### Adaptation

* Ajout d’un compteur de distance
* Arrêt du parcours à la distance maximale souhaitée

---

## 🏔️ 5. Analyse de la carte

### a) Trouver le sommet le plus haut

* Parcours de toutes les cases
* Comparaison des valeurs d’altitude
* Conservation de l’altitude maximale rencontrée

⏱️ Complexité : **O(n)**

---

### b) Génération de rivières

#### Algorithme utilisé

👉 **DFS (Depth-First Search)**

#### Contraintes

* L’altitude doit être **strictement descendante**
* Le chemin doit être **le plus long possible**

DFS est adapté car il explore un chemin en profondeur avant de revenir en arrière.

---

### c) Embranchements de rivières

Pour créer des embranchements :

* On explore **tous les voisins valides** (et pas uniquement le plus bas)

### Structure obtenue

* 🌳 **Arbre**
* ou
* 🔀 **Graphe orienté acyclique (DAG)**

---

## 🗺️ 6. Génération complète d’une carte cohérente

### Algorithme proposé

👉 **Diamond-Square Algorithm**

Cet algorithme permet :

* Une génération procédurale réaliste des altitudes
* Des transitions naturelles entre terrains

### Étapes générales

1. Génération des altitudes (Diamond-Square)
2. Attribution des terrains selon l’altitude
3. Détection des sommets élevés (sources)
4. Génération des rivières par DFS

---

### 🌊 Extension bonus : Lacs

#### Contrainte ajoutée

* L’eau n’est plus uniquement **linéaire** (rivière)
* Elle peut former des **zones fermées**

#### Solution possible

* Détection de **minima locaux**
* Remplissage des bassins
* Vérification de l’écoulement ou stagnation

---

## ✅ Conclusion

Ce projet combine :

* Structures de graphes
* Algorithmes classiques (BFS, DFS)
* Génération procédurale
* Modélisation réaliste de terrains

Il permet d’obtenir une carte cohérente et extensible, proche des systèmes utilisés dans les jeux vidéo ou la simulation.

---

📚 **Mots-clés :** Graphe, Grille hexagonale, BFS, DFS, Diamond-Square, Génération procédurale
