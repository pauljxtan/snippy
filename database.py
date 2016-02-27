"""
Database operations.
"""
import os
import sqlite3

DB_NAME = "snippy.db"
TABLE_NAME = "snippets"

EXAMPLE_TYPE = "Function"
EXAMPLE_LANG = "Python"
EXAMPLE_TITLE = "Prints hello world"
EXAMPLE_CODE = "def hello_world():\n    print \"Hello, world!\""


def init_db(verbose=False):
    if os.path.isfile(DB_NAME):
        return

    connection = get_connection()

    cursor = connection.cursor()
    create_command = ("CREATE TABLE %s (creation_date DATETIME, type TEXT, "
                      "language TEXT, title TEXT, code TEXT)" % TABLE_NAME)
    if verbose:
        print create_command
    cursor.execute(create_command)

    insert(connection, EXAMPLE_TYPE, EXAMPLE_LANG, EXAMPLE_TITLE, EXAMPLE_CODE,
           verbose)

    connection.commit()
    connection.close()


def get_connection():
    return sqlite3.connect(DB_NAME)


def get_all_rows(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM %s" % TABLE_NAME)
    return cursor.fetchall()


def insert_row(connection, snippet_type, snippet_lang, snippet_title,
               snippet_code, verbose=False):
    cursor = connection.cursor()
    command = ("INSERT INTO %s VALUES (DATETIME(), '%s', '%s', '%s', '%s')"
               % (TABLE_NAME, snippet_type, snippet_lang, snippet_title,
                  snippet_code))
    if verbose:
        print command
    cursor.execute(command)
