def generate_coherent_map(self) -> None:
        """
        Génère une carte avec altitudes et terrains cohérents
        via l'algorithme Diamond-Square.
        """
        # Initialisation : tout à 0
        for x in range(self.width):
            for y in range(self.height):
                self.add_altitude(x, y, 0)
   
        # Initialiser les 4 coins avec des valeurs aléatoires
        self.add_altitude(0, 0, random.randint(50, 150))
        self.add_altitude(self.width - 1, 0, random.randint(50, 150))
        self.add_altitude(0, self.height - 1, random.randint(50, 150))
        self.add_altitude(self.width - 1, self.height - 1, random.randint(50, 150))
   
        randomness = 120  # Magnitude du bruit
        tileWidth = min(self.width, self.height) - 1
   
        # Trouver la plus grande puissance de 2
        step = 1
        while step < tileWidth:
            step *= 2
        step //= 2
   
        # Boucle principale Diamond-Square
        while step > 0:
            halfStep = step // 2
            if halfStep <= 0:
                break
       
            # ===== DIAMOND STEP =====
            # Calculer les centres des carrés
            for x in range(0, self.width, step):
                for y in range(0, self.height, step):
                    # Récupérer les 4 coins
                    x2 = (x + step) % self.width
                    y2 = (y + step) % self.height
               
                    c1 = self.get_altitude(x, y)
                    c2 = self.get_altitude(x2, y)
                    c3 = self.get_altitude(x, y2)
                    c4 = self.get_altitude(x2, y2)
               
                    # Moyenne des coins + bruit aléatoire
                    avg = (c1 + c2 + c3 + c4) / 4.0
                    avg += random.uniform(-randomness, randomness)
               
                    # Placer au centre
                    xm = (x + halfStep) % self.width
                    ym = (y + halfStep) % self.height
                    self.add_altitude(xm, ym, avg)
       
            # ===== SQUARE STEP =====
            # Calculer les milieux des arêtes
            for x in range(0, self.width, halfStep):
                for y in range((x + halfStep) % step, self.height, step):
                    neighbors = []
               
                    # Récupérer les 4 voisins (haut, bas, gauche, droite)
                    if self.get_altitude(x, (y - halfStep) % self.height) is not None:
                        neighbors.append(self.get_altitude(x, (y - halfStep) % self.height))
                    if self.get_altitude(x, (y + halfStep) % self.height) is not None:
                        neighbors.append(self.get_altitude(x, (y + halfStep) % self.height))
                    if self.get_altitude((x - halfStep) % self.width, y) is not None:
                        neighbors.append(self.get_altitude((x - halfStep) % self.width, y))
                    if self.get_altitude((x + halfStep) % self.width, y) is not None:
                        neighbors.append(self.get_altitude((x + halfStep) % self.width, y))
               
                    # Moyenne des voisins + bruit
                    if neighbors:
                        avg = sum(neighbors) / len(neighbors)
                        avg += random.uniform(-randomness, randomness)
                        self.add_altitude(x, y, avg)
       
            # Réduire le bruit progressivement
            randomness *= 0.6
            step //= 2
   
        # Lissage final (3 passes)
        for _ in range(3):
            self.fixHeightAlonePoints()
   
        # Collecter toutes les altitudes pour calculer les quantiles
        allaltitudes = []
        for vertex in self.get_all_vertices():
            altitude = self.get_altitude(*vertex)
            allaltitudes.append(altitude)
        
        # Calculer les seuils (15%, 35%, 65%, 85%)
        allquantiles = np.quantile(allaltitudes, [0.15, 0.35, 0.65, 0.85])
        
        # Assigner les terrains selon l'altitude
        self.generate_terrain(allaltitudes)
   
        # ===== GÉNÉRATION DES RIVIÈRES =====
        # Identifier les points hauts (> 85e percentile)
        high_points = [v for v in self.get_all_vertices()
                    if self.get_altitude(*v) > allquantiles[3]]
   
        # Environ 1 rivière pour 100 points hauts
        num_rivers = max(1, len(high_points) // 100)
   
        # Générer les rivières depuis des points hauts aléatoires
        for _ in range(num_rivers):
            if high_points:
                start = random.choice(high_points)
                rivers = self.generate_river_with_branches(start, branch_probability=0.15)
                self.display_rivers(rivers)



# =============== Méthodes utilisés dans 'generate_coherent_map()' ====================
def fixHeightAlonePoints(self) -> None:
        """Lisse les points isolés en moyennant avec leurs voisins."""
        new_altitudes = {}
        
        for vertex in self.get_all_vertices():
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


def generate_terrain(self, allaltitudes) -> None:
        """Assigne les terrains selon l'altitude (par quantiles)."""
        
        # Calculer les seuils
        allquantiles = np.quantile(allaltitudes, [0.15, 0.35, 0.65, 0.85])
   
        # Dictionnaires pour stocker les altitudes par type
        water_cells = []
        altitude_eau = {}
        altitude_desert = {}
        altitude_herbe = {}
        altitude_foret = {}
        altitude_montagne = {}
   
        for vertex in self.get_all_vertices():
            x, y = vertex
            altitude = self.get_altitude(x, y)
       
            # Assigner le terrain selon l'altitude
            if altitude < allquantiles[0]:  # 15% le plus bas
                self.add_terrain(x, y, "eau")
                altitude_eau[(x, y)] = altitude
                water_cells.append(vertex)
            elif altitude < allquantiles[1]:  # 15-35%
                self.add_terrain(x, y, "desert")
                altitude_desert[(x, y)] = altitude
            elif altitude < allquantiles[2]:  # 35-65%
                self.add_terrain(x, y, "herbe")
                altitude_herbe[(x, y)] = altitude
            elif altitude < allquantiles[3]:  # 65-85%
                self.add_terrain(x, y, "foret")
                altitude_foret[(x, y)] = altitude
            else:  # 15% le plus haut
                self.add_terrain(x, y, "montagne")
                altitude_montagne[(x, y)] = altitude
        
        # Calculer la transparence pour chaque type de terrain
        self.attribute_alpha(altitude_eau)
        self.attribute_alpha(altitude_desert)
        self.attribute_alpha(altitude_herbe)
        self.attribute_alpha(altitude_foret)
        self.attribute_alpha(altitude_montagne)

def attribute_alpha(self, altitude_terrain) -> None:
        """Calcule la transparence selon l'altitude normalisée."""
        if not altitude_terrain:
            return
            
        min_alt = min(altitude_terrain.values())
        max_alt = max(altitude_terrain.values())
        altitude_range = max_alt - min_alt if max_alt != min_alt else 1
         
        for coord, altitude in altitude_terrain.items():
            # Normaliser entre 0 et 1
            normalized = (altitude - min_alt) / altitude_range
            # Mapper sur [0.4, 1.0] pour la transparence
            alpha = 0.4 + (normalized * 0.6)
            self.viewer.add_alpha(coord[0], coord[1], alpha)