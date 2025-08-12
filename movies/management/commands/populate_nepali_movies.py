from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from movies.models import Movie

class Command(BaseCommand):
    help = 'Populate database with Nepali movies'

    def handle(self, *args, **options):
        self.stdout.write('Creating Nepali movies...')
        
        # Nepali movies data with poster URLs
        nepali_movies = [
            {
                'title': 'Loot',
                'genre': 'comedy',
                'language': 'nepali',
                'duration': 135,
                'rating': 7.8,
                'description': 'A comedy film about a group of friends who plan a heist to solve their financial problems. Directed by Nischal Basnet, this film became one of the highest-grossing Nepali films.',
                'release_date': date(2012, 9, 7),
                'poster_url': 'https://images.unsplash.com/photo-1489599835382-957593cb2371?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Kabaddi',
                'genre': 'drama',
                'language': 'nepali',
                'duration': 120,
                'rating': 7.5,
                'description': 'A drama about a young man who returns to Nepal after living abroad and gets involved in the traditional sport of Kabaddi. The film explores themes of identity and cultural connection.',
                'release_date': date(2013, 8, 30),
                'poster_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Talakjung vs Tulke',
                'genre': 'drama',
                'language': 'nepali',
                'duration': 140,
                'rating': 8.2,
                'description': 'A critically acclaimed film about the Nepali Civil War, exploring the impact of conflict on ordinary people. The film was Nepal\'s official entry for the Academy Awards.',
                'release_date': date(2014, 12, 19),
                'poster_url': 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Pashupati Prasad',
                'genre': 'drama',
                'language': 'nepali',
                'duration': 125,
                'rating': 8.0,
                'description': 'A heartwarming story about a simple man named Pashupati Prasad who works as a helper in a restaurant and dreams of a better life for his family.',
                'release_date': date(2016, 8, 12),
                'poster_url': 'https://images.unsplash.com/photo-1504674900240-9c9c0b1c6b8b?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Chhakka Panja',
                'genre': 'comedy',
                'language': 'nepali',
                'duration': 130,
                'rating': 7.6,
                'description': 'A comedy film about a group of friends who get involved in various humorous situations. The film became a commercial success and spawned sequels.',
                'release_date': date(2016, 9, 9),
                'poster_url': 'https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Prem Geet',
                'genre': 'romance',
                'language': 'nepali',
                'duration': 145,
                'rating': 7.4,
                'description': 'A romantic drama about love, sacrifice, and destiny. The film features beautiful cinematography and emotional storytelling.',
                'release_date': date(2016, 12, 2),
                'poster_url': 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Chhakka Panja 2',
                'genre': 'comedy',
                'language': 'nepali',
                'duration': 135,
                'rating': 7.2,
                'description': 'The sequel to the successful comedy film, continuing the adventures of the same group of friends with new hilarious situations.',
                'release_date': date(2017, 9, 8),
                'poster_url': 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Bir Bikram',
                'genre': 'action',
                'language': 'nepali',
                'duration': 150,
                'rating': 7.8,
                'description': 'An action film based on the life of Bir Bikram Shah, a historical figure. The film showcases Nepali history and culture through action sequences.',
                'release_date': date(2018, 1, 19),
                'poster_url': 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Chhakka Panja 3',
                'genre': 'comedy',
                'language': 'nepali',
                'duration': 140,
                'rating': 7.0,
                'description': 'The third installment of the popular comedy franchise, bringing more laughter and entertainment to audiences.',
                'release_date': date(2018, 9, 7),
                'poster_url': 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Bulbul',
                'genre': 'romance',
                'language': 'nepali',
                'duration': 130,
                'rating': 7.6,
                'description': 'A romantic film about love that transcends social barriers. The film explores themes of love, family, and societal expectations.',
                'release_date': date(2019, 2, 14),
                'poster_url': 'https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Chhakka Panja 4',
                'genre': 'comedy',
                'language': 'nepali',
                'duration': 145,
                'rating': 6.8,
                'description': 'The fourth part of the comedy series, continuing the tradition of family-friendly entertainment with Nepali humor.',
                'release_date': date(2019, 9, 6),
                'poster_url': 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Aama',
                'genre': 'drama',
                'language': 'nepali',
                'duration': 120,
                'rating': 8.4,
                'description': 'A touching drama about the relationship between a mother and her children, exploring family bonds and sacrifice.',
                'release_date': date(2020, 3, 6),
                'poster_url': 'https://images.unsplash.com/photo-1504674900240-9c9c0b1c6b8b?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Chhakka Panja 5',
                'genre': 'comedy',
                'language': 'nepali',
                'duration': 140,
                'rating': 6.5,
                'description': 'The latest installment in the comedy franchise, bringing more laughter and family entertainment.',
                'release_date': date(2021, 9, 10),
                'poster_url': 'https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Gopi',
                'genre': 'drama',
                'language': 'nepali',
                'duration': 125,
                'rating': 7.9,
                'description': 'A drama about a young man named Gopi who faces various challenges in life and learns important lessons about perseverance and hope.',
                'release_date': date(2022, 1, 14),
                'poster_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            },
            {
                'title': 'Chhakka Panja 6',
                'genre': 'comedy',
                'language': 'nepali',
                'duration': 135,
                'rating': 6.2,
                'description': 'The sixth installment of the popular comedy series, continuing to entertain audiences with Nepali humor and family values.',
                'release_date': date(2022, 9, 9),
                'poster_url': 'https://images.unsplash.com/photo-1489599835382-957593cb2371?w=300&h=450&fit=crop&crop=center&auto=format&q=80'
            }
        ]
        
        created_count = 0
        updated_count = 0
        for movie_data in nepali_movies:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults=movie_data
            )
            if created:
                self.stdout.write(f'Created Nepali movie: {movie.title}')
                created_count += 1
            else:
                # Update existing movie with poster if it doesn't have one
                movie.poster_url = movie_data['poster_url']
                movie.save()
                self.stdout.write(f'Updated poster for existing movie: {movie.title}')
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {len(nepali_movies)} Nepali movies. {created_count} new movies were created, {updated_count} existing movies were updated with posters.')
        ) 