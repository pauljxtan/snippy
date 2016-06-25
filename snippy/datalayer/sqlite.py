import datetime
import logging
import sqlite3

# TODO: probably better to use built-in conversions

PYTHON_TO_SQLITE_TYPE = {
    datetime.datetime: 'DATETIME',
    str: 'TEXT',
}

SQLITE_TO_PYTHON_TYPE = {value: key for key, value
                         in PYTHON_TO_SQLITE_TYPE.items()}

def python_to_sqlite_type(dtype):
    """Converts a Python datatype to a SQLite datatype."""
    return PYTHON_TO_SQLITE_TYPE[dtype]

def sqlite_to_python_type(sqlite_dtype):
    """Converts a SQLite datatype to a Python datatype."""
    return SQLITE_TO_PYTHON_TYPE[sqlite_dtype]

class Sqlite:
    @classmethod
    def get_db_connection(cls, db_name):
        """Returns a database connection."""
        conn = sqlite3.connect(db_name)
        logging.info("Obtained connection to DB {0}".format(db_name))
        return conn

    @classmethod
    def execute_sql(cls, db_conn, sql, args=None):
        """Executes the given SQL."""
        cursor = db_conn.cursor()
        if args:
            print sql, args
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)

        query_results = None
        try:
            query_results = cursor.fetchall()
        except: # TODO: use correct exception
            # Not a query
            pass

        logging.debug("Execute: {0}, {1}".format(sql, args))
        db_conn.commit()
        cursor.close()

        return query_results