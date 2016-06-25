"""
SQL generators.
"""
import logging
from snippy.utils.loggingtools import get_logger
from snippy.datalayer.sqlite import python_to_sqlite_type

class SqlGenerator:
    def __init__(self, table):
        self._table = table
        self._logger = get_logger('sqlgenerator', logging.DEBUG)

    def get_create_table_sql(self):
        sql = ("CREATE TABLE IF NOT EXISTS {0} {1};"
               .format(self._table.name,
                       self._get_format_schema_sql(self._table.schema)))
        self._logger.debug("SQL: {0}".format(sql))
        return sql

    def _get_format_schema_sql(self, schema):
        sql = "("
        for col in schema.columns[:-1]:
            sql += "{0} {1}, ".format(col.name,
                                      python_to_sqlite_type(col.dtype))
        sql += ("{0} {1})"
                .format(schema.columns[-1].name,
                        python_to_sqlite_type(schema.columns[-1].dtype)))
        self._logger.debug("SQL: {0}".format(sql))
        return sql

    def get_drop_table_sql(self):
        sql = "DROP TABLE {0};".format(self._table.name)
        self._logger.debug("SQL: {0}".format(sql))
        return sql

    def get_insert_row_sql(self):
        cols = self._table.schema.get_column_names()
        cols_str = ", ".join(cols)
        cols_param_str = ", ".join([":{0}".format(col) for col in cols])
        sql = ("INSERT INTO {0} ({1}) values ({2});"
               .format(self._table.name, cols_str, cols_param_str))
        self._logger.debug("SQL: {0}".format(sql))
        return sql

    def get_update_row_sql(self):
        cols = self._table.schema.get_column_names()
        sql = ("UPDATE {0} SET ".format(self._table.name))
        sql += ", ".join([":{0} = ?".format(col) for col in cols])
        sql += "WHERE :rowid = ?"
        self._logger.debug("SQL: {0}".format(sql))
        return sql

    def get_delete_row_sql(self):
        sql = "DELETE FROM {0} WHERE :rowid = ?".format(self._table.name)
        self._logger.debug("SQL: {0}".format(sql))
        return sql

    def get_query_all_rows_sql(self):
        sql = "SELECT * FROM {0};".format(self._table.name)
        self._logger.debug("SQL: {0}".format(sql))
        return sql

    def get_query_row_by_value_sql(self, column_name, value):
        if column_name not in self._table.schema.get_column_names():
            raise ValueError("Column name is not in table schema")
        sql = "SELECT * FROM {0} WHERE {1} = ".format(self._table.name,
                                                      column_name)
        if isinstance(value, str):
            sql += "'{0}'".format(value)
        else:
            sql += "{0}".format(value)
        self._logger.debug("SQL: {0}".format(sql))
        return sql

    #def get_insert_row_sql(self, row):
        #if row.schema != self._table.schema:
        #    raise ValueError("Row schema does not match table schema")
        #columns_str = ", ".join(row.get_column_names())
        #values_str = ", ".join(map(str, row.values))