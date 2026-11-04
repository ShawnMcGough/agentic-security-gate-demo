"""A synthetic, in-memory employee directory for teaching; not a service."""

import argparse
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


def search_people(connection, name):
    return connection.execute(
        "SELECT id, name, team FROM people WHERE name = ? ORDER BY id", (name,)
    ).fetchall()


def main():
    parser = argparse.ArgumentParser(description="Search the synthetic directory.")
    parser.add_argument("--name", help="Exact name to find; omit to list everyone.")
    args = parser.parse_args()
    connection = create_directory()
    try:
        people = (
            list_people(connection)
            if args.name is None
            else search_people(connection, args.name)
        )
        for person_id, name, team in people:
            print(f"{person_id}: {name} ({team})")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
