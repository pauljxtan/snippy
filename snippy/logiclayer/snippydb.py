import datetime
from snippy.datalayer.snippytypes import Snippet
from snippy.datalayer.sqlite import Sqlite
from snippy.datalayer.tabledefinitions import TABLE_STANDARD
from snippy.logiclayer.tablecontroller import TableController

EXAMPLE_SNIPPET = {
    'creation_date': datetime.datetime.now(),
    'snippet_type':  "Function",
    'language':  "Python",
    'title': "Prints hello world",
    'code':  "def hello_world():\n    print \"Hello, world!\""
}

class SnippyDB:
    def __init__(self, db_name, verbose=False):
        self._db_name = db_name
        self._db_conn = Sqlite.get_db_connection(db_name)
        self._table = TABLE_STANDARD
        self._table_ctlr = TableController(self._db_conn, self._table)
        self.verbose = verbose

        self._table_ctlr.create_table()
        if verbose:
            print "Created table {0}".format(self._table.name) 

        self._table_ctlr.insert_row(EXAMPLE_SNIPPET)

    def __del__(self):
        self._db_conn.close()

    def query_all_rows(self):
        return self._table_ctlr.query_all_rows()

    def query_by_creation_date(self, creation_date):
        return self._table_ctlr.query_row_by_value('creation_date',
                                                   creation_date)

    def query_by_snippet_type(self, snippet_type):
        return self._table_ctlr.query_row_by_value('snippet_type',
                                                   snippet_type)

    def query_by_language(self, language):
        return self._table_ctlr.query_row_by_value('language', language)

    def query_by_title(self, title):
        return self._table_ctlr.query_row_by_value('title', title)

    def insert_snippet(self, snippet):
        print self._get_row_from_snippet(snippet)
        self._table_ctlr.insert_row(self._get_row_from_snippet(snippet))

    def _get_row_from_snippet(self, snippet):
        return {'creation_date': snippet.cdate,
                'snippet_type': snippet.stype,
                'language': snippet.lang,
                'title': snippet.title,
                'code': snippet.code}
