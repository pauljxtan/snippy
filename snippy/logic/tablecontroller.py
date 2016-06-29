import logging
from snippy.data.sqlgenerator import SqlGenerator
from snippy.data.sqlite import Sqlite
from snippy.utils.loggingtools import get_logger

class TableController:
    def __init__(self, db_conn, table):
        """
        :param db_conn: Database connection
        :type db_conn: sqlite3.Connection
        :param table: Database table
        :type table: snippy.data.dbtypes.Table
        """
        self._db_conn = db_conn
        self._table = table
        self._sql_gen = SqlGenerator(table)
        self._logger = get_logger('tablecontroller', logging.DEBUG)

    def create_table(self, clobber=False):
        """
        :param clobber: Flag indicating to overwrite existing table
        :type clobber: bool
        """
        if clobber:
            sql = self._sql_gen.get_drop_table_sql()
            Sqlite.execute_sql(self._db_conn, sql)
            self._logger.info("Dropped table {0}".format(self._table.name))
        sql = self._sql_gen.get_create_table_sql()
        Sqlite.execute_sql(self._db_conn, sql)
        self._logger.info("Created table {0}".format(self._table.name))

    def insert_row(self, row):
        """
        :param row: Table row
        :type row: dict(column name, value)
        """
        sql = self._sql_gen.get_insert_row_sql()
        Sqlite.execute_sql(self._db_conn, sql, row)
        self._logger.info("Inserted row [...]")

    def update_row(self, rowid, row):
        """
        :param rowid: Table row ID
        :type rowid: int
        :param row: Table row
        :type row: dict(column name, value)
        """
        row['rowid'] = rowid
        sql = self._sql_gen.get_update_row_sql(row)
        Sqlite.execute_sql(self._db_conn, sql, row)
        self._logger.info("Updated row [...]")

    def delete_row(self, rowid):
        """
        :param rowid: Table row ID
        :type rowid: int
        """
        sql = self._sql_gen.get_delete_row_sql({'rowid': rowid})
        Sqlite.execute_sql(self._db_conn, sql, rowid)
        self._logger.info("Deleted row [...]")

    def query_all_rows(self):
        sql = self._sql_gen.get_query_all_rows_sql()
        queryResults = Sqlite.execute_sql(self._db_conn, sql)
        self._logger.info("Queried all rows")
        return queryResults

    def query_row_by_value(self, column_name, value):
        """
        :param column_name: Column name
        :type column_name: str
        :param value: Search value
        :type value: [Column datatype]
        """
        sql = self._sql_gen.get_query_row_by_value_sql(column_name, value)
        queryResults = Sqlite.execute_sql(self._db_conn, sql)
        self._logger.info("Queried rows with {0} = {1}".format(column_name, value))
        return queryResults

    #def table_exists(self, table_name):
    #    sql = ("SELECT name FROM sqlite_master "
    #           "WHERE type = 'table' AND name = 'table_name';")
    #    table_names = Sqlite.execute_sql(self._db_conn, sql)
    #    print table_names
    #    return table_name in table_names
