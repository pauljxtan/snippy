import Tkinter as tk
import ttk
from snippy.database import SnippyDB
from snippy.widgets import DataBox

DB_FILENAME = "snippy.db"
TABLE_NAME = "snippy"


class SnippyGui(ttk.Frame):
    def __init__(self, parent, db, verbose=False):
        ttk.Frame.__init__(self, parent)
        self._parent = parent
        self._db = db
        self.verbose = verbose

        self._databox = self._make_databox()
        self._databox.pack(fill=tk.BOTH, expand=True)

        self._notebook = ttk.Notebook(self)
        self._notebook.pack(fill=tk.BOTH, expand=True)

        self._context_menu = self._make_context_menu()

        # TESTING ONLY
        title = self._db.get_unique_elem(1, 'title')
        code = self._db.get_unique_elem(1, 'code')
        self._add_notebook_page(title, code)

    def _make_databox(self):
        """
        Initialize a data box with existing data.
        """
        databox = DataBox(self)
        rows = self._db.get_all_rows()
        for _, row in enumerate(rows):
            databox.insert_row(row)
        return databox

    def _add_notebook_page(self, tab_text, text=""):
        page = ttk.Frame(self._notebook)
        page_text = tk.Text(page)
        page_text.insert(tk.END, text)
        page_text.pack(fill=tk.BOTH, expand=True)
        self._notebook.add(page, text=tab_text)

    def _make_context_menu(self):
        menu = tk.Menu(self)
        menu.add_command(label="Create", command=self._show_create_form)
        menu.add_command(label="Edit")
        menu.add_command(label="Delete")
        return menu

    def _show_context_menu(self, event):
        iid = self._databox.tree.identify_row(event.y)
        if iid:
            print "Showing context menu for row %s" % iid
            # self._databox.tree.selection_set(iid)
            self._context_menu.post(event.x_root, event.y_root)

    def _show_create_form(self):
        form = self._make_create_form()
        self._notebook.add(form, text="Create snippet")
        self._notebook.select(form)

    def _make_create_form(self):
        form = ttk.Frame(self._notebook)
        ttk.Label(form, text="Title").grid(row=0, column=0)
        ttk.Entry(form).grid(row=0, column=1)
        ttk.Label(form, text="Type").grid(row=1, column=0)
        ttk.Entry(form).grid(row=1, column=1)
        ttk.Label(form, text="Language").grid(row=2, column=0)
        ttk.Entry(form).grid(row=2, column=1)
        ttk.Label(form, text="Description").grid(row=3, column=0)
        ttk.Entry(form).grid(row=3, column=1)
        return form


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
