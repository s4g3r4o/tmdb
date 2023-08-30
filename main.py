import requests
def getPoster():
    # Use a breakpoint in the code line below to debug your script.
    base_url="http://image.tmdb.org/t/p/"
    secure_base_url="https://image.tmdb.org/t/p/"
    poster_sizes=["w92","w154","w185","w342","w500","w780","original"]
    movie="Caballeros del zodiaco"
    url = "https://api.themoviedb.org/3/search/movie?query="+movie+"&include_adult=false&language=es-ES&page=1&year=2023"

    headers = {
        "accept": "application/json",
        #"Authorization": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }

    response = requests.get(url, headers=headers).json()

    #print(response.text)
    #print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(base_url+poster_sizes[3]+response['results'][0]['poster_path'])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    getPoster()
