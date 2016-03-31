import Tkinter as tk
import ttk
from snippy.database import SnippyDB, TABLE_COLUMNS, TABLE_TITLES

DB_FILENAME = "snippy.db"
TABLE_NAME = "snippy"


class SnippyGui(ttk.Frame):
    def __init__(self, parent, db, verbose=False):
        ttk.Frame.__init__(self, parent)
        self._parent = parent
        self._db = db
        self.verbose = verbose

        self._data_box = DataBox(self)
        self._init_data()
        self._data_box.pack(fill=tk.BOTH, expand=True)

        self._notebook = ttk.Notebook(self)
        self._notebook.pack(fill=tk.BOTH, expand=True)

        # TESTING ONLY
        title = self._db.get_unique_elem(1, 'title')
        code = self._db.get_unique_elem(1, 'code')
        self._add_notebook_page(title, code)

    def _init_data(self):
        """
        Initialize the data box with existing data.
        """
        rows = self._db.get_all_rows()
        for _, row in enumerate(rows):
            self._data_box.insert_row(row)

    def _add_notebook_page(self, tab_text, text):
        page = ttk.Frame(self._notebook)
        page_text = tk.Text(page)
        page_text.insert(tk.END, text)
        page_text.pack(fill=tk.BOTH, expand=True)
        self._notebook.add(page, text=tab_text)


class DataBox(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self._parent = parent
        self.tree = ttk.Treeview(self, columns=TABLE_COLUMNS)
        for column, title in zip(TABLE_COLUMNS, TABLE_TITLES):
            self.tree.heading(column, text=title)
        # TODO: scrollbars?
        self.tree.pack(fill=tk.BOTH, expand=True)

    def insert_row(self, row):
        self.tree.insert("", tk.END, text=row[-1], values=row[:-1])


def center(win):
    """
    Centers the window on the screen.
    @param win: Tkinter window
    """
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def main():
    db = SnippyDB(DB_FILENAME, TABLE_NAME, clobber=True, verbose=True)

    root = tk.Tk()
    # root.geometry('640x480')
    # center(root)
    root.title("Snippy")
    snippy_gui = SnippyGui(root, db, verbose=True)
    snippy_gui.pack(fill=tk.BOTH, expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()
