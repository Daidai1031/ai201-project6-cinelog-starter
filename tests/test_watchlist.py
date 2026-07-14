"""
tests/test_watchlist.py — CineLog

Tests for the watchlist service.
"""

from datetime import datetime, timedelta, timezone

import pytest
from app import create_app, db
from models import Film, User, WatchlistEntry
from services.collection_service import FilmNotFoundError
from services.watchlist_service import add_to_watchlist, get_watchlist


@pytest.fixture
def app():
    """Create an isolated test app with an in-memory database."""
    app = create_app(config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_user(app):
    """A user to use in tests."""
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def sample_film(app):
    """A film to use in tests."""
    with app.app_context():
        film = Film(title="Paddington 2", year=2017, genre="Comedy")
        db.session.add(film)
        db.session.commit()
        return film.id


def test_add_to_watchlist_nonexistent_film_raises(app, sample_user):
    """
    Adding a film_id that doesn't exist in the database should raise
    FilmNotFoundError, not a database integrity error.
    """
    with app.app_context():
        fake_film_id = "00000000-0000-0000-0000-000000000000"

        with pytest.raises(FilmNotFoundError):
            add_to_watchlist(user_id=sample_user, film_id=fake_film_id)


def test_get_watchlist_orders_newest_first(app, sample_user):
    """
    get_watchlist() should return entries ordered by date_added descending,
    so the most recently added film appears first.
    """
    with app.app_context():
        older_film = Film(title="A Older Film", year=2000, genre="Drama")
        newer_film = Film(title="Z Newer Film", year=2020, genre="Drama")
        db.session.add_all([older_film, newer_film])
        db.session.commit()

        now = datetime.now(timezone.utc)
        older_entry = WatchlistEntry(
            user_id=sample_user,
            film_id=older_film.id,
            date_added=now - timedelta(days=1),
        )
        newer_entry = WatchlistEntry(
            user_id=sample_user,
            film_id=newer_film.id,
            date_added=now,
        )
        db.session.add_all([older_entry, newer_entry])
        db.session.commit()

        watchlist = get_watchlist(sample_user)

        assert [film["title"] for film in watchlist] == [
            "Z Newer Film",
            "A Older Film",
        ]
