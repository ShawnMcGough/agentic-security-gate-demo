"""A synthetic, in-memory employee directory for teaching; not a service."""

import sqlite3


def create_directory():
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT, team TEXT)"
    )
    connection.executemany(
        "INSERT INTO people (name, team) VALUES (?, ?)",
        [("Ada", "Engineering"), ("Grace", "Research"), ("Linus", "Operations")],
    )
    return connection


def list_people(connection):
    return connection.execute(
        "SELECT id, name, team FROM people ORDER BY id"
    ).fetchall()


def main():
    connection = create_directory()
    try:
        for person_id, name, team in list_people(connection):
            print(f"{person_id}: {name} ({team})")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
