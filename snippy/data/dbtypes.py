"""
Database types.
"""

class Table:
    """Represents a database table.

    :param name: Table name
    :type name: str
    :param schema: Table schema
    :type schema: snippy.data.dbtypes.Schema
    """
    def __init__(self, name, schema):
        self.name = name
        self.schema = schema

    def __eq__(self, other):
        return self.name == other.name and self.schema == other.schema

class Schema:
    """Represents the schema of a database table.

    :param columns: Columns in schema
    :type columns: list(snippy.data.dbtypes.Column)
    """
    def __init__(self, columns):
        self.columns = columns

    def __eq__(self, other):
        return (self.get_column_names() == other.get_column_names() and
                self.get_column_dtypes() == other.get_column_dtypes())

    def get_column_names(self):
        return [column.name for column in self.columns]

    def get_column_dtypes(self):
        return [column.dtype for column in self.columns]

class Column:
    """Represents a column in the schema of a database table.

    :param name: Column name
    :type name: str
    :param dtype: Column datatype
    :type dtype: type
    """
    def __init__(self, name, dtype):
        self.name = name
        self.dtype = dtype

    def __eq__(self, other):
        return self.name == other.name and self.dtype == other.dtype
