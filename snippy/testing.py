import datetime
import logging
from snippy.datalayer.dbtypes import Column, Table, Schema
from snippy.datalayer.sqlgenerator import SqlGenerator
from snippy.datalayer.sqlite import Sqlite
#from snippy.utils.logging import Logger, SeverityLevels
from snippy.utils.logformats import LOG_FORMAT_STANDARD
from snippy.datalayer.snippytypes import Snippet
from snippy.logiclayer.tablecontroller import TableController
from snippy.datalayer.tabledefinitions import TABLE_STANDARD
from snippy.logiclayer.snippydb import SnippyDB

#logging.basicConfig(
#    filename="test1.log",
#    filemode='a',
#    level=logging.DEBUG,
#    format=LOG_FORMAT_STANDARD
#    )

columns = (Column('creation_date', datetime.datetime), Column('title', str))
schema = Schema(columns)

sql_generator = SqlGenerator(Table("mytable", schema))

#db_conn = Sqlite.get_db_connection("snippy.db")
#table = Table("test1", schema)
#table_ctlr = TableController(db_conn, table)
#table_ctlr.create_table()

#print(sql_generator.get_create_table_sql()
#values = (datetime.datetime.now(), "hello world")
#print(sql_generator.get_insert_row_sql()
#print(sql_generator.get_query_all_rows_sql()
#print(sql_generator.get_query_row_by_value_sql('title', "hello world")


#row = {'creation_date': datetime.datetime.now(), 'title': "hello, world"}
#print(row
#table_ctlr.insert_row(row)
#print(table_ctlr.query_all_rows()
#print(table_ctlr.query_row_by_value('title', "hello, world")

snippet = Snippet(datetime.datetime.now(), "function", "Python", "Simple hello world",
                  "def hello_world():\n    print(\"Hello, world!\"")
snippet2 = Snippet(datetime.datetime.now(), "function", "Python", "Simple hello world2",
                  "def hello_world():\n    print(\"Hello, world!\"")
#row = {'creation_date': snippet.cdate, 'snippet_type': snippet.stype, 'language': snippet.lang,
#       'title': snippet.title, 'code': snippet.code}
#table = TABLE_STANDARD
#table_ctlr = TableController(db_conn, table)
#table_ctlr.create_table(True)
#table_ctlr.insert_row(row)
#table_ctlr.insert_row(row)
#print(table_ctlr.query_all_rows()
#print(table_ctlr.query_row_by_value('title', "Simple hello world")

db = SnippyDB("snippy.db")
db.insert_snippet(snippet)
print(db.query_all())
db.insert_snippet(snippet2)
db.insert_snippet(snippet2)
print(db.query_all())
print(db.query_by_title("Simple hello world"))
