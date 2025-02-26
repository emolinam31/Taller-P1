import pandas as pd 
import json
# Lee el archivo  CSV 
df = pd.read_csv('movies_initial.csv')

# Guardar el dataframe como JSON
df.to_json('movies_initial.json', orient='records')

with open('movies_initial.json', "r") as file:
    movies = json.load(file)

for i in range(100):
    movie = movies[i]
    print(movie)
    break