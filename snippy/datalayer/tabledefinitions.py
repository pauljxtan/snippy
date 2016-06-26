import datetime
from snippy.datalayer.dbtypes import Column, Schema, Table

_COLUMNS_STANDARD = (
    Column('creation_date', datetime.datetime),
    Column('snippet_type', str),
    Column('language', str),
    Column('title', str),
    Column('code', str)
)
_SCHEMA_STANDARD = Schema(_COLUMNS_STANDARD)
TABLE_STANDARD = Table('snippy', _SCHEMA_STANDARD)

class TableDefinition:
    def __init__(self, name, columns, databox_indices=None):
        if databox_indices is None:
            self.databox_indices = tuple(range(len(columns)))
        else:
            self.databox_indices = databox_indices

        self.name = name
        self.cols = columns

    @property
    def schema(self):
        return Schema(self.cols)

    @property
    def table(self):
        return Table(self.name, self.schema)

    @property
    def cols_databox(self):
        return [self.cols[i] for i in self.databox_indices]

    @property
    def col_names(self):
        return [col.name for col in self.cols]

    @property
    def col_names_databox(self):
        return [self.col_names[i] for i in self.databox_indices]

    @property
    def col_names_display(self):
        return [name.replace("_", " ").title() for name in self.col_names]

    @property
    def col_names_display_databox(self):
       return [name.replace("_", " ").title()
               for name in self.col_names_display]

_TABLE_STANDARD_COLS = (
    Column('creation_date', datetime.datetime),
    Column('snippet_type', str),
    Column('language', str),
    Column('title', str),
    Column('code', str)
)
TABLE_STANDARD = TableDefinition('snippy', _TABLE_STANDARD_COLS, (0, 1, 2, 3))