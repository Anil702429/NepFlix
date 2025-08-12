from django.core.management.base import BaseCommand
from datetime import date

from movies.models import Movie


class Command(BaseCommand):
    help = "Enrich existing Movie records with details from IMDb list (year, runtime, rating, synopsis)"

    def handle(self, *args, **options):
        # Data extracted from IMDb list: https://www.imdb.com/list/ls071994910/
        # Durations converted to minutes; release_date set to Jan 1 of the year.
        data = {
            "The Black Hen": {
                "year": 2015,
                "duration": 90,  # 1h 30m
                "rating": 6.9,
                "description": (
                    "They are bonded, nonetheless, by friendship and affection for a hen, "
                    "whose eggs just might make a difference to Prakash's impoverished family. "
                    "When the boy's father sells the bird, the chums desperately attempt to raise "
                    "funds in order to buy it back."
                ),
                "director": "Min Bahadur Bham",
                "cast": ["Khadka Raj Nepali", "Sukra Raj Rokaya", "Jit Bahadur Malla"],
            },
            "Kabaddi": {
                "year": 2014,
                "duration": 123,  # 2h 3m
                "rating": 8.2,
                "description": (
                    "Kaji, a young aimless man, dreams of marrying Maiya, a village girl, although "
                    "she wants to go to the city for higher education. Their lives are thrown into turmoil "
                    "with the arrival of Bibek, a charming young man from the city."
                ),
                "director": "Ram Babu Gurung",
                "cast": ["Dayahang Rai", "Nischal Basnet", "Rishma Gurung"],
            },
            "Talakjung vs Tulke": {
                "year": 2014,
                "duration": 133,  # 2h 13m
                "rating": 8.0,
                "description": (
                    "Tulké is a day laborer in a Nepalese mountain village. He struggles to reclaim his "
                    "lost aristocratic identity, while a violent revolution disrupts every aspect of village life."
                ),
                "director": "Nischal Basnet",
                "cast": ["Khagendra Lamichhane", "Dayahang Rai", "Shushank Mainali"],
            },
            "Loot": {
                "year": 2012,
                "duration": 138,  # 2h 18m
                "rating": 8.1,
                "description": (
                    "A man with a 'master plan' to rob a bank searches for and leads four frustrated men "
                    "in their quest for quick money."
                ),
                "director": "Nischal Basnet",
                "cast": ["Saugat Malla", "Karma Shakya", "Dayahang Rai"],
            },
            "Pashupati Prasad": {
                "year": 2016,
                "duration": 140,  # 2h 20m
                "rating": 8.5,
                "description": (
                    "When a man named Pashupati travels to Kathmandu to repay his father's debts, he discovers "
                    "the sacred site of Pashupatinath and confronts the dangers that lurk in the city."
                ),
                "director": "Dipendra K. Khanal",
                "cast": ["Khagendra Lamichhane", "Rabindra Singh Baniya", "Bipin Karki"],
            },
            "Small World": {
                "year": 2008,
                "duration": 144,  # 2h 24m
                "rating": 7.1,
                "description": (
                    "Ravi and Reetu are good chat friends but have no idea that they dislike each other "
                    "in real life."
                ),
                "director": "Alok Nembang",
                "cast": ["Karma Shakya", "Namrata Shrestha", "Neer Bikram Shah"],
            },
        }

        updated = []
        missing = []

        for title, info in data.items():
            try:
                movie = Movie.objects.get(title=title)
            except Movie.DoesNotExist:
                missing.append(title)
                continue

            movie.duration = info["duration"]
            movie.rating = info["rating"]
            movie.description = info["description"]
            movie.release_date = date(info["year"], 1, 1)
            # Director & Cast
            if info.get("director"):
                movie.director = info["director"]
            if info.get("cast"):
                movie.cast = ", ".join(info["cast"])

            movie.language = movie.language or "nepali"
            movie.save(update_fields=[
                "duration",
                "rating",
                "description",
                "release_date",
                "language",
                "director",
                "cast",
            ])
            updated.append(title)

        if updated:
            self.stdout.write(self.style.SUCCESS(f"Updated: {', '.join(updated)}"))
        if missing:
            self.stdout.write(self.style.WARNING(f"Missing movies (not updated): {', '.join(missing)}"))

