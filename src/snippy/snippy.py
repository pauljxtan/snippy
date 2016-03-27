import Tkinter as tk
import ttk
import database as db

DB_FILENAME = "snippy.db"


class SnippyGui(ttk.Frame):
    def __init__(self, parent, db_conn, table_name="snippy", verbose=False):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.conn = db_conn
        self.table_name = table_name
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
        tree = ttk.Treeview(self.parent)
        tree['columns'] = ('creation_date', 'type', 'lang', 'title')
        tree.heading('creation_date', text="Creation date")
        tree.heading('type', text="Snippet type")
        tree.heading('lang', text="Language")
        tree.heading('title', text="Title")

        tree = self.init_data(tree)

        return tree

    def init_data(self, tree):
        """
        Inserts all existing data into the tree.
        """
        rows = db.get_all_rows(self.conn, self.table_name)
        print rows
        for i, row in enumerate(rows):
            print row
            tree.insert("", i, text="", values=row)

        return tree

    def make_notebook(self):
        notebook = ttk.Notebook(self.parent)
        code_text_frame = ttk.Frame()
        code_text = tk.Text(code_text_frame)
        code_text.config(state=tk.DISABLED)
        code_text.pack()
        notebook.add(code_text_frame, text="TAB TEXT")
        notebook.pack(fill=tk.BOTH, expand=True)

        return notebook, code_text_frame, code_text

    def display_code_in_notebook(self, row_id):
        code = db.get_unique_elem(self.conn, self.table_name, row_id, 'code',
                                  self.verbose)
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
    db.init_db(DB_FILENAME, "snippy", True)
    db_conn = db.get_connection(DB_FILENAME)

    root = tk.Tk()
    # root.geometry('640x480')
    root.title("Snippy")
    SnippyGui(root, db_conn, "snippy", True)
    root.mainloop()


if __name__ == '__main__':
    main()
