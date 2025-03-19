import pandas as pd
import os
import time
from user import User
from API.dbAPI import MovieDatabaseAPI
from Recomendation_system import RecommendationSystem
from pruebas_precision import prueba_precision  
from utilidad import obtener_peliculas_calificadas  


CALIFICACIONES_ARCHIVO = "calificaciones.csv"

def cargar_calificaciones():
    """Carga las calificaciones desde el archivo CSV."""
    if os.path.exists(CALIFICACIONES_ARCHIVO):
        return pd.read_csv(CALIFICACIONES_ARCHIVO)
    else:
        return pd.DataFrame(columns=['usuario_id', 'pelicula_id', 'calificacion'])

def guardar_calificaciones(calificaciones_df):
    """Guarda las calificaciones en el archivo CSV."""
    calificaciones_df.to_csv(CALIFICACIONES_ARCHIVO, index=False)

def calificar_peliculas(email):
    """Permite al usuario calificar películas populares y guarda las calificaciones."""
    movie_db = MovieDatabaseAPI()
    peliculas = movie_db.get_popular_movies()
    
    print("\nPelículas populares disponibles:")
    for i, pelicula in enumerate(peliculas):
        print(f"{i+1}. {pelicula.title} - Rating: {pelicula.rating}")
    
    calificaciones = []
    for pelicula in peliculas[:10]:  
        while True:
            try:
                rating = int(input(f"Califica la película {pelicula.title} (1-5): "))
                if rating < 1 or rating > 5:
                    raise ValueError
                break
            except ValueError:
                print("Por favor, introduce un número entre 1 y 5.")
        
        calificaciones.append({'usuario_id': email, 'pelicula_id': pelicula.id, 'calificacion': rating})
    
    # Cargar calificaciones existentes y agregar las nuevas
    calificaciones_existentes = cargar_calificaciones()
    nuevas_calificaciones = pd.DataFrame(calificaciones)
    todas_calificaciones = pd.concat([calificaciones_existentes, nuevas_calificaciones])
    
    # Guardar calificaciones en el archivo
    guardar_calificaciones(todas_calificaciones)

def generar_recomendacion(email):
    """Genera recomendaciones basadas en las calificaciones guardadas y mide el rendimiento."""
    calificaciones_df = cargar_calificaciones()

    if email not in calificaciones_df['usuario_id'].values:
        print("El usuario no tiene suficientes calificaciones para generar recomendaciones.")
        return
    
    sistema_recomendacion = RecommendationSystem(calificaciones_df)
    
    # Medición del tiempo de respuesta
    start_time = time.time()
    recomendaciones = sistema_recomendacion.recomendar_peliculas(email)
    end_time = time.time()
    
    # Mostrar recomendaciones generadas
    print("\nPelículas recomendadas para ti:")
    if recomendaciones:
        for rec in recomendaciones:
            print(f"Película: {rec[1]} (ID: {rec[0]}) - Rating: {rec[2]}")
    else:
        print("No se encontraron nuevas películas para recomendar.")

    # Cálculo del tiempo de respuesta
    tiempo_respuesta = end_time - start_time
    print(f"\nTiempo de respuesta para generar recomendaciones: {tiempo_respuesta:.2f} segundos")

def main():
    print("Bienvenido al sistema de recomendación de películas.\n")
    
    while True:
        opcion = input("Selecciona una opción: \n1. Iniciar sesión\n2. Generar recomendaciones\n3. Ejecutar pruebas de precisión\n4. Salir\n")
        
        if opcion == "1":
            # Registro o inicio de sesión
            while True:
                tiene_cuenta = input("¿Tienes cuenta? (s/n): ").lower()
                if tiene_cuenta == "s":
                    email = input("Introduce tu email: ")
                    password = input("Introduce tu contraseña: ")
                    if User.verificar_usuario(email, password):
                        print("Inicio de sesión exitoso.")
                        calificar_peliculas(email)  # Calificar películas después de iniciar sesión
                        break
                    else:
                        print("Usuario o contraseña incorrectos.")
                elif tiene_cuenta == "n":
                    email = input("Introduce tu email para registrar: ")
                    password = input("Introduce una contraseña: ")
                    user = User(email, password)
                    User.guardar_usuario(user)
                    print("Usuario registrado exitosamente.")
                    calificar_peliculas(email)  # Calificar películas después de registrarse
                    break
                else:
                    print("Opción no válida.")
        
        elif opcion == "2":
            email = input("Introduce tu email para obtener recomendaciones: ")
            generar_recomendacion(email)

        elif opcion == "3":
            # Ejecutar pruebas de precisión solo con el usuario "agusricc@hotmail.es"
            print("Ejecutando pruebas de precisión para el usuario 'agusricc@hotmail.es'...\n")
            prueba_precision(usuario_email="agusricc@hotmail.es")

        elif opcion == "4":
            print("Saliendo del sistema.")
            break
        
        else:
            print("Opción no válida. Inténtalo de nuevo.")
 
if __name__ == "__main__":
    main()
