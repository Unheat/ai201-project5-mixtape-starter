"""
tests/test_feed.py — Mixtape

Exploratory tests for get_friends_listening_now, just to see how it's
called and what it returns. Run with: pytest tests/test_feed.py -s
"""

import pytest
from datetime import datetime, timedelta, timezone
from app import create_app, db
from models import User, Song, ListeningEvent, friendships
from services.feed_service import get_friends_listening_now


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def users(app):
    with app.app_context():
        me = User(username="me", email="me@example.com")
        friend = User(username="friend", email="friend@example.com")
        db.session.add_all([me, friend])
        db.session.flush()
        db.session.execute(friendships.insert().values(user_id=me.id, friend_id=friend.id))
        db.session.execute(friendships.insert().values(user_id=friend.id, friend_id=me.id))
        db.session.commit()
        yield me, friend


def _listen(user, song, when):
    db.session.add(ListeningEvent(user_id=user.id, song_id=song.id, listened_at=when))
    db.session.commit()


def test_recent_friend_listen_shows_up(app, users):
    """A friend who listened a few minutes ago should appear."""
    with app.app_context():
        me, friend = users
        song = Song(title="Test Song", artist="Test Artist", shared_by=me.id)
        db.session.add(song)
        db.session.commit()

        _listen(friend, song, datetime.now(timezone.utc) - timedelta(minutes=5))

        result = get_friends_listening_now(me.id)
        print("recent listen result:", result)
        assert len(result) == 1
        assert result[0]["friend"]["username"] == "friend"


def test_old_friend_listen_does_not_show_up(app, users):
    """A friend who listened a long time ago should NOT appear."""
    with app.app_context():
        me, friend = users
        song = Song(title="Old Song", artist="Test Artist", shared_by=me.id)
        db.session.add(song)
        db.session.commit()

        _listen(friend, song, datetime.now(timezone.utc) - timedelta(days=3))

        result = get_friends_listening_now(me.id)
        print("old listen result:", result)
        assert result == []
