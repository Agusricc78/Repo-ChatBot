import pandas as pd
import numpy as np
import os
from scipy.sparse import csr_matrix
from implicit.als import AlternatingLeastSquares

# Archivo donde se almacenan las calificaciones
CALIFICACIONES_ARCHIVO = "calificaciones.csv"

def cargar_calificaciones():
    """Carga las calificaciones desde el archivo CSV."""
    if os.path.exists(CALIFICACIONES_ARCHIVO):
        df = pd.read_csv(CALIFICACIONES_ARCHIVO)
        if 'usuario_id' not in df.columns or 'pelicula_id' not in df.columns or 'calificacion' not in df.columns:
            print("Error: El archivo de calificaciones no contiene las columnas necesarias.")
            return pd.DataFrame(columns=['usuario_id', 'pelicula_id', 'calificacion'])
        return df
    else:
        return pd.DataFrame(columns=['usuario_id', 'pelicula_id', 'calificacion'])

def prueba_precision(usuario_email="milei123@hotmail.com"):
    """Calcula la precisión del sistema de recomendación para un solo usuario."""
    calificaciones_df = cargar_calificaciones()

    if calificaciones_df.empty:
        print("No hay suficientes calificaciones para ejecutar las pruebas de precisión.")
        return

    # Filtrar las calificaciones para el usuario especificado
    usuario_df = calificaciones_df[calificaciones_df['usuario_id'] == usuario_email]

    if usuario_df.empty:
        print(f"No hay suficientes calificaciones para el usuario {usuario_email} para realizar la prueba.")
        return

    # Crear la matriz dispersa de calificaciones para el usuario especificado
    pelicula_codes, pelicula_indices = pd.factorize(calificaciones_df['pelicula_id'])

    # Reindexar las calificaciones de usuario
    usuario_df['pelicula_code'] = usuario_df['pelicula_id'].map(
        dict(zip(calificaciones_df['pelicula_id'], pelicula_codes))
    )

    # Crear la matriz de interacciones del usuario (tiene una sola fila)
    user_item_matrix = csr_matrix((usuario_df['calificacion'], ([0] * len(usuario_df), usuario_df['pelicula_code'])),
                                  shape=(1, len(pelicula_codes)))

    # Entrenar el modelo ALS con la matriz de usuario-película
    model = AlternatingLeastSquares(factors=10, regularization=0.1, iterations=20)
    model.fit(user_item_matrix.T)

    # Obtener recomendaciones para el usuario especificado
    user_index = 0  # Solo hay un usuario en la matriz
    recomendaciones = model.recommend(user_index, user_item_matrix, N=5, filter_already_liked_items=False)

    # Mostrar las recomendaciones
    print(f"\nRecomendaciones para el usuario {usuario_email}:")
    for rec in recomendaciones:
        pelicula_code = int(rec[0])  # Código interno de la película, asegurarse de que sea un valor entero
        score = rec[1]               # Puntaje de la recomendación
        
        # Validar que el índice no sea mayor al tamaño del arreglo
        if pelicula_code < len(pelicula_indices):
            pelicula_original_id = pelicula_indices[pelicula_code]
            print(f"Película ID: {pelicula_original_id} - Puntaje: {score:.2f}")
        else:
            print(f"Error: Índice {pelicula_code} fuera de los límites para el mapeo de película.")

if __name__ == "__main__":
    prueba_precision()
