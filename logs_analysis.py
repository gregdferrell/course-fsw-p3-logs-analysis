# /usr/bin/python3.6.2
#
#

import re

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
    return [(row[0], row[1], row[2]) for row in rows]


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
        # Calculate percent error and round to two decimal places
        percent_error = round(100 * (day[2] - day[1]) / day[2], 2)
        if percent_error >= 1:
            print(re.sub(' +', ' ', f"{day[0]} - {percent_error}% errors"))
