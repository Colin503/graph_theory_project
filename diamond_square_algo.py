import numpy as np
import random

def diamond_square(width, height, roughness=0.5, max_altitude=500):
    """
    Algorithme Diamond-Square pour générer un terrain réaliste avec altitudes progressives.
    
    :param width: largeur de la grille
    :param height: hauteur de la grille
    :param roughness: facteur de rugosité (0-1), plus élevé = plus de variation
    :param max_altitude: altitude maximale (0-500)
    :return: matrice 2D des altitudes
    """
    
    # Initialiser la grille avec des dimensions qui sont des puissances de 2 + 1
    size = 2 ** int(np.ceil(np.log2(max(width, height)))) + 1
    grid = np.zeros((size, size))
    
    # Initialiser les quatre coins avec des altitudes aléatoires
    grid[0, 0] = random.randint(0, max_altitude)
    grid[0, size-1] = random.randint(0, max_altitude)
    grid[size-1, 0] = random.randint(0, max_altitude)
    grid[size-1, size-1] = random.randint(0, max_altitude)
    
    scale = max_altitude
    step = size - 1
    
    # Algorithme Diamond-Square
    while step > 1:
        half_step = step // 2
        
        # Phase Diamond
        for i in range(0, size - 1, step):
            for j in range(0, size - 1, step):
                # Moyenne des quatre coins + variation aléatoire
                avg = (grid[i, j] + grid[i, j + step] + 
                       grid[i + step, j] + grid[i + step, j + step]) / 4
                variation = random.uniform(-1, 1) * scale * roughness
                grid[i + half_step, j + half_step] = np.clip(avg + variation, 0, max_altitude)
        
        # Phase Square
        for i in range(0, size, half_step):
            for j in range((i + half_step) % step, size, step):
                # Moyenne des 4 voisins (haut, bas, gauche, droite)
                neighbors = []
                if i - half_step >= 0:
                    neighbors.append(grid[i - half_step, j])
                if i + half_step < size:
                    neighbors.append(grid[i + half_step, j])
                if j - half_step >= 0:
                    neighbors.append(grid[i, j - half_step])
                if j + half_step < size:
                    neighbors.append(grid[i, j + half_step])
                
                if neighbors:
                    avg = np.mean(neighbors)
                    variation = random.uniform(-1, 1) * scale * roughness
                    grid[i, j] = np.clip(avg + variation, 0, max_altitude)
        
        # Réduire l'échelle et le pas
        scale *= roughness
        step = half_step
    
    # Retourner la grille redimensionnée aux bonnes dimensions
    return grid[:height, :width]


def smooth_terrain(altitude_grid, iterations=3):
    """
    Lisse le terrain pour éviter les pentes trop abruptes.
    
    :param altitude_grid: matrice des altitudes
    :param iterations: nombre d'itérations de lissage
    :return: grille lissée
    """
    grid = altitude_grid.copy()
    height, width = grid.shape
    
    for _ in range(iterations):
        new_grid = grid.copy()
        for i in range(1, height - 1):
            for j in range(1, width - 1):
                # Moyenne avec les 4 voisins
                neighbors = [grid[i-1, j], grid[i+1, j], grid[i, j-1], grid[i, j+1]]
                new_grid[i, j] = (grid[i, j] + np.mean(neighbors)) / 2
        grid = new_grid
    
    return grid