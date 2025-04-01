from django.core.management.base import BaseCommand
from movie.models import Movie
import numpy as np


class Command(BaseCommand):
    help = "Verify and print the embeddings of movies"

    def handle(self, *args, **options):
        for movie in Movie.objects.all():
            try:
                # Convert the binary field to a numpy array
                embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)  # Use np.float64 as default
                print(f"Movie: {movie.title}, Embedding (first 5 values): {embedding_vector[:5]}")
            except Exception as e:
                self.stderr.write(f"Error processing movie '{movie.title}': {str(e)}")