import Tkinter as tk
import ttk
import database as db

DB_FILENAME = "snippy.db"
TABLE_NAME = "snippy"


class SnippyGui(ttk.Frame):
    def __init__(self, parent, db_conn):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.conn = db_conn

        self.tree = self.make_tree()
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.parent)
        test_frame = ttk.Frame()
        test_text = tk.Text(test_frame)
        test_text.insert(tk.END, "FRAME TEXT")
        test_text.config(state=tk.DISABLED)
        test_text.pack()
        self.notebook.add(test_frame, text="TAB TEXT")
        self.notebook.pack(fill=tk.BOTH, expand=True)

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
        rows = db.get_all_rows(self.conn, TABLE_NAME)
        for i, row in enumerate(rows):
            tree.insert("", i, text="", values=row)

        return tree


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
    db.init_db(DB_FILENAME, TABLE_NAME, True)
    db_conn = db.get_connection(DB_FILENAME)

    root = tk.Tk()
    # root.geometry('640x480')
    root.title("Snippy")
    SnippyGui(root, db_conn).pack()
    root.mainloop()


if __name__ == '__main__':
    main()
