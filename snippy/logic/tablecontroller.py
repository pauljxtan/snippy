"""
The database table controller.
"""
import logging
from sqlite3 import Connection
from typing import Any, Mapping
from snippy.data.dbtypes import Table
from snippy.data.sqlgenerator import SqlGenerator
from snippy.data.sqlite import Sqlite
from snippy.utils.loggingtools import get_logger


class TableController:
    """Controls data access and manipulation for a given table.

    :param db_conn: Database connection
    :type db_conn: sqlite3.Connection
    :param table: Database table
    :type table: snippy.data.dbtypes.Table
    """
    def __init__(self, db_conn: Connection, table: Table):
        self._db_conn = db_conn
        self._table = table
        self._sql_gen = SqlGenerator(table)
        self._logger = get_logger('tablecontroller', logging.DEBUG)

    def create_table(self, clobber: bool=False):
        """Creates a table.

        :param clobber: Flag indicating to overwrite existing table
        :type clobber: bool
        """
        if clobber:
            sql = self._sql_gen.get_drop_table_sql()
            Sqlite.execute_sql(self._db_conn, sql)
            self._logger.info("Dropped table %s", self._table.name)
        sql = self._sql_gen.get_create_table_sql()
        Sqlite.execute_sql(self._db_conn, sql)
        self._logger.info("Created table %s", self._table.name)

    def insert_row(self, row: Mapping[str, Any]):
        """Inserts a row.

        :param row: Table row
        :type row: dict(str, [column datatype])
        """
        sql = self._sql_gen.get_insert_row_sql()
        Sqlite.execute_sql(self._db_conn, sql, row)
        # TODO: get row id from insert
        self._logger.info("Inserted row [...]")

    def update_row(self, rowid: int, row: Mapping[str, Any]):
        """Updates a row.

        :param rowid: Table row ID
        :type rowid: int
        :param row: Table row
        :type row: dict(str, [column datatype])
        """
        row['rowid'] = rowid
        sql = self._sql_gen.get_update_row_sql()
        Sqlite.execute_sql(self._db_conn, sql, row)
        self._logger.info("Updated row %s", rowid)

    def delete_row(self, rowid: int):
        """Deletes a row.

        :param rowid: Table row ID
        :type rowid: int
        """
        sql = self._sql_gen.get_delete_row_sql()
        Sqlite.execute_sql(self._db_conn, sql, {'rowid': rowid})
        self._logger.info("Deleted row %s", rowid)

    def delete_all_rows(self):
        """Deletes all rows."""
        sql = self._sql_gen.get_delete_all_rows_sql()
        Sqlite.execute_sql(self._db_conn, sql)
        self._logger.info("Deleted all rows")

    def query_all_rows(self):
        """Returns all rows."""
        sql = self._sql_gen.get_query_all_rows_sql()
        query_results = Sqlite.execute_sql(self._db_conn, sql)
        self._logger.info("Queried all rows")
        return query_results

    def query_row_by_value(self, column_name: str, value: Any):
        """Returns all rows with a given column value.

        :param column_name: Column name
        :type column_name: str
        :param value: Search value
        :type value: [Column datatype]
        """
        sql = self._sql_gen.get_query_row_by_value_sql(column_name, value)
        query_results = Sqlite.execute_sql(self._db_conn, sql)
        self._logger.info("Queried rows with %s = %s", column_name, value)
        return query_results

    # def table_exists(self, table_name):
    #     sql = ("SELECT name FROM sqlite_master "
    #            "WHERE type = 'table' AND name = 'table_name';")
    #     table_names = Sqlite.execute_sql(self._db_conn, sql)
    #     print table_names
    #     return table_name in table_names
