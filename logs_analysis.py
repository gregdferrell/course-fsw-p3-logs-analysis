# /usr/bin/python3.6.2
#
#

import re
import sys

import psycopg2

DB_SERVER = ''  # TODO Fill this in
DB_PORT = ''  # TODO Fill this in
DB_NAME = 'news'  # TODO Fill this in
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
    SELECT to_char(time, 'Month DD, YYYY') AS dt,
        count(*) FILTER (WHERE status LIKE '2%') AS count_success,
        count(*) AS count_total
    FROM log
    GROUP BY dt
    ORDER BY dt
"""


def connect():
    """
    Connect to the PostgreSQL database.
    :return: Returns a tuple of database connection and cursor.
    """
    try:
        db = psycopg2.connect(
            f"dbname='{DB_NAME}' user='{DB_USER}' host='{DB_SERVER}' " +
            F"port='{DB_PORT}' password='{DB_PASSWORD}'")
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("Error connecting to the database: " + str(e))
        sys.exit(1)


def execute_query(query):
    """
    Creates a DB connection, executes the given query, closes the connection
    and returns the results of the query.
    """
    conn, cursor = connect()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows


def print_most_popular_articles():
    """
    Print most popular articles
    """
    print("Most popular articles:")
    rows = execute_query(SQL_GET_MOST_POPULAR_ARTICLES)
    for article in rows:
        print(f"\"{article[0]}\" - {article[1]} views")


def print_most_popular_authors():
    """
    Prints most popular authors
    """
    print("\nMost popular authors:")
    rows = execute_query(SQL_GET_MOST_POPULAR_AUTHORS)
    for author in rows:
        print(f"\"{author[0]}\" - {author[1]} views")


def print_days_with_high_errors():
    """
    Prints days with HTTP error response rate >= 1%
    """
    print('\nDays with error response rate >= 1%:')
    rows = execute_query(SQL_GET_DAYS_WITH_HIGH_ERRORS)
    for day in rows:
        # Calculate percent error and round to two decimal places
        percent_error = round(100 * (day[2] - day[1]) / day[2], 2)
        if percent_error >= 1:
            print(re.sub(' +', ' ', f"{day[0]} - {percent_error}% errors"))


if __name__ == "__main__":
    print_most_popular_articles()
    print_most_popular_authors()
    print_days_with_high_errors()
