"""
Sqlite data access.
"""
import datetime
import logging
import sqlite3
from snippy.utils.loggingtools import get_logger


# TODO: probably better to use built-in conversions

PYTHON_TO_SQLITE_TYPE = {
    datetime.datetime: 'DATETIME',
    str: 'TEXT',
}

SQLITE_TO_PYTHON_TYPE = {value: key for key, value
                         in PYTHON_TO_SQLITE_TYPE.items()}


def python_to_sqlite_type(dtype: type):
    """
    Converts a Python datatype to a SQLite datatype.

    :param dtype: Python datatype
    :type dtype: type
    """
    return PYTHON_TO_SQLITE_TYPE[dtype]


def sqlite_to_python_type(sqlite_dtype: str):
    """
    Converts a SQLite datatype to a Python datatype.

    :param sqlite_dtype: SQLite datatype
    :type sqlite_dtype: str
    """
    return SQLITE_TO_PYTHON_TYPE[sqlite_dtype]


class Sqlite:
    """Sqlite database access."""
    @classmethod
    def get_db_connection(cls, db_name: str):
        """
        Returns a database connection.

        :param db_name: Database name
        :type db_name: str
        """
        logger = get_logger('sqlite', logging.DEBUG)
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        logger.info("Obtained connection to DB %s", db_name)
        return conn

    @classmethod
    def execute_sql(cls, db_conn: sqlite3.Connection, sql: str, args=None):
        """
        Executes the given SQL.

        :param db_conn: Database connection
        :type db_conn: sqlite3.Connection
        :param sql: SQL statement(s)
        :type sql: str
        :param args: Named parameters for SQL statement(s)
        :type args: dict
        """
        logger = get_logger('sqlite', logging.DEBUG)
        cursor = db_conn.cursor()
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)

        query_results = None
        try:
            query_results = cursor.fetchall()
        except sqlite3.Error:
            # Not a query
            pass

        logger.debug("Execute: %s, %s", sql, args)
        db_conn.commit()
        cursor.close()

        return query_results
