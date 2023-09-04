import requests
import pandas as pd

def Score_y_Url(row):
    base_url = "http://image.tmdb.org/t/p/"
    secure_base_url = "https://image.tmdb.org/t/p/"
    poster_sizes = ["w92", "w154", "w185", "w342", "w500", "w780", "original"]

    nombre=row["Titulo"]
    año=row['Año']
    tipo=row["Tipo"]
    posterURL=""
    score=""
    if nombre != "":
        if tipo == "Pelicula":
            if año != "":
                url = "https://api.themoviedb.org/3/search/movie?query=" + nombre + "&include_adult=false&language=es-ES&page=1&year=" + año
            else:
                url = "https://api.themoviedb.org/3/search/movie?query=" + nombre + "&include_adult=false&language=es-ES&page=1"
        if tipo == "Serie":  # pongo Serie y no else por si en el futuro se meten Documentales
            if año != "":
                url = "https://api.themoviedb.org/3/search/tv?query=" + nombre + "&include_adult=false&language=es-ES&page=1&year=" + año
            else:
                url = "https://api.themoviedb.org/3/search/tv?query=" + nombre + "&include_adult=false&language=es-ES&page=1"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYmY4MTJmMTFiOWMwMjE3Zjk1YWM3MjBiYzhlZWNhZiIsInN1YiI6IjVhYTVhZWMzMGUwYTI2MDc0YjAyZDc4YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.bdB6qvk3WIdgL5BXXSFB4wZ1JUt9FqS4Er8u-YurVNg"
        }

        response = requests.get(url, headers=headers).json()

        if len(response['results']) != 0:
            posterURL = base_url + poster_sizes[0] + response['results'][0]['poster_path']
            score_int = response['results'][0]['vote_average']
            score=f'{score_int:.1f}'

    return pd.Series([score, posterURL], index=['Score', 'Url'])

def ChangeCSVPanda():
    df = pd.read_csv("torrentdb.csv",sep='[;]',engine='python', encoding='ISO-8859-1')

    df['Año'] = df['Año'].apply(lambda x: str(int(x)) if pd.notna(x) else '')
    df['Capitulo'] = df['Capitulo'].apply(lambda x: str(int(x)) if pd.notna(x) else '')
    df = df.applymap(lambda x: str(x) if pd.notna(x) else '')
    # Aplicar la función para crear las columnas "score" y "url"
    df[['Score', 'Url']] = df.apply(Score_y_Url, axis=1)

    df.to_csv('torrentdb_updated.csv', index=False, sep=";", encoding='ISO-8859-1')

if __name__ == '__main__':
    ChangeCSVPanda()
