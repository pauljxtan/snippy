"""
Database operations.
"""
import sqlite3

DB_NAME = "snippy.db"
TABLE_NAME = "snippets"

EXAMPLE_TYPE = "Function"
EXAMPLE_LANG = "Python"
EXAMPLE_TITLE = "Prints hello world"
EXAMPLE_CODE = "def hello_world():\n    print \"Hello, world!\""


def initialize_database(verbose=False):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()
    create_command = ("CREATE TABLE %s (creation_date DATETIME, type TEXT, "
                      "language TEXT, title TEXT, code TEXT)" % TABLE_NAME)
    if verbose:
        print create_command
    cursor.execute(create_command)

    insert_snippet(cursor, EXAMPLE_TYPE, EXAMPLE_LANG, EXAMPLE_TITLE,
                   EXAMPLE_CODE, verbose)

    connection.commit()
    connection.close()


def insert_snippet(cursor, snippet_type, snippet_lang, snippet_title,
                   snippet_code, verbose=False):
    command = ("INSERT INTO %s VALUES (DATETIME(), '%s', '%s', '%s', '%s')"
               % (TABLE_NAME, snippet_type, snippet_lang, snippet_title,
                  snippet_code))
    if verbose:
        print command
    cursor.execute(command)


def print_table_rows():
    """For debugging only"""
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM %s" % TABLE_NAME)
    rows = cursor.fetchall()
    for row in rows:
        print row

    connection.close()


if __name__ == '__main__':
    import os

    os.remove("snippy.db")
    initialize_database(True)
    print_table_rows()
