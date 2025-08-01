import logging
import re
from datetime import timedelta

from django.utils.timezone import now

from movies.models import Genre, SearchTerm, Movie
from omdb.django_client import get_client_from_settings

logger = logging.getLogger(__name__)

def get_or_create_genres(genre_names):
    for genre_name in genre_names:
        genre, created = Genre.objects.get_or_create(name=genre_name)
        yield genre


def fill_movie_details(movie):
    """
    Fetch a movie's full details from OMDb. Then, save it to the DB. If the movie already has a `full_record` this does
    nothing, so it's safe to call with any `Movie`.
    """
    if movie.is_full_record:
        logger.warning(
            "'%s' is already a full record.",
            movie.title,
        )
        return
    omdb_client = get_client_from_settings()
    movie_details = omdb_client.get_by_imdb_id(movie.imdb_id)
    movie.title = movie_details.title
    movie.year = movie_details.year
    movie.plot = movie_details.plot
    movie.runtime_minutes = movie_details.runtime_minutes
    movie.genres.clear()
    for genre in get_or_create_genres(movie_details.genres):
        movie.genres.add(genre)
    movie.is_full_record = True
    movie.save()

def search_and_save(search):
    """
    Perform a search for search_term against the API, but only if it hasn't been searched in the past 24 hours. Save
    each result to the local DB as a partial record.
    """
    # Replace multiple spaces with single spaces, and lowercase the search
    normalized_search_term = re.sub(r"\s+", " ", search.lower())

    search_term, created = SearchTerm.objects.get_or_create(term=normalized_search_term)

    if not created and (search_term.last_search > now() - timedelta(days=1)):
        # Don't search as it has been searched recently
        logger.warning(
            "Search for '%s' was performed in the past 24 hours so not searching again.",
            normalized_search_term,
        )
        return

    omdb_client = get_client_from_settings()

    for omdb_movie in omdb_client.search(search):
        logger.info("Saving movie: '%s' / '%s'", omdb_movie.title, omdb_movie.imdb_id)
        movie, created = Movie.objects.get_or_create(
            imdb_id=omdb_movie.imdb_id,
            defaults={
                "title": omdb_movie.title,
                "year": omdb_movie.year,
            },
        )

        if created:
            logger.info("Movie created: '%s'", movie.title)

    search_term.save()
