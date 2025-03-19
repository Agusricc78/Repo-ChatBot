from API.dbAPI import MovieDatabaseAPI
import os
import csv
import pandas as pd

archivo_csv = "calificaciones.csv"

def obtener_peliculas_calificadas(archivo_csv):
    """Carga las calificaciones desde el archivo CSV."""
    if os.path.exists(archivo_csv):
        try:
            calificaciones_df = pd.read_csv(archivo_csv)
            # Verificar que el archivo contenga al menos las columnas necesarias
            if 'usuario_id' in calificaciones_df.columns and 'pelicula_id' in calificaciones_df.columns:
                return calificaciones_df
            else:
                print("El archivo no contiene las columnas necesarias.")
                return pd.DataFrame(columns=['usuario_id', 'pelicula_id', 'interaccion'])
        except pd.errors.EmptyDataError:
            print("El archivo de calificaciones está vacío.")
            return pd.DataFrame(columns=['usuario_id', 'pelicula_id', 'interaccion'])
    else:
        print(f"El archivo {archivo_csv} no se encontró.")
        return pd.DataFrame(columns=['usuario_id', 'pelicula_id', 'interaccion'])
    
# Ejemplo de uso
archivo_csv = "calificaciones.csv"
peliculas_calificadas = obtener_peliculas_calificadas(archivo_csv)

# Crear instancia de MovieDatabaseAPI
movie_api = MovieDatabaseAPI()

# Obtener nuevas películas no calificadas
nuevas_peliculas = movie_api.obtener_nuevas_peliculas(peliculas_calificadas)

# Imprimir nuevas películas
for pelicula in nuevas_peliculas:
    print(f"{pelicula.title} ({pelicula.release_date}) - Rating: {pelicula.rating}")
