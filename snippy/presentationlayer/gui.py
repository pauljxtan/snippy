import tkinter as tk
from tkinter import ttk

from snippy.logiclayer.snippydb import SnippyDb
from snippy.presentationlayer.widgets import DataBox, MyNotebook
from snippy.presentationlayer.forms import FormMaker
from snippy.presentationlayer.menus import MenuMaker

WELCOME_MESSAGE = ("Welcome to Snippy!\n"
                   "To get started, click on 'Create snippet' on the top menu,"
                   " or right-click on any snippet above.")

class SnippyGui(ttk.Frame):
    def __init__(self, parent, db, verbose=False):
        ttk.Frame.__init__(self)
        self.parent = parent
        self._db = db
        self.verbose = verbose

        self._databox = DataBox(self)
        self._databox.pack(fill=tk.BOTH, expand=True)
        self.update_databox()

        self._notebook = MyNotebook(self)
        self._notebook.pack(fill=tk.BOTH, expand=True)
        self._make_welcome_tab()

        self._menu_maker = MenuMaker(self)
        self.parent.config(menu=self._menu_maker.make_menubar())
        self._context_menu = self._menu_maker.make_context_menu()
        self._row_id_context_menu = None

        self.form_maker = FormMaker(self)

    def update_databox(self):
        self._databox.clear_all_rows()
        rows = self.get_all_snippets()
        for _, row in enumerate(rows):
            self._databox.insert_row(row)

    def _make_welcome_tab(self):
        page = ttk.Frame(self._notebook)
        page.pack(fill=tk.BOTH, expand=True)

        label = tk.Label(page, text=WELCOME_MESSAGE)
        label.pack(fill=tk.BOTH, expand=True)

        self._notebook.add_tab(page, "Welcome!")

    def show_context_menu(self, event):
        """
        Displays the context menu for the selected row.
        """
        rowid = self._databox.tree.identify_row(event.y)
        if rowid:
            self._databox.tree.selection_set(rowid)
            self._row_id_context_menu = self._databox.tree.selection()[0]
            self._context_menu.post(event.x_root, event.y_root)

    def get_row_id_context_menu(self):
        """
        Returns the row id for which to display the context menu.
        """
        return self._row_id_context_menu

    #==== Database operations
    def get_all_snippets(self):
        return self._db.query_all()

    def get_snippet_by_rowid(self, rowid):
        return self._db.query_by_rowid(rowid)

    def insert_snippet(self, snippet):
        self._db.insert_snippet(snippet)

    def update_snippet(self, rowid, snippet):
        self._db.update_snippet(rowid, snippet)

    def delete_snippet(self, rowid):
        self._db.delete_snippet(rowid)

    #==== Notebook operations
    def add_tab(self, tab_label, tab_content, **kw):
        self._notebook.add_tab(tab_label, tab_content, **kw)

    def select_tab(self, tab_id):
        self._notebook.select(tab_id)

    def close_selected_tab(self):
        self._notebook.close_selected_tab()

