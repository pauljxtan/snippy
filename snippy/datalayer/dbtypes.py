"""
Database types.
"""

class Table:
    def __init__(self, name, schema):
        self.name = name
        self.schema = schema

    def __eq__(self, other):
        return self.name == other.name and self.schema == other.schema

class Schema:
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
    def __init__(self, name, dtype):
        self.name = name
        self.dtype = dtype

    def __eq__(self, other):
        return self.name == other.name and self.dtype == other.dtype

#class Row:
#    def __init__(self, schema, values):
#        self.schema = schema
#        self.values = values

#    def get_column_names(self):
#        return self.schema.get_column_names()
