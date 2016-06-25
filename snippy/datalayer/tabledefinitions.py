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