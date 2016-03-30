import Tkinter as tk
import ttk
from database import SnippyDB, TABLE_COLUMNS, TABLE_TITLES

DB_FILENAME = "snippy.db"
TABLE_NAME = "snippy"


class SnippyGui(ttk.Frame):
    def __init__(self, parent, db, verbose=False):
        ttk.Frame.__init__(self, parent)
        self._parent = parent
        self._db = db
        self.verbose = verbose

        self.data_box = DataBox(self)
        self._init_data()
        self.data_box.pack(fill=tk.BOTH, expand=True)

        self._notebook, self._code_text_frame, self._code_text \
            = self._make_notebook()
        self._display_code_in_notebook(1)

    def _init_data(self):
        """
        Initialize the data box with existing data.
        """
        rows = self._db.get_all_rows()
        for i, row in enumerate(rows):
            print row
            self.data_box.insert_row(row)

    def _make_notebook(self):
        notebook = ttk.Notebook(self._parent)
        code_text_frame = ttk.Frame()
        code_text = tk.Text(code_text_frame)
        # code_text.config(state=tk.DISABLED)
        code_text.pack()
        notebook.add(code_text_frame, text="TAB TEXT")
        notebook.pack(fill=tk.BOTH, expand=True)

        return notebook, code_text_frame, code_text

    def _display_code_in_notebook(self, row_id):
        code = self._db.get_unique_elem(row_id, 'code')
        self._code_text.insert(tk.END, code)


class DataBox(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self._parent = parent
        self._tree = None
        self._make_tree()

    def _make_tree(self):
        self.tree = ttk.Treeview(columns=TABLE_COLUMNS)
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
    SnippyGui(root, db, verbose=True)
    center(root)
    root.mainloop()


if __name__ == '__main__':
    main()
