import os
import requests
from dotenv import load_dotenv
from movie import Movie

class MovieDatabaseAPI:
    def __init__(self):
        load_dotenv()
        self.api_token = os.getenv('TMDB_API_TOKEN')

    def obtener_peliculas_populares(self):
        url = "https://api.themoviedb.org/3/movie/popular"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }

        try:
            response = requests.get(url, headers=headers)

            # Verifica si la respuesta fue exitosa (código de estado 200)
            if response.status_code == 200:
                peliculas_data = response.json()['results']
                peliculas = []
                
                # Crea una lista de objetos Movie con los datos recibidos
                for p in peliculas_data:
                    pelicula = Movie(
                        id=p['id'],
                        title=p['title'],
                        overview=p['overview'],
                        release_date=p['release_date'],
                        rating=p['vote_average']
                    )
                    peliculas.append(pelicula)

                return peliculas
            
            # Si hay un error, muestra el código de estado
            else:
                print(f"Error en la API: Código de estado {response.status_code}, Detalle: {response.json()}")
                return []

        except requests.exceptions.RequestException as e:
            # Manejo de excepciones de red o API
            print(f"Error al conectar con la API de TMDb: {e}")
            return []

    def get_popular_movies(self):
        return self.obtener_peliculas_populares()

    def obtener_nuevas_peliculas(self, peliculas_calificadas):
        url = "https://api.themoviedb.org/3/account/21584305/rated/movies?language=en-US&page=1&sort_by=created_at.asc"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }

        try:
            response = requests.get(url, headers=headers)

            # Verifica si la respuesta fue exitosa (código de estado 200)
            if response.status_code == 200:
                peliculas_data = response.json()['results']
                nuevas_peliculas = []

                # Crea una lista de objetos Movie con los datos recibidos
                for p in peliculas_data:
                    if p['id'] not in peliculas_calificadas:
                        pelicula = Movie(
                            id=p['id'],
                            title=p['title'],
                            overview=p['overview'],
                            release_date=p['release_date'],
                            rating=p['vote_average']
                        )
                        nuevas_peliculas.append(pelicula)

                return nuevas_peliculas
            else:
                print(f"Error en la API: Código de estado {response.status_code}, Detalle: {response.json()}")
                return []

        except requests.exceptions.RequestException as e:
            # Manejo de excepciones de red o API
            print(f"Error al conectar con la API de TMDb: {e}")
            return []

    def get_new_movies(self, peliculas_calificadas, n=5):
        """Retorna una lista de nuevas películas no calificadas, hasta un máximo de n."""
        nuevas_peliculas = self.obtener_nuevas_peliculas(peliculas_calificadas)
        return nuevas_peliculas[:n]
