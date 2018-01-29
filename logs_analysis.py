# /usr/bin/python3.6.2
#
#

import psycopg2

DB_SERVER = ''  # TODO Fill this in
DB_PORT = ''  # TODO Fill this in
DB_NAME = ''  # TODO Fill this in
DB_USER = ''  # TODO Fill this in
DB_PASSWORD = ''  # TODO Fill this in

SQL_GET_MOST_POPULAR_ARTICLES = """
    SELECT art.title, COUNT(*) AS num_views
    FROM articles art, log l
    WHERE art.slug = REPLACE(l.path, '/article/', '')
    GROUP BY art.title
    ORDER BY num_views DESC
"""

SQL_GET_MOST_POPULAR_AUTHORS = """
    SELECT auth.name, COUNT(*) AS num_views
    FROM authors auth, articles art, log l
    WHERE auth.id = art.author
        AND art.slug = REPLACE(l.path, '/article/', '')
    GROUP BY auth.name
    ORDER BY num_views DESC
"""

SQL_GET_DAYS_WITH_HIGH_ERRORS = """
    TODO
"""


def get_db_connection():
    return psycopg2.connect(
        f"dbname='{DB_NAME}' user='{DB_USER}' host='{DB_SERVER}' " +
        F"port='{DB_PORT}' password='{DB_PASSWORD}'")


def get_most_popular_articles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(SQL_GET_MOST_POPULAR_ARTICLES)
    rows = cursor.fetchall()
    conn.close()
    return [(row[0], row[1]) for row in rows]


def get_most_popular_authors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(SQL_GET_MOST_POPULAR_AUTHORS)
    rows = cursor.fetchall()
    conn.close()
    return [(row[0], row[1]) for row in rows]


def get_days_with_high_errors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(SQL_GET_DAYS_WITH_HIGH_ERRORS)
    rows = cursor.fetchall()
    conn.close()
    return [(row[0], row[1]) for row in rows]


if __name__ == "__main__":
    # 1. List most popular articles
    print("Most popular articles:")
    for article in get_most_popular_articles():
        print(f"\"{article[0]}\" - {article[1]} views")

    # 2. List most popular authors
    print("\nMost popular authors:")
    for author in get_most_popular_authors():
        print(f"\"{author[0]}\" - {author[1]} views")

    # 3. List days with HTTP error response rate >= 1%
    print('\nDays with error response rate >= 1%:')
    for day in get_days_with_high_errors():
        print(f"\"{day[0]}\" - {day[1]} errors")
