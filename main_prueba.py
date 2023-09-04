import requests
import pandas as pd
from datetime import datetime


def Score_y_Url(row):
    base_url = "http://image.tmdb.org/t/p/"
    secure_base_url = "https://image.tmdb.org/t/p/"
    poster_sizes = ["w92", "w154", "w185", "w342", "w500", "w780", "original"]

    nombre = row["Titulo"]
    año = row['Año']
    tipo = row["Tipo"]
    posterURL = ""
    score = ""

    if nombre != "":
        if tipo == "Pelicula":
            if año != "":
                año_str = str(año)  # Convertir el año a una cadena
                url = f"https://api.themoviedb.org/3/search/movie?query={nombre}&include_adult=false&language=es-ES&page=1&year={año_str}"
            else:
                url = f"https://api.themoviedb.org/3/search/movie?query={nombre}&include_adult=false&language=es-ES&page=1"
        if tipo == "Serie":
            if año != "":
                año_str = str(año)  # Convertir el año a una cadena
                url = f"https://api.themoviedb.org/3/search/tv?query={nombre}&include_adult=false&language=es-ES&page=1&year={año_str}"
            else:
                url = f"https://api.themoviedb.org/3/search/tv?query={nombre}&include_adult=false&language=es-ES&page=1"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYmY4MTJmMTFiOWMwMjE3Zjk1YWM3MjBiYzhlZWNhZiIsInN1YiI6IjVhYTVhZWMzMGUwYTI2MDc0YjAyZDc4YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.bdB6qvk3WIdgL5BXXSFB4wZ1JUt9FqS4Er8u-YurVNg"
            # Tu clave de API de TMDB
        }

        response = requests.get(url, headers=headers).json()

        # Imprimir la respuesta de la API para depuración
        print("Respuesta de la API de TMDB:")
        print(response)

        if 'results' in response and len(response['results']) != 0:
            poster_path = response['results'][0]['poster_path']
            if poster_path:
                posterURL = secure_base_url + poster_sizes[
                    2] + poster_path  # Puedes ajustar el tamaño del póster según tus necesidades
            score_int = response['results'][0]['vote_average']
            score = f'{score_int:.1f}'

            # Imprimir información cuando se obtiene la URL
            print(f"Obteniendo URL para '{nombre}' ({tipo}), Año: {año}")
            print(f"URL: {posterURL}")

    return pd.Series([score, posterURL], index=['Score', 'Url'])


# Prueba con título "Guardianes de la Galaxia" y año 2023
test_row = {
    "Titulo": "Guardianes de la Galaxia: Volumen 3",
    "Año": 2023,
    "Tipo": "Pelicula"
}

test_score, test_url = Score_y_Url(test_row)

# Imprimir resultados de la prueba
print(f"Resultados de la prueba:")
print(f"Título: {test_row['Titulo']}")
print(f"Año: {test_row['Año']}")
print(f"Score: {test_score}")
print(f"URL: {test_url}")

# Leer el archivo CSV original
df = pd.read_csv("torrentdb.csv", sep=';', engine='python', encoding='ISO-8859-1')

df['Año'] = df['Año'].apply(lambda x: str(int(x)) if not pd.isna(x) else '')
df['Capitulo'] = df['Capitulo'].apply(lambda x: str(int(x)) if not pd.isna(x) else '')
df['Titulo'] = df['Titulo'].apply(lambda x: str(x) if not pd.isna(x) else '')

# Abre el archivo de resultados para escritura
with open('torrentdb_updated.csv', 'w', encoding='ISO-8859-1') as result_file:
    result_file.write("Score;Url\n")  # Escribir la primera línea con encabezados

    for index, row in df.iterrows():
        # Obtiene la hora actual en milisegundos
        current_time = datetime.now().strftime('%H:%M:%S.%f')[:-3]

        # Aplica la función Score_y_Url para obtener Score y Url
        score, url = Score_y_Url(row)

        # Imprimir información cuando se escribe una fila en el CSV
        print(f"Guardando fila en CSV: Título: {row['Titulo']}, Año: {row['Año']}, Fecha: {current_time}, URL: {url}")

        # Escribe la información en el archivo de resultados
        result_file.write(f"{score};{url}\n")
