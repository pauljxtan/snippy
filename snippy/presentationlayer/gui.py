"""
The application GUI.
"""

import Tkinter as tk
import ttk
from snippy.database import SnippyDB
from snippy.widgets import DataBox, MyNotebook
from snippy.forms import FormMaker
from snippy.menus import MenuMaker

DB_FILENAME = "snippy.db"
TABLE_NAME = "snippy"
ROOT_TITLE = "Snippy"
WELCOME_MESSAGE = ("Welcome to Snippy!\n"
                   "To get started, click on 'Create snippet' on the top menu,"
                   " or right-click on any snippet above.")


class SnippyGui(ttk.Frame): # pylint: disable=too-many-ancestors,too-many-instance-attributes
    """
    The application GUI.
    """
    def __init__(self, parent, db, verbose=False):
        ttk.Frame.__init__(self, parent)

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

        menubar = self._menu_maker.make_menubar()
        self.parent.config(menu=menubar)

        self._context_menu = tk.Menu(self)
        self._context_menu = self._menu_maker.make_context_menu()
        self._row_id_context_menu = None

        self.form_maker = FormMaker(self)

    def update_databox(self):
        """
        Updates the databox.
        """
        self._databox.clear_all_rows()
        rows = self._db.get_all_rows()
        for _, row in enumerate(rows):
            self._databox.insert_row(row)

    def _make_welcome_tab(self):
        """
        Creates the welcome tab.
        """
        page = ttk.Frame(self._notebook)
        page.pack(fill=tk.BOTH, expand=True)

        text = WELCOME_MESSAGE
        label = tk.Label(page, text=text)
        label.pack(fill=tk.BOTH, expand=True)

        self._notebook.add_tab(page, "Welcome!")

    def show_context_menu(self, event):
        """
        Displays the context menu for the selected row.
        """
        iid = self._databox.tree.identify_row(event.y)
        if iid:
            self._databox.tree.selection_set(iid)
            self._row_id_context_menu = self._databox.tree.selection()[0]
            self._context_menu.post(event.x_root, event.y_root)

    def get_row_id_context_menu(self):
        """
        Returns the row id for which to display the context menu.
        """
        return self._row_id_context_menu

    #---- Database operations -------------------------------------------------
    def get_row(self, row_id):
        """
        Returns the row specified by the given id.
        """
        return self._db.get_row(row_id)

    def insert_row(self, snippet_type, snippet_lang, snippet_title,
                   snippet_code):
        """
        Inserts a row into the database and refreshes the databox.
        """
        self._db.insert_row(snippet_type, snippet_lang, snippet_title,
                            snippet_code)
        self.update_databox()

    def edit_row(self, row_id, snippet_type, snippet_lang, snippet_title, # pylint: disable=too-many-arguments
                 snippet_code):
        """
        Replaces all elements in the row specified by the given id and
        refreshes the databox.
        """
        self._db.edit_row(row_id, snippet_type, snippet_lang, snippet_title,
                          snippet_code)
        self.update_databox()

    def delete_row(self, row_id):
        """
        Deletes the row specified by the given id and refreshes the databox.
        """
        self._db.delete_row(row_id)
        self.update_databox()
    #--------------------------------------------------------------------------

    #---- Notebook operations -------------------------------------------------
    def add_tab(self, tab_label, tab_content, **kw):
        """
        Adds a tab to the notebook.
        """
        self._notebook.add_tab(tab_label, tab_content, **kw)

    def select_tab(self, tab_id):
        """
        Selects a tab in the notebook.
        """
        self._notebook.select(tab_id)

    def close_selected_tab(self):
        """
        Closes the selected tab in the notebook.
        """
        self._notebook.close_selected_tab()
    #--------------------------------------------------------------------------


def main():
    """
    The main function.
    """
    snippy_db = SnippyDB(DB_FILENAME, TABLE_NAME, clobber=True, verbose=True)

    root = tk.Tk()
    root.title(ROOT_TITLE)
    snippy_gui = SnippyGui(root, snippy_db, verbose=True)
    snippy_gui.pack(fill=tk.BOTH, expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()
