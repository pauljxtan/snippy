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

        self.tree = ttk.Treeview(self.parent)
        self.make_tree()

    def make_tree(self):
        """
        Builds the data tree.
        """
        self.tree.pack(fill='both', expand=True)
        self.tree['columns'] = ('creation_date', 'type', 'lang', 'title')
        self.tree.heading('creation_date', text="Creation date")
        self.tree.heading('type', text="Snippet type")
        self.tree.heading('lang', text="Language")
        self.tree.heading('title', text="Title")

        self.load_data()

    def load_data(self):
        """
        Inserts data into the tree.
        """
        rows = db.get_all_rows(self.conn, TABLE_NAME)
        for i, row in enumerate(rows):
            self.tree.insert("", i, text="", values=row)


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
