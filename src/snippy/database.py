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

    create_command = ("""
CREATE TABLE %s (
    creation_date DATETIME,
    type TEXT,
    language TEXT,
    title TEXT,
    code TEXT)
""" % table_name)
    if verbose:
        print create_command
    connection.execute(create_command)

    insert_row(connection, table_name, EXAMPLE_TYPE, EXAMPLE_LANG,
               EXAMPLE_TITLE, EXAMPLE_CODE, verbose)

    connection.commit()
    connection.close()


def get_connection(db_filename):
    connection = sqlite3.connect(db_filename)
    #connection.row_factory = sqlite3.Row

    return connection


def get_all_rows(connection, table_name):
    rows = connection.execute("SELECT * FROM %s" % table_name)

    return rows.fetchall()


def insert_row(connection, table_name, snippet_type, snippet_lang,
               snippet_title, snippet_code, verbose=False):
    command = ("INSERT INTO %s VALUES (DATETIME(), '%s', '%s', '%s', '%s')"
               % (table_name, snippet_type, snippet_lang, snippet_title,
                  snippet_code))
    if verbose:
        print command
    connection.execute(command)


def get_row(connection, table_name, row_id, verbose=False):
    command = ("SELECT * FROM %s WHERE ROWID=%s" % (table_name, row_id))

    if verbose:
        print command
    row = connection.execute(command)

    return row.fetchone()


def get_unique_elem(connection, table_name, row_id, column, verbose=False):
    #connection.row_factory = sqlite3.Row
    #row = get_row(connection, table_name, row_id, verbose)
    #connection.row_factory = None
    #return row[column]
    command = ("SELECT %s FROM %s WHERE ROWID=%s"
               % (column, table_name, row_id))

    if verbose:
        print command
    elem = connection.execute(command)

    return elem.fetchone()[0]
