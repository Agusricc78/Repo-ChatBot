import csv

import pandas as pd

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def guardar_usuario(user):
        with open('data/usuarios.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user.email, user.password])

    @staticmethod
    def verificar_usuario(email, password):
        try:
            with open('data/usuarios.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == email and row[1] == password:
                        return True
        except FileNotFoundError:
            return False
        return False
    
    @staticmethod
    def guardar_calificaciones(calificaciones):
        with open('calificaciones.csv', 'a', newline='') as archivo_csv:
            writer = csv.DictWriter(archivo_csv, fieldnames=['usuario_id', 'pelicula_id', 'calificacion'])
            writer.writerows(calificaciones)

    @staticmethod
    def cargar_calificaciones():
        try:
            return pd.read_csv('calificaciones.csv')
        except FileNotFoundError:
            return pd.DataFrame(columns=['usuario_id', 'pelicula_id', 'calificacion'])
    
    
    
    
