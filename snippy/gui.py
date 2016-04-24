import Tkinter as tk
import ttk
from snippy.database import SnippyDB
from snippy.widgets import DataBox, MyNotebook
from snippy.forms import FormMaker
from snippy.menus import MenuMaker

DB_FILENAME = "snippy.db"
TABLE_NAME = "snippy"
ROOT_TITLE = "Snippy"
WELCOME_MESSAGE  = ("Welcome to Snippy!\n"
                    "To get started, click on 'Create snippet' on the top menu,"
                    " or right-click on any snippet above.")


class SnippyGui(ttk.Frame):
    def __init__(self, parent, db, verbose=False):
        ttk.Frame.__init__(self, parent)

        self._parent = parent
        self._db = db
        self.verbose = verbose

        self._databox = DataBox(self)
        self._databox.pack(fill=tk.BOTH, expand=True)
        self.update_databox()

        self._notebook = MyNotebook(self)
        self._notebook.pack(fill=tk.BOTH, expand=True)
        self._make_welcome_tab()

        self._menu_maker = MenuMaker()

        menubar = self._menu_maker.make_menubar(self)
        self._parent.config(menu=menubar)

        self._context_menu = tk.Menu(self)
        self._context_menu = self._menu_maker.make_context_menu(self)
        self._row_id_context_menu = None

        self._form_maker = FormMaker()

    def update_databox(self):
        self._databox.clear_all_rows()
        rows = self._db.get_all_rows()
        for _, row in enumerate(rows):
            self._databox.insert_row(row)

    def _make_welcome_tab(self):
        page = ttk.Frame(self._notebook)
        page.pack(fill=tk.BOTH, expand=True)

        text = WELCOME_MESSAGE
        label = tk.Label(page, text=text)
        label.pack(fill=tk.BOTH, expand=True)

        self._notebook.add_tab(page, "Welcome!")

    def _show_context_menu(self, event):
        iid = self._databox.tree.identify_row(event.y)
        if iid:
            self._databox.tree.selection_set(iid)
            self._row_id_context_menu = self._databox.tree.selection()[0]
            self._context_menu.post(event.x_root, event.y_root)

    #---- Database operations -------------------------------------------------
    def get_row(self, row_id):
        return self._db.get_row(row_id)

    def insert_row(self, snippet_type, snippet_lang, snippet_title,
                   snippet_code):
        self._db.insert_row(snippet_type, snippet_lang, snippet_title,
                            snippet_code)

    def edit_row(self, row_id, snippet_type, snippet_lang, snippet_title,
                 snippet_code):
        self._db.edit_row(row_id, snippet_type, snippet_lang, snippet_title,
                      snippet_code)
    #--------------------------------------------------------------------------

    #---- Notebook operations -------------------------------------------------
    def close_selected_tab(self):
        self._notebook.close_selected_tab()
    #--------------------------------------------------------------------------


def main():
    db = SnippyDB(DB_FILENAME, TABLE_NAME, clobber=True, verbose=True)

    root = tk.Tk()
    root.title(ROOT_TITLE)
    snippy_gui = SnippyGui(root, db, verbose=True)
    snippy_gui.pack(fill=tk.BOTH, expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()
