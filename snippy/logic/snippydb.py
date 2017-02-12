"""
The Snippy database.
"""
from datetime import datetime
from snippy.data.snippytypes import Snippet
from snippy.data.sqlite import Sqlite
from snippy.data.tabledefinitions import TABLE_STANDARD
from snippy.logic.tablecontroller import TableController
from snippy.utils.utils import get_row_from_snippet, get_snippets_from_rows


class SnippyDb:
    """Encapsulates a snippy database.

    :param db_name: Database name
    :type db_name: str
    :param verbose: Verbose flag
    :type verbose: bool
    """
    def __init__(self, db_name: str, clobber: bool=False, verbose: bool=False):
        self._db_name = db_name
        self._db_conn = Sqlite.get_db_connection(db_name)
        self._table = TABLE_STANDARD.table
        self._table_ctlr = TableController(self._db_conn, self._table)
        self.verbose = verbose

        self._table_ctlr.create_table(clobber)
        if verbose:
            print("Created table {0}".format(self._table.name))

    def __del__(self):
        self._db_conn.close()

    def get_all_snippets(self):
        """Returns all snippets in the database."""
        rows = self._table_ctlr.query_all_rows()
        return get_snippets_from_rows(rows), [row['rowid'] for row in rows]

    def get_snippets_by_creation_date(self, creation_date: datetime):
        """Returns all snippets with the given creation date.

        :param creation_date: Snippet creation date
        :type creation_date: datetime
        """
        rows = self._table_ctlr.query_row_by_value('creation_date',
                                                   creation_date)
        return get_snippets_from_rows(rows)

    def get_snippets_by_snippet_type(self, snippet_type: str):
        """Returns all snippets of the given type.

        :param snippet_type: Snippet type
        :type snippet_type: str
        """
        rows = self._table_ctlr.query_row_by_value('snippet_type',
                                                   snippet_type)
        return get_snippets_from_rows(rows)

    def get_snippets_by_language(self, language: str):
        """Returns all snippets in the given programming language.

        :param language: Snippet programming language
        :type language: str
        """
        rows = self._table_ctlr.query_row_by_value('language', language)
        return get_snippets_from_rows(rows)

    def get_snippets_by_title(self, title: str):
        """Returns all snippets with the given title.

        :param title: Snippet title
        :type title: str
        """
        rows = self._table_ctlr.query_row_by_value('title', title)
        return get_snippets_from_rows(rows)

    def get_snippets_by_rowid(self, rowid: int):
        """Returns all snippets with the given row ID.

        :param rowid: Table row ID
        :type rowid: int
        """
        rows = self._table_ctlr.query_row_by_value('rowid', rowid)
        return get_snippets_from_rows(rows)

    def insert_snippet(self, snippet: Snippet):
        """Inserts a snippet into the database.

        :param snippet: Snippet
        :type snippet: snippy.data.snippytypes.Snippet
        """
        self._table_ctlr.insert_row(get_row_from_snippet(snippet))

    def update_snippet(self, rowid: int, snippet: Snippet):
        """Updates a snippet in the database.

        :param rowid: Table row ID
        :type rowid: int
        :param snippet: Snippet
        :type snippet: snippy.data.snippytypes.Snippet
        """
        self._table_ctlr.update_row(rowid, get_row_from_snippet(snippet))

    def delete_snippet(self, rowid: int):
        """Deletes a snippet from the database.

        :param rowid: Table row ID
        :type rowid: int
        """
        self._table_ctlr.delete_row(rowid)

    def delete_all_snippets(self):
        """Deletes all snippets from the database."""
        self._table_ctlr.delete_all_rows()
