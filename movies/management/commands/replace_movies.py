from django.core.management.base import BaseCommand
from datetime import date

from movies.models import Movie


class Command(BaseCommand):
    help = "Replace all movies with a specific curated set"

    def handle(self, *args, **options):
        self.stdout.write("Clearing existing movies…")
        Movie.objects.all().delete()

        self.stdout.write("Creating selected movies…")
        selected_movies = [
            {
                "title": "The Black Hen",
                "genre": "drama",
                "language": "nepali",
                "duration": 90,
                "rating": 8.0,
                "description": "A poignant story set during the Nepali civil war, exploring innocence, loss, and friendship.",
                "release_date": date(2015, 9, 3),
                "poster_url": "",
            },
            {
                "title": "Kabaddi",
                "genre": "drama",
                "language": "nepali",
                "duration": 120,
                "rating": 7.5,
                "description": "A returning villager navigates love, tradition, and rivalry in rural Nepal.",
                "release_date": date(2013, 8, 30),
                "poster_url": "",
            },
            {
                "title": "Talakjung vs Tulke",
                "genre": "drama",
                "language": "nepali",
                "duration": 140,
                "rating": 8.2,
                "description": "A powerful tale of identity and upheaval during times of political conflict.",
                "release_date": date(2014, 12, 19),
                "poster_url": "",
            },
            {
                "title": "Loot",
                "genre": "comedy",
                "language": "nepali",
                "duration": 135,
                "rating": 7.8,
                "description": "A stylish heist caper that changed modern Nepali cinema.",
                "release_date": date(2012, 9, 7),
                "poster_url": "",
            },
            {
                "title": "Pashupati Prasad",
                "genre": "drama",
                "language": "nepali",
                "duration": 125,
                "rating": 8.0,
                "description": "An earnest man in Kathmandu struggles with hardship and hope.",
                "release_date": date(2016, 1, 29),
                "poster_url": "",
            },
            {
                "title": "Small World",
                "genre": "drama",
                "language": "nepali",
                "duration": 110,
                "rating": 7.4,
                "description": "Interwoven lives reflect dreams and realities in a changing Nepal.",
                "release_date": date(2014, 6, 1),
                "poster_url": "",
            },
        ]

        for data in selected_movies:
            Movie.objects.create(**data)
            self.stdout.write(f"Created: {data['title']}")

        self.stdout.write(self.style.SUCCESS("Successfully replaced movies with the selected set."))

