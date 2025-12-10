import numpy as np
import random

def diamond_square(grid, roughness=0.5, max_altitude=12):
    #Avoir les coins initiaux avec des valeurs aléatoires
    h = len(grid)
    grid[0, 0] = random.randint(1, max_altitude)
    grid[0, h-1] = random.randint(1, max_altitude)
    grid[h-1, 0] = random.randint(1, max_altitude)
    grid[h-1, h-1] = random.randint(1, max_altitude) 
    i = h - 1

    #Boucle principale
    while i > 1: 
        id_val = i // 2 
        
        #Phase de diamant : allant au centre des carrés
        for x in range(0, h - 1, i):
            for y in range(0, h - 1, i):
                avg = (grid[x, y] + grid[x, y+i] + grid[x+i, y] + grid[x+i, y+i]) / 4.0
                grid[x+id_val, y+id_val] = avg + random.randint(int(-id_val), int(id_val)) * roughness
    
        #Phase de carré
        offset = 0
        for x in range(0, h, int(id_val)):
            if offset == 0:
                offset = int(id_val)
            else:
                offset = 0
            for y in range(offset, int(h), int(id_val)):
                sum_val = 0
                n = 0
                if x - int(id_val) >= 0:
                    sum_val += grid[x - int(id_val), y]
                    n += 1
                if x + int(id_val) < h:
                    sum_val += grid[x + int(id_val), y]
                    n += 1
                if y >= int(id_val):
                    sum_val += grid[x, y - int(id_val)]
                    n += 1
                if y + int(id_val) < h:
                    sum_val += grid[x, y + int(id_val)]
                    n += 1
                grid[x, y] = sum_val / n + random.randint(-int(id_val), int(id_val)) * roughness
        i = int(id_val)
    return grid



grid = [[0 for _ in range(17)] for _ in range(17)]
print(diamond_square(np.array(grid)))