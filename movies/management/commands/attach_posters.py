from django.core.management.base import BaseCommand
from django.conf import settings
import os
import re

from movies.models import Movie


class Command(BaseCommand):
    help = "Attach local poster files in media/movie_posters to Movie.poster"

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"[^a-z0-9]", "", text.lower())

    def handle(self, *args, **options):
        media_dir = os.path.join(settings.MEDIA_ROOT, "movie_posters")
        if not os.path.isdir(media_dir):
            self.stdout.write(self.style.ERROR(f"Directory not found: {media_dir}"))
            return

        files = [
            f for f in os.listdir(media_dir)
            if os.path.isfile(os.path.join(media_dir, f)) and os.path.splitext(f)[1].lower() in {".jpg", ".jpeg", ".png", ".webp"}
        ]

        file_stems = {f: self._normalize(os.path.splitext(f)[0]) for f in files}

        updated_titles = []
        missing_files = []
        missing_movies = []

        for title in [
            "Loot",
            "Talakjung vs Tulke",
            "Kabaddi",
            "The Black Hen",
            "Pashupati Prasad",
            "Small World",
        ]:
            try:
                movie = Movie.objects.get(title=title)
            except Movie.DoesNotExist:
                missing_movies.append(title)
                continue

            norm_title = self._normalize(title)

            # Try exact normalized match first
            chosen_file = None
            for fname, stem in file_stems.items():
                if stem == norm_title:
                    chosen_file = fname
                    break

            # Fallback: stem contains title or vice versa
            if not chosen_file:
                for fname, stem in file_stems.items():
                    if norm_title in stem or stem in norm_title:
                        chosen_file = fname
                        break

            if not chosen_file:
                missing_files.append(title)
                continue

            # Assign by name since file already exists in MEDIA_ROOT
            movie.poster.name = f"movie_posters/{chosen_file}"
            movie.save(update_fields=["poster"])
            updated_titles.append(title)

        if updated_titles:
            self.stdout.write(self.style.SUCCESS(f"Attached posters for: {', '.join(updated_titles)}"))
        if missing_files:
            self.stdout.write(self.style.WARNING(
                f"No poster file found for: {', '.join(missing_files)}"
            ))
        if missing_movies:
            self.stdout.write(self.style.WARNING(
                f"Movies not found (skipped): {', '.join(missing_movies)}"
            ))

