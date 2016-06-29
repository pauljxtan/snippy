import datetime
import logging
from snippy.data.dbtypes import Column, Table, Schema
from snippy.data.sqlgenerator import SqlGenerator
from snippy.data.sqlite import Sqlite
#from snippy.utils.logging import Logger, SeverityLevels
from snippy.utils.logformats import LOG_FORMAT_STANDARD
from snippy.data.snippytypes import Snippet
from snippy.logic.tablecontroller import TableController
from snippy.data.tabledefinitions import TABLE_STANDARD
from snippy.logic.snippydb import SnippyDB

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
print(db.get_all_snippets())
db.insert_snippet(snippet2)
db.insert_snippet(snippet2)
print(db.get_all_snippets())
print(db.get_snippets_by_title("Simple hello world"))
