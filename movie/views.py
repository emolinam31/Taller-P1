from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64


def home(request):
    # return HttpResponse("<h1>Welcome To The Home Page<h1>")
    # return render(request, "home.html",  {'name':'Esteban Molina'})
    # searchTerm = request.GET.get("searchMovie")
    # movies = Movie.objects,all()
    # return render(request, "home.html", {"searchTerm":searchTerm, "movies": movies})
    searchTerm = request.GET.get('searchMovie')

    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})


def about(request):
    return render(request, "about.html")


def statistics_views(request):
    matplotlib.use('Agg')  # This is required to render the plot in the browser
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')  # Get the years of the movies
    movie_counts_by_year = {}  # Dictionary to store the number of movies per year
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "none"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count
    bar_width = 0.5  # Width of the bars
    bar_spacing = 0.5  # Spacing between the bars
    bar_positions = range(len(movie_counts_by_year))  # Positions of the bars

    # Create the bar chart
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, color='b', align='center')

    # Customize the chart
    plt.title('Movies by Year')
    plt.xlabel('Year')
    plt.ylabel('# of Movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    # Adjust the space between the bars
    plt.subplots_adjust(bottom=0.3)

    # Save the chart to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convert the chart to base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Render the template with the chart
    return render(request, 'statistics.html', {'graphic': graphic})

