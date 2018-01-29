# Service for retrieving log information

from logsanalysis.db_init import conn


class Author:
    def __init__(self, id: int, name: str, bio: str):
        self.id = id
        self.name = name
        self.bio = bio

    def __str__(self):
        return f"id:{self.id}, name:{self.name}, bio:{self.bio}"


def get_authors():
    cursor = conn.cursor()
    cursor.execute("SELECT a.id, a.name, a.bio FROM authors a ORDER BY a.name")
    authors = []
    for row in cursor.fetchall():
        authors.append(Author(row[0], row[1], row[2]))
    conn.close()
    return authors
