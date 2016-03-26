"""
Database operations.
"""
import os
import sqlite3

EXAMPLE_TYPE = "Function"
EXAMPLE_LANG = "Python"
EXAMPLE_TITLE = "Prints hello world"
EXAMPLE_CODE = "def hello_world():\n    print \"Hello, world!\""


def init_db(db_filename, table_name, verbose=False):
    if os.path.isfile(db_filename):
        return

    connection = get_connection(db_filename)

    cursor = connection.cursor()
    create_command = ("CREATE TABLE %s (creation_date DATETIME, type TEXT, "
                      "language TEXT, title TEXT, code TEXT)" % table_name)
    if verbose:
        print create_command
    cursor.execute(create_command)

    insert_row(connection, table_name, EXAMPLE_TYPE, EXAMPLE_LANG,
               EXAMPLE_TITLE, EXAMPLE_CODE, verbose)

    connection.commit()
    connection.close()


def get_connection(db_filename):
    return sqlite3.connect(db_filename)


def get_all_rows(connection, table_name):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM %s" % table_name)
    return cursor.fetchall()


def insert_row(connection, table_name, snippet_type, snippet_lang,
               snippet_title, snippet_code, verbose=False):
    cursor = connection.cursor()
    command = ("INSERT INTO %s VALUES (DATETIME(), '%s', '%s', '%s', '%s')"
               % (table_name, snippet_type, snippet_lang, snippet_title,
                  snippet_code))
    if verbose:
        print command
    cursor.execute(command)


def get_row(connection, table_name, snippet_type, snippet_lang, snippet_title,
            snippet_code, verbose=False):
    return
