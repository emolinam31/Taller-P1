from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

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