from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time, timedelta
from movies.models import Movie
from theaters.models import Theater
from booking.models import ShowTime, Seat

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create theaters
        theaters = []
        theater_data = [
            {
                'name': 'Cineplex Downtown',
                'address': '123 Main Street',
                'city': 'New York',
                'phone': '+1-555-0101',
                'email': 'downtown@cineplex.com'
            },
            {
                'name': 'AMC Multiplex',
                'address': '456 Broadway Ave',
                'city': 'New York',
                'phone': '+1-555-0102',
                'email': 'multiplex@amc.com'
            },
            {
                'name': 'Regal Cinemas',
                'address': '789 5th Avenue',
                'city': 'New York',
                'phone': '+1-555-0103',
                'email': 'info@regal.com'
            }
        ]
        
        for data in theater_data:
            theater, created = Theater.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            theaters.append(theater)
            if created:
                self.stdout.write(f'Created theater: {theater.name}')
        
        # Create movies
        movies = []
        movie_data = [
            {
                'title': 'The Avengers: Endgame',
                'genre': 'action',
                'language': 'english',
                'duration': 181,
                'rating': 8.4,
                'description': 'After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos\' actions and restore balance to the universe.',
                'release_date': date(2019, 4, 26)
            },
            {
                'title': 'Inception',
                'genre': 'sci-fi',
                'language': 'english',
                'duration': 148,
                'rating': 8.8,
                'description': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
                'release_date': date(2010, 7, 16)
            },
            {
                'title': 'The Dark Knight',
                'genre': 'action',
                'language': 'english',
                'duration': 152,
                'rating': 9.0,
                'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'release_date': date(2008, 7, 18)
            },
            {
                'title': 'La La Land',
                'genre': 'romance',
                'language': 'english',
                'duration': 128,
                'rating': 8.0,
                'description': 'A jazz pianist falls for an aspiring actress in Los Angeles.',
                'release_date': date(2016, 12, 9)
            },
            {
                'title': 'Parasite',
                'genre': 'thriller',
                'language': 'korean',
                'duration': 132,
                'rating': 8.6,
                'description': 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.',
                'release_date': date(2019, 5, 30)
            },
            {
                'title': 'Spirited Away',
                'genre': 'animation',
                'language': 'japanese',
                'duration': 125,
                'rating': 8.6,
                'description': 'During her family\'s move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, where humans are changed into beasts.',
                'release_date': date(2001, 7, 20)
            }
        ]
        
        for data in movie_data:
            movie, created = Movie.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            movies.append(movie)
            if created:
                self.stdout.write(f'Created movie: {movie.title}')
        
        # Create showtimes
        showtime_data = [
            {'time': time(10, 0), 'price': 12.00},
            {'time': time(13, 0), 'price': 15.00},
            {'time': time(16, 0), 'price': 15.00},
            {'time': time(19, 0), 'price': 18.00},
            {'time': time(22, 0), 'price': 12.00},
        ]
        
        # Create showtimes for the next 7 days
        for i in range(7):
            show_date = date.today() + timedelta(days=i)
            
            for movie in movies:
                for theater in theaters:
                    for showtime_info in showtime_data:
                        showtime, created = ShowTime.objects.get_or_create(
                            movie=movie,
                            theater=theater,
                            date=show_date,
                            time=showtime_info['time'],
                            defaults={'price': showtime_info['price']}
                        )
                        
                        if created:
                            # Create seats for this showtime
                            for row in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
                                for seat_num in range(1, 11):
                                    Seat.objects.create(
                                        showtime=showtime,
                                        row=row,
                                        seat_number=seat_num
                                    )
                            
                            self.stdout.write(f'Created showtime: {movie.title} at {theater.name} on {show_date} at {showtime_info["time"]}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data')) 