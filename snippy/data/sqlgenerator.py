"""
SQL generators.
"""
import logging
from snippy.data.dbtypes import Schema, Table
from snippy.data.sqlite import python_to_sqlite_type
from snippy.utils.loggingtools import get_logger


class SqlGenerator:
    """A SQL generator for standard database operations."""
    def __init__(self, table: Table):
        """Initializes a SQL generator for a given table.

        :param table: Database table
        :type table: snippy.data.dbtypes.Table
        """
        self._table = table
        self._logger = get_logger('sqlgenerator', logging.DEBUG)

    def get_create_table_sql(self):
        """Returns the SQL for creating the table."""
        sql = ("CREATE TABLE IF NOT EXISTS {0} {1};"
               .format(self._table.name,
                       self._get_format_schema_sql(self._table.schema)))
        self._logger.debug("SQL: %s", sql)
        return sql

    def get_drop_table_sql(self):
        """Returns the SQL for dropping the table."""
        sql = "DROP TABLE IF EXISTS {0};".format(self._table.name)
        self._logger.debug("SQL: %s", sql)
        return sql

    def get_insert_row_sql(self):
        """Returns the SQL for inserting a row into the table."""
        cols = self._table.schema.get_column_names()
        cols_str = ", ".join(cols)
        cols_param_str = ", ".join([":{0}".format(col) for col in cols])
        sql = ("INSERT INTO {0} ({1}) values ({2});"
               .format(self._table.name, cols_str, cols_param_str))
        self._logger.debug("SQL: %s", sql)
        return sql

    def get_update_row_sql(self):
        """Returns the SQL for updating a row in the table."""
        cols = self._table.schema.get_column_names()
        sql = ("UPDATE {0} SET ".format(self._table.name))
        sql += ", ".join(["{0} = :{0}".format(col) for col in cols])
        sql += "WHERE rowid = :rowid"
        self._logger.debug("SQL: %s", sql)
        return sql

    def get_delete_row_sql(self):
        """Returns the SQL for deleting a row in the table."""
        sql = "DELETE FROM {0} WHERE rowid = :rowid".format(self._table.name)
        self._logger.debug("SQL: %s", sql)
        return sql

    def get_delete_all_rows_sql(self):
        """Returns the SQL for deleting all rows in the table."""
        sql = "DELETE FROM {0}".format(self._table.name)
        self._logger.debug("SQL: %s", sql)
        return sql

    def get_query_all_rows_sql(self):
        """Returns the SQL for querying all rows in the table."""
        sql = "SELECT *, ROWID FROM {0};".format(self._table.name)
        self._logger.debug("SQL: %s", sql)
        return sql

    def get_query_row_by_value_sql(self, column_name: str, value):
        """Returns the SQL for querying rows with a given column value.

        :param column_name: Column name
        :type column_name: str
        :param value: Search value
        :type value: [Column datatype]
        """
        if column_name not in self._table.schema.get_column_names():
            raise ValueError("Column name is not in table schema")
        sql = "SELECT *, ROWID FROM {0} WHERE {1} = ".format(self._table.name,
                                                             column_name)
        if isinstance(value, str):
            sql += "'{0}'".format(value)
        else:
            sql += "{0}".format(value)
        self._logger.debug("SQL: %s", sql)
        return sql

    def _get_format_schema_sql(self, schema: Schema):
        sql = "("
        for col in schema.columns[:-1]:
            sql += "{0} {1}, ".format(col.name,
                                      python_to_sqlite_type(col.dtype))
        sql += ("{0} {1})"
                .format(schema.columns[-1].name,
                        python_to_sqlite_type(schema.columns[-1].dtype)))
        self._logger.debug("SQL: %s", sql)
        return sql
