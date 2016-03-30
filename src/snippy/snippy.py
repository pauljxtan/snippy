import Tkinter as tk
import ttk
from database import SnippyDB

DB_FILENAME = "snippy.db"
TABLE_NAME = "snippy"


class SnippyGui(ttk.Frame):
    def __init__(self, parent, db, verbose=False):
        ttk.Frame.__init__(self, parent)
        self._parent = parent
        self._db = db
        self.verbose = verbose

        self.tree = self.make_tree()
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.notebook, self.code_text_frame, self.code_text \
            = self.make_notebook()
        self.display_code_in_notebook(1)

    def make_tree(self):
        """
        Builds the data tree.
        """
        tree = ttk.Treeview(self._parent)
        tree['columns'] = ('creation_date', 'type', 'lang', 'title')
        tree.heading('creation_date', text="Creation date")
        tree.heading('type', text="Snippet type")
        tree.heading('lang', text="Language")
        tree.heading('title', text="Title")

        return self.init_data(tree)

    def init_data(self, tree):
        """
        Inserts all existing data into the tree.
        """
        rows = self._db.get_all_rows()
        for i, row in enumerate(rows):
            tree.insert("", i, text="", values=row)

        return tree

    def make_notebook(self):
        notebook = ttk.Notebook(self._parent)
        code_text_frame = ttk.Frame()
        code_text = tk.Text(code_text_frame)
        code_text.config(state=tk.DISABLED)
        code_text.pack()
        notebook.add(code_text_frame, text="TAB TEXT")
        notebook.pack(fill=tk.BOTH, expand=True)

        return notebook, code_text_frame, code_text

    def display_code_in_notebook(self, row_id):
        code = self._db.get_unique_elem(row_id, 'code')
        self.code_text.insert(tk.END, "TEST")
        self.code_text.insert(tk.END, code)


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
    root.title("Snippy")
    SnippyGui(root, db, verbose=True)
    root.mainloop()


if __name__ == '__main__':
    main()
