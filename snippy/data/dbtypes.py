"""Database types."""

from typing import Iterable

class Column: # pylint: disable=too-few-public-methods
    """Represents a column in the schema of a database table.

    :param name: Column name
    :type name: str
    :param dtype: Column datatype
    :type dtype: type
    """
    def __init__(self, name: str, dtype: type):
        self.name = name
        self.dtype = dtype

    def __eq__(self, other):
        return self.name == other.name and self.dtype == other.dtype

class Schema:
    """Represents the schema of a database table.

    :param columns: Columns in schema
    :type columns: iterable(snippy.data.dbtypes.Column)
    """
    def __init__(self, columns: Iterable[Column]):
        self.columns = columns

    def __eq__(self, other):
        return (self.get_column_names() == other.get_column_names() and
                self.get_column_dtypes() == other.get_column_dtypes())

    def get_column_names(self):
        """Returns the column names."""
        return [column.name for column in self.columns]

    def get_column_dtypes(self):
        """Returns the column datatypes."""
        return [column.dtype for column in self.columns]

class Table: # pylint: disable=too-few-public-methods
    """Represents a database table.

    :param name: Table name
    :type name: str
    :param schema: Table schema
    :type schema: snippy.data.dbtypes.Schema
    """
    def __init__(self, name: str, schema: Schema):
        self.name = name
        self.schema = schema

    def __eq__(self, other):
        return self.name == other.name and self.schema == other.schema
