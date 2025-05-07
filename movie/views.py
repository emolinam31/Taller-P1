from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv


def home(request):
    movies = Movie.objects.all()
    return render(request, "home.html", {'movies': movies})
   

def about(request):
    return render(request, "about.html")

def statistics_views(request):
    matplotlib.use('Agg')  # Esto es necesario para renderizar el gráfico en el navegador

    # Gráfico de películas por año
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "none"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.figure(figsize=(10, 5))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, color='b', align='center')
    plt.title('Movies by Year')
    plt.xlabel('Year')
    plt.ylabel('# of Movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png_mpy = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png_mpy).decode('utf-8')

    # Gráfico de películas por género
    genres = Movie.objects.values_list('genre', flat=True)
    genre_counts = {}
    for genre in genres:
        if genre:
            first_genre = genre.split(',')[0].strip()
            if first_genre in genre_counts:
                genre_counts[first_genre] += 1
            else:
                genre_counts[first_genre] = 1

    bar_positions = range(len(genre_counts))

    plt.figure(figsize=(10, 5))
    plt.bar(bar_positions, genre_counts.values(), width=bar_width, color='g', align='center')
    plt.title('Movies by Genre')
    plt.xlabel('Genre')
    plt.ylabel('# of Movies')
    plt.xticks(bar_positions, genre_counts.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png_mpg = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png_mpg).decode('utf-8')

    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})

def signup(request):
    email = request.GET.get("email")
    return render(request, 'signup.html', {'email': email})



def iarecommendation(request):
    # Cargar la API Key desde múltiples posibles fuentes
    # 1. Obtener ruta al archivo de configuración
    api_key_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'api_keys.env')
    
    # 2. Intentar cargar desde el archivo
    if os.path.exists(api_key_file):
        load_dotenv(api_key_file)
    
    # 3. Intentar obtener la clave API de diferentes formas
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        api_key = os.environ.get('openai_apikey')
    
    # 4. Si aún no se encuentra, leer directamente del archivo
    if not api_key and os.path.exists(api_key_file):
        try:
            with open(api_key_file, 'r') as file:
                for line in file:
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        if key.lower() in ['openai_api_key', 'api_key', 'openai_apikey']:
                            api_key = value.strip()
        except Exception as e:
            print(f"Error leyendo API key: {e}")
    
    # 5. Inicializar cliente de OpenAI con la clave obtenida
    client = OpenAI(api_key=api_key)

    # Función para calcular similitud de coseno
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    # Recibir el prompt del usuario desde el formulario
    prompt = request.GET.get("prompt", "")  # Obtiene el valor del formulario (GET)

    best_movie = None
    max_similarity = -1

    if prompt:  # Solo procesar si el usuario ingresó un prompt
        # Generar embedding del prompt
        response = client.embeddings.create(
            input=[prompt],
            model="text-embedding-3-small"
        )
        prompt_emb = np.array(response.data[0].embedding, dtype=np.float32)

        # Recorrer la base de datos y comparar
        for movie in Movie.objects.all():
            movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
            similarity = cosine_similarity(prompt_emb, movie_emb)

            if similarity > max_similarity:
                max_similarity = similarity
                best_movie = movie

    # Preparar el contexto para la plantilla
    context = {
        'prompt': prompt,
        'best_movie': best_movie,
        'max_similarity': max_similarity if best_movie else None,
    }

    return render(request, 'iarecommendation.html', context)