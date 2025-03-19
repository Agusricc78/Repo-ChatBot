import pandas as pd
import numpy as np
from movie import Movie

class RecommendationSystem:
    def __init__(self, ratings_df):
        self.ratings_df = ratings_df
        self.matriz = self.crear_matriz()
        self.usuario_features = self.calcular_usuario_features()

        # Lista de 20 películas predefinidas para recomendación (en formato Movie)
        self.peliculas_para_recomendar = [
            Movie(120, "The Lord of the Rings: The Fellowship of the Ring", "Young hobbit Frodo Baggins...", "2001-12-18", 8.396),
            Movie(106, "Predator", "A team of elite commandos...", "1987-06-12", 7.491),
            Movie(155, "The Dark Knight", "Batman raises the stakes in his war on crime...", "2008-07-14", 8.509),
            Movie(12, "Finding Nemo", "Nemo, an adventurous young clownfish...", "2003-05-30", 7.822),
            Movie(107, "Snatch", "Unscrupulous boxing promoters...", "2000-09-01", 7.803),
            Movie(38, "Eternal Sunshine of the Spotless Mind", "Joel Barish, heartbroken...", "2004-03-19", 8.1),
            Movie(13, "Forrest Gump", "A man with a low IQ has accomplished great things...", "1994-06-23", 8.5),
            Movie(280, "Terminator 2: Judgment Day", "Nearly 10 years have passed since Sarah Connor...", "1991-07-03", 8.096),
            Movie(310, "Bruce Almighty", "Bruce Nolan toils as a 'human interest' reporter...", "2003-05-23", 6.7),
            Movie(187, "Sin City", "Welcome to Sin City. This town beckons to the tough...", "2005-04-01", 7.437),
            Movie(238, "The Godfather", "Spanning the years 1945 to 1955, a chronicle...", "1972-03-14", 8.712),
            Movie(289, "Casablanca", "In Casablanca, Morocco in December 1941...", "1942-11-26", 8.173),
            Movie(275, "Fargo", "Jerry, a small-town Minnesota car salesman...", "1996-03-08", 7.87),
            Movie(675, "Harry Potter and the Order of the Phoenix", "Returning for his fifth year at Hogwarts...", "2007-06-28", 7.687),
            Movie(503, "Poseidon", "A packed cruise ship traveling the Atlantic...", "2006-05-10", 5.848),
            Movie(1271, "300", "Based on Frank Miller's graphic novel...", "2007-03-07", 7.17),
            Movie(3103, "Gladiator", "A former Roman General sets out to exact vengeance...", "2000-05-01", 8.2),
            Movie(244786, "Whiplash", "A promising young drummer enrolls at a music school...", "2014-10-10", 8.5),
            Movie(597, "Titanic", "A seventeen-year-old aristocrat falls in love...", "1997-11-18", 7.9),
            Movie(680, "Pulp Fiction", "The lives of two mob hitmen, a boxer, a gangster...", "1994-09-10", 8.9)
        ]

    def crear_matriz(self):
        # Crear una matriz de usuarios y películas
        return self.ratings_df.pivot(index='usuario_id', columns='pelicula_id', values='calificacion').fillna(0)

    def calcular_usuario_features(self):
        # Calcular las características del usuario usando SVD
        from sklearn.decomposition import TruncatedSVD
        
        svd = TruncatedSVD(n_components=5)  # Usa 5 componentes para obtener una mejor representación
        matriz_svd = svd.fit_transform(self.matriz)
        return pd.DataFrame(matriz_svd, index=self.matriz.index)

    def recomendar_peliculas(self, usuario_id, n_recomendaciones=5):
        if usuario_id not in self.matriz.index:
            print(f"Usuario {usuario_id} no encontrado en la matriz.")
            return []

        # Verifica que haya más de un usuario para calcular similitudes
        if len(self.matriz.index) == 1:
            print("No hay suficientes usuarios para calcular recomendaciones.")
            return []

        usuario_vector = self.usuario_features.loc[usuario_id].values.reshape(1, -1)

        # Cálculo de similitudes utilizando el coseno de similitud
        from sklearn.metrics.pairwise import cosine_similarity
        similitud = cosine_similarity(self.usuario_features, usuario_vector).flatten()
        similitud_df = pd.Series(similitud, index=self.matriz.index, name="similitud").sort_values(ascending=False)

        print("Similitudes calculadas:", similitud_df.head())

        # Obtener las películas vistas por el usuario actual
        peliculas_vistas = self.matriz.loc[usuario_id][self.matriz.loc[usuario_id] > 0].index.tolist()
        print("Películas vistas por el usuario:", peliculas_vistas)

        # Recomendaciones utilizando la lista de películas predefinidas
        recomendaciones = [
            (pelicula.id, pelicula.title, pelicula.rating)
            for pelicula in self.peliculas_para_recomendar
            if pelicula.id not in peliculas_vistas
        ]

        # Limitar las recomendaciones al número deseado
        recomendaciones = recomendaciones[:n_recomendaciones]

        if not recomendaciones:
            print("No se encontraron nuevas películas para recomendar.")
        else:
            print("Recomendaciones generadas:", recomendaciones)

        return recomendaciones  # Regresa la lista completa con ID de película, título y rating

    
    