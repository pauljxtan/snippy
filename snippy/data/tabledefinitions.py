"""
Database table definitions.
"""
import datetime
from snippy.data.dbtypes import Column, Schema, Table


class TableDefinition:
    """Encapsulates various properties of a database table."""
    def __init__(self, name: str, columns: list, databox_indices=None):
        """Initializes the table definition.

        :param name: Table name
        :type name: str
        :param columns: Table columns
        :type columns: list(Column)
        :param databox_indices: Indices of columns to display in databox
        :type databox_indices = list(int)
        """
        if databox_indices is None:
            self.databox_indices = tuple(range(len(columns)))
        else:
            self.databox_indices = databox_indices

        self.name = name
        self.cols = columns

    @property
    def table(self):
        """The table."""
        return Table(self.name, self.schema)

    @property
    def schema(self):
        """The table schema."""
        return Schema(self.cols)

    @property
    def cols_databox(self):
        """The columns to be included in the databox."""
        return [self.cols[i] for i in self.databox_indices]

    @property
    def col_names(self):
        """The column names."""
        return [col.name for col in self.cols]

    @property
    def col_names_databox(self):
        """The names of the columns to be included in the databox."""
        return [self.col_names[i] for i in self.databox_indices]

    @property
    def col_names_display(self):
        """The column names in more human-readable format."""
        return [name.replace("_", " ").title() for name in self.col_names]

    @property
    def col_names_display_databox(self):
        """The columns names to be included in the databox,
        in more human-readable format.
        """
        return [name.replace("_", " ").title()
                for name in self.col_names_display]

_TABLE_STANDARD_COLS = (
    Column('creation_date', datetime.datetime),
    Column('snippet_type', str),
    Column('language', str),
    Column('title', str),
    Column('code', str)
)

#: The standard table definition
TABLE_STANDARD = TableDefinition('snippy', _TABLE_STANDARD_COLS, (0, 1, 2, 3))
