"""seed.py — create a demo user and films for manually testing the watchlist.

Run from the repo root with the app's environment active:

    python seed.py

It prints the UUIDs to use in the curl commands from the PR description.
"""

from app import create_app, db
from models import User, Film

app = create_app()
with app.app_context():
    u = User(username="alice", email="alice@example.com")
    f1 = Film(title="Paddington 2", year=2017, genre="Comedy")
    f2 = Film(title="Arrival", year=2016, genre="Sci-Fi")
    db.session.add_all([u, f1, f2])
    db.session.commit()
    print("USER_ID =", u.id)
    print("FILM_1  =", f1.id)
    print("FILM_2  =", f2.id)
