import Tkinter as tk
import ttk
from snippy.database import SnippyDB
from snippy.widgets import DataBox, MyNotebook

DB_FILENAME = "snippy.db"
TABLE_NAME = "snippy"
ROOT_TITLE = "Snippy"

class SnippyGui(ttk.Frame):
    def __init__(self, parent, db, verbose=False):
        ttk.Frame.__init__(self, parent)
        self._parent = parent
        self._db = db
        self.verbose = verbose

        self._databox = DataBox(self)
        self._databox.pack(fill=tk.BOTH, expand=True)
        self._update_databox()

        self._notebook = MyNotebook(self)
        self._notebook.pack(fill=tk.BOTH, expand=True)
        self._make_welcome_tab()

        self._context_menu = tk.Menu(self)
        self._make_context_menu()

    def _update_databox(self):
        self._databox.clear_all_rows()
        rows = self._db.get_all_rows()
        for _, row in enumerate(rows):
            self._databox.insert_row(row)

    def _make_context_menu(self):
        self._context_menu.add_command(label="Create", command=self._show_create_form)
        self._context_menu.add_command(label="Edit")
        self._context_menu.add_command(label="Delete")

    def _show_context_menu(self, event):
        iid = self._databox.tree.identify_row(event.y)
        if iid:
            print "Showing context menu for row %s" % iid
            # self._databox.tree.selection_set(iid)
            self._context_menu.post(event.x_root, event.y_root)

    def _show_create_form(self):
        form = self._make_create_form()
        self._notebook.add_tab(form, "Create snippet")
        self._notebook.select(form)

    def _make_create_form(self):
        form = ttk.Frame()

        ttk.Label(form, text="Create snippet").grid(row=0, columnspan=2)

        ttk.Label(form, text="Type").grid(row=1, column=0)
        ttk.Label(form, text="Language").grid(row=2, column=0)
        ttk.Label(form, text="Title").grid(row=3, column=0)
        ttk.Label(form, text="Code").grid(row=4, column=0)

        entry_type = ttk.Entry(form)
        entry_lang = ttk.Entry(form)
        entry_title = ttk.Entry(form)
        text_code = tk.Text(form)

        entry_type.grid(row=1, column=1)
        entry_lang.grid(row=2, column=1)
        entry_title.grid(row=3, column=1)
        text_code.grid(row=4, column=1)

        def create_snippet():
           self._db.insert_row(entry_type.get(), entry_lang.get(),
                               entry_title.get(), text_code.get("1.0", tk.END))
           self._update_databox()

        ttk.Button(form, text="Create", command=create_snippet).grid(
            row=5, columnspan=2)

        return form

    def _make_welcome_tab(self):
        page = ttk.Frame(self._notebook)
        page.pack(fill=tk.BOTH, expand=True)

        text = "Welcome to Snippy!\nTo get started, right-click on any snippet above."
        label = tk.Label(page, text=text)
        label.pack(fill=tk.BOTH, expand=True)

        self._notebook.add_tab(page, "Welcome!")

    #def _add_notebook_page(self, tab_text, text=""):
    #    page = ttk.Frame(self._notebook)
    #    page_text = tk.Text(page)
    #    page_text.insert(tk.END, text)
    #    page_text.pack(fill=tk.BOTH, expand=True)
    #    #self._notebook.add(page, text=tab_text)
    #    self._notebook.add_tab(page, tab_text)


def main():
    db = SnippyDB(DB_FILENAME, TABLE_NAME, clobber=True, verbose=True)

    root = tk.Tk()
    root.title(ROOT_TITLE)
    snippy_gui = SnippyGui(root, db, verbose=True)
    snippy_gui.pack(fill=tk.BOTH, expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()
