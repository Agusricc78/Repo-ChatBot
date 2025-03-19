from sklearn.decomposition import TruncatedSVD
import pandas as pd

class MatrixFactorizationModel:
    def __init__(self, n_componentes=2):
        self.svd = TruncatedSVD(n_components=n_componentes)

    def ajustar(self, matriz_calificaciones):
        return self.svd.fit_transform(matriz_calificaciones)

    def predecir(self, usuario_id, matriz, caracteristicas_usuarios):
        usuario_index = matriz.index.get_loc(usuario_id)
        usuario_vector = caracteristicas_usuarios.iloc[usuario_index]
        return usuario_vector
