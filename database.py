"""
Database operations.
"""
import sqlite3

DB_NAME = "snippy.db"
TABLE_NAME = "snippets"

def initialize_database(verbose=False):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()
    create_command = ("CREATE TABLE %s (type text, lang text, code text)"
                      % TABLE_NAME)
    if verbose: print create_command
    cursor.execute(create_command)

    example_type = "function"
    example_lang = "python"
    example_code = "def hello_world():\n    print \"Hello, world!\""

    insert_snippet(cursor, example_type, example_lang, example_code, verbose)

    connection.commit()
    connection.close()

def insert_snippet(cursor, snippet_type, snippet_lang, snippet_code,
                   verbose=False):
    command = ("INSERT INTO %s VALUES ('%s', '%s', '%s')"
               % (TABLE_NAME, snippet_type, snippet_lang, snippet_code))
    if verbose: print command
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
    initialize_database(True)
    print_table_rows()
