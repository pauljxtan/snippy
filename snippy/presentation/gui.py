import datetime
import tkinter as tk
from tkinter import ttk

from snippy.data.snippytypes import Snippet
from snippy.logic.snippydb import SnippyDb
from snippy.presentation.forms import FormMaker
from snippy.presentation.menus import MenuMaker
from snippy.presentation.widgets import DataBox, MyNotebook

WELCOME_MESSAGE = ("Welcome to Snippy!\n"
                   "To get started, click on 'Create snippet' on the top menu,"
                   " or right-click on any snippet above.")
EXAMPLE_SNIPPET = Snippet(datetime.datetime(2001, 1, 1), "Function", "Python",
                          "Simple hello world",
                          "def hello_world():\n    print(Hello, world!)")

class SnippyGui(ttk.Frame):
    """The main snippy GUI.

    :param parent: Parent widget
    :type parent: Tkinter.Widget
    :param db: Database/table controller
    :type db: snippy.logic.tablecontroller.TableController
    """
    def __init__(self, parent: tk.Widget, db: SnippyDb, verbose=False):
        ttk.Frame.__init__(self)
        self.parent = parent
        self._db = db
        self._verbose = verbose

        self._databox = DataBox(self)
        self._databox.pack(fill=tk.BOTH, expand=True)
        self._update_databox()

        self._notebook = MyNotebook(self)
        self._notebook.pack(fill=tk.BOTH, expand=True)
        self._make_welcome_tab()

        self._menu_maker = MenuMaker(self)
        self.parent.config(menu=self._menu_maker.make_menubar())
        self._context_menu = self._menu_maker.make_context_menu()
        self._row_id_context_menu = None

        self.form_maker = FormMaker(self)

        self.insert_snippet(EXAMPLE_SNIPPET)

    def _update_databox(self):
        """Updates the databox from the database."""
        self._databox.clear_all_rows()
        snippets, rowids = self._get_all_snippets()
        for rowid, snippet in zip(rowids, snippets):
            values = (snippet.cdate, snippet.stype, snippet.lang,
                      snippet.title)
            self._databox.insert_row(rowid, values)

    def show_context_menu(self, event: tk.Event):
        """Displays the context menu for the selected row."""
        rowid = self._databox.tree.identify_row(event.y)
        if rowid:
            self._databox.tree.selection_set(rowid)
            self._row_id_context_menu = self._databox.tree.selection()[0]
            self._context_menu.post(event.x_root, event.y_root)

    def get_row_id_context_menu(self):
        """Returns the row id for which to display the context menu."""
        return self._row_id_context_menu

    #==== Database operations
    def _get_all_snippets(self):
        return self._db.get_all_snippets()

    def get_snippet_by_rowid(self, rowid: int):
        return self._db.query_by_rowid(rowid)

    def insert_snippet(self, snippet: Snippet):
        self._db.insert_snippet(snippet)
        self._update_databox()

    def update_snippet(self, rowid: int, snippet: Snippet):
        self._db.update_snippet(rowid, snippet)

    def delete_snippet(self, rowid: int):
        self._db.delete_snippet(rowid)
        self._update_databox()

    #==== Notebook operations
    def add_tab(self, tab_label: str, tab_content: tk.Widget, **kw):
        self._notebook.add_tab(tab_label, tab_content, **kw)

    def select_tab(self, tab_id: int):
        self._notebook.select(tab_id)

    def close_selected_tab(self):
        self._notebook.close_selected_tab()

    def _make_welcome_tab(self):
        page = ttk.Frame(self._notebook)
        page.pack(fill=tk.BOTH, expand=True)

        label = tk.Label(page, text=WELCOME_MESSAGE)
        label.pack(fill=tk.BOTH, expand=True)

        self._notebook.add_tab(page, "Welcome!")
