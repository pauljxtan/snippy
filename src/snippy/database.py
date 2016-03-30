"""
Database operations.
"""
import os
import sqlite3

EXAMPLE_SNIPPET = {
    'type':  "Function",
    'lang':  "Python",
    'title': "Prints hello world",
    'code':  "def hello_world():\n    print \"Hello, world!\""
}

TABLE_SCHEMA = """(
    creation_date DATETIME,
    type TEXT,
    language TEXT,
    title TEXT,
    code TEXT
)
"""


class SnippyDB:
    def __init__(self, db_filename, table_name, clobber=False, verbose=False):
        if os.path.isfile(db_filename):
            if not clobber:
                raise ValueError("Database file %s already exists"
                                 % db_filename)
            if verbose:
                print "Overwriting %s" % db_filename
                os.remove(db_filename)

        self._db_filename = db_filename
        self._table_name = table_name
        self.verbose = verbose
        self._conn = sqlite3.connect(db_filename)

        # Initialize the table with some example data
        command = "CREATE TABLE %s %s" % (self._table_name, TABLE_SCHEMA)
        if verbose:
            print command
        self._conn.execute(command)
        self.insert_row(EXAMPLE_SNIPPET['type'], EXAMPLE_SNIPPET['lang'],
                        EXAMPLE_SNIPPET['title'], EXAMPLE_SNIPPET['code'])

    def get_all_rows(self):
        command = "SELECT * FROM %s" % self._table_name
        if self.verbose:
            print command
        rows = self._conn.execute(command)

        return rows.fetchall()

    def get_row(self, row_id):
        command = ("SELECT * FROM %s WHERE ROWID=%s"
                   % (self._table_name, row_id))
        if self.verbose:
            print command
        row = self._conn.execute(command)

        return row.fetchone()

    def get_unique_elem(self, row_id, column):
        command = ("SELECT %s FROM %s WHERE ROWID=%s"
                   % (column, self._table_name, row_id))
        if self.verbose:
            print command
        elem = self._conn.execute(command)

        return elem.fetchone()[0]

    def insert_row(self, snippet_type, snippet_lang, snippet_title,
                   snippet_code):
        command = ("INSERT INTO %s VALUES (DATETIME(), '%s', '%s', '%s', '%s')"
                   % (self._table_name, snippet_type, snippet_lang,
                      snippet_title, snippet_code))
        if self.verbose:
            print command
        self._conn.execute(command)
