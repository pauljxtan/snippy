import logging
from snippy.datalayer.sqlgenerator import SqlGenerator
from snippy.datalayer.sqlite import Sqlite
from snippy.utils.loggingtools import get_logger

class TableController:
    def __init__(self, db_conn, table):
        self._db_conn = db_conn
        self._table = table
        self._sql_gen = SqlGenerator(table)
        self._logger = get_logger('tablecontroller', logging.DEBUG)

    def create_table(self, clobber=False):
        if clobber:
            sql = self._sql_gen.get_drop_table_sql()
            Sqlite.execute_sql(self._db_conn, sql)
            self._logger.info("Dropped table {0}".format(self._table.name))
        sql = self._sql_gen.get_create_table_sql()
        Sqlite.execute_sql(self._db_conn, sql)
        self._logger.info("Created table {0}".format(self._table.name))

    def insert_row(self, row):
        sql = self._sql_gen.get_insert_row_sql()
        Sqlite.execute_sql(self._db_conn, sql, row)
        self._logger.info("Inserted row [...]")

    def query_all_rows(self):
        sql = self._sql_gen.get_query_all_rows_sql()
        queryResults = Sqlite.execute_sql(self._db_conn, sql)
        self._logger.info("Queried all rows")
        return queryResults

    def query_row_by_value(self, column_name, value):
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
