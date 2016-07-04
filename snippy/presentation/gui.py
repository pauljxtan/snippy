"""
The Snippy GUI.
"""
from datetime import datetime
import tkinter as tk
from typing import Iterable
from tkinter import messagebox, ttk
from snippy.data.snippytypes import Snippet
from snippy.data.tabledefinitions import TABLE_STANDARD, TableDefinition
from snippy.logic.snippydb import SnippyDb
from snippy.utils.loggingtools import get_logger

MODULE_NAME = "widgets"

WELCOME_MESSAGE = ("Welcome to Snippy!\n"
                   "To get started, click on 'Create snippet' on the top menu,"
                   " or right-click on any snippet above.")
EXAMPLE_SNIPPET = Snippet(datetime(2001, 1, 1), "Function", "Python",
                          "Simple hello world",
                          "def hello_world():\n    print(Hello, world!)")


class SnippyGui(ttk.Frame):
    """The main snippy GUI.

    :param parent: Parent widget
    :type parent: Tkinter.Widget
    :param db: Database/table controller
    :type db: snippy.logic.tablecontroller.TableController
    """
    def __init__(self, parent: tk.Widget, db: SnippyDb, verbose=False):
        ttk.Frame.__init__(self)
        self.parent = parent
        self._db = db
        self._verbose = verbose

        self._databox = DataBox(self)
        self._databox.pack(fill=tk.BOTH, expand=True)
        self._update_databox()

        self._notebook = MyNotebook(self)
        self._notebook.pack(fill=tk.BOTH, expand=True)
        self._make_welcome_tab()

        self._menu_maker = MenuMaker(self)
        self.parent.config(menu=self._menu_maker.make_menubar())
        self._context_menu = self._menu_maker.make_context_menu()
        self._row_id_context_menu = None

        self.form_maker = FormMaker(self)

        self.insert_snippet(EXAMPLE_SNIPPET)

    def _update_databox(self):
        """Updates the databox from the database."""
        self._databox.clear_all_rows()
        snippets, rowids = self._get_all_snippets()
        for rowid, snippet in zip(rowids, snippets):
            values = (snippet.cdate, snippet.stype, snippet.lang,
                      snippet.title)
            self._databox.insert_row(rowid, values)

    def show_context_menu(self, event: tk.Event):
        """Displays the context menu for the selected row."""
        rowid = self._databox.tree.identify_row(event.y)
        if rowid:
            self._databox.tree.selection_set(rowid)
            self._row_id_context_menu = self._databox.tree.selection()[0]
            self._context_menu.post(event.x_root, event.y_root)

    def get_row_id_context_menu(self):
        """Returns the row id for which to display the context menu."""
        return self._row_id_context_menu

    # ==== Database operations

    def _get_all_snippets(self):
        return self._db.get_all_snippets()

    def get_snippet_by_rowid(self, rowid: int):
        """Returns the snippet with the given row ID."""
        return self._db.query_by_rowid(rowid)

    def insert_snippet(self, snippet: Snippet):
        """Inserts a snippet."""
        self._db.insert_snippet(snippet)
        self._update_databox()

    def update_snippet(self, rowid: int, snippet: Snippet):
        """Updates a snippet."""
        self._db.update_snippet(rowid, snippet)

    def delete_snippet(self, rowid: int):
        """Deletes a snippet."""
        self._db.delete_snippet(rowid)
        self._update_databox()

    # ==== Notebook operations
    def add_tab(self, tab_label: str, tab_content: tk.Widget, **kw):
        """Adds a tab to the notebook."""
        self._notebook.add_tab(tab_label, tab_content, **kw)

    def select_tab(self, tab_id: int):
        """Selects a tab on the notebook."""
        self._notebook.select(tab_id)

    def close_selected_tab(self):
        """Closes the selected tab on the notebook."""
        self._notebook.close_selected_tab()

    def _make_welcome_tab(self):
        page = ttk.Frame(self._notebook)
        page.pack(fill=tk.BOTH, expand=True)

        label = tk.Label(page, text=WELCOME_MESSAGE)
        label.pack(fill=tk.BOTH, expand=True)

        self._notebook.add_tab(page, "Welcome!")


class DataBox(ttk.Frame):
    """A wrapper around ttk.Treeview for displaying data.

    :param gui: Snippy GUI instance
    :type gui: snippy.presentation.gui.SnippyGui
    :param table_definition: Table definition
    :type table_definition: snippy.data.tabledefinitions.TableDefinition
    """
    def __init__(self, gui: SnippyGui,
                 table_definition: TableDefinition=TABLE_STANDARD):
        ttk.Frame.__init__(self, gui)
        self._logger = get_logger(MODULE_NAME)

        self.tree = ttk.Treeview(self,
                                 columns=table_definition.col_names_databox)
        for column, title in zip(table_definition.col_names_databox,
                                 table_definition.col_names_display_databox):
            self.tree.heading(column, text=title)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<Button-3>', gui.show_context_menu)

        scrollbar_x = ttk.Scrollbar(self.tree, orient=tk.HORIZONTAL,
                                    command=self.tree.xview)
        scrollbar_y = ttk.Scrollbar(self.tree, orient=tk.VERTICAL,
                                    command=self.tree.yview)
        self.tree.configure(xscroll=scrollbar_x.set, yscroll=scrollbar_y.set)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    def insert_row(self, iid: int, values: Iterable):
        """Inserts a row into the tree.

        :param iid: Row ID
        :type iid: int
        :param values: Row values
        :type values: list
        """
        try:
            self.tree.insert("", tk.END, iid=iid, text=iid, values=values)
        except tk.TclError as exc:
            self._logger.error(exc.__doc__)

    def clear_all_rows(self):
        """Deletes all rows in the tree."""
        self.tree.delete(*self.tree.get_children())


class MyNotebook(ttk.Frame):
    """A small wrapper around ttk.Notebook with a context menu.

    :param parent: The parent widget
    :type parent: tkinter.Widget
    """
    def __init__(self, parent: tk.Widget, **kw):
        ttk.Frame.__init__(self, parent)
        self._notebook = ttk.Notebook(self, **kw)
        self._notebook.pack(fill=tk.BOTH, expand=True)

        self._index_right_clicked = None

        self._context_menu = self._make_context_menu()
        self._notebook.bind('<Button-3>', self._on_right_click)

    def add_tab(self, tab_content: tk.Widget, tab_label: int, **kw):
        """Adds a new tab to the notebook.

        :param tab_content: Content to put in the tab (typically a Frame)
        :type tab_content: tkinter.Widget
        :param tab_label: Tab label
        :type tab_label: str
        """
        self._notebook.add(tab_content, text=tab_label, **kw)

    def _make_context_menu(self):
        """Returns a context menu."""
        menu = tk.Menu(self)

        def _close_tab_right_clicked():
            self._notebook.forget(self._index_right_clicked)
            self._index_right_clicked = None

        menu.add_command(label="Close tab", command=_close_tab_right_clicked)
        return menu

    def _on_right_click(self, event: tk.Event):
        if event.widget.identify(event.x, event.y) == 'label':
            index = event.widget.index('@%d,%d' % (event.x, event.y))
            self._index_right_clicked = index
            self._context_menu.post(event.x_root, event.y_root)

    def select(self, tab_id: int):
        """Selects a tab."""
        self._notebook.select(tab_id)

    def close_selected_tab(self):
        """Closes the selected tab."""
        self._notebook.forget(self._notebook.select())


class FormMaker(object):
    """Creates forms for creating and editing snippets."""
    def __init__(self, gui: SnippyGui):
        self.gui = gui

    def make_create_form(self):
        """Returns a snippet creation form."""
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

        def _create_snippet():
            snippet = Snippet(datetime.now(), entry_type.get(),
                              entry_lang.get(), entry_title.get(),
                              text_code.get("1.0", tk.END))
            self.gui.insert_snippet(snippet)
            self.gui.close_selected_tab()

        ttk.Button(form, text="Create", command=_create_snippet).grid(
            row=5, columnspan=2)

        return form

    def make_edit_form(self, row_id: int):
        """Returns a snippet editing form."""
        form = ttk.Frame()

        ttk.Label(form, text="Edit snippet").grid(row=0, columnspan=2)

        ttk.Label(form, text="Type").grid(row=1, column=0)
        ttk.Label(form, text="Language").grid(row=2, column=0)
        ttk.Label(form, text="Title").grid(row=3, column=0)
        ttk.Label(form, text="Code").grid(row=4, column=0)

        entry_type = ttk.Entry(form)
        entry_lang = ttk.Entry(form)
        entry_title = ttk.Entry(form)
        text_code = tk.Text(form)

        # Initialize with existing values
        row = self.gui.get_snippet_by_rowid(row_id)
        entry_type.insert(tk.END, row[1])
        entry_lang.insert(tk.END, row[2])
        entry_title.insert(tk.END, row[3])
        text_code.insert(tk.END, row[4])

        entry_type.grid(row=1, column=1)
        entry_lang.grid(row=2, column=1)
        entry_title.grid(row=3, column=1)
        text_code.grid(row=4, column=1)

        def _edit_snippet():
            self.gui.edit_row(row_id, entry_type.get(), entry_lang.get(),
                              entry_title.get(), text_code.get("1.0", tk.END))
            self.gui.close_selected_tab()

        ttk.Button(form, text="Submit", command=_edit_snippet).grid(
            row=5, columnspan=2)

        return form


class MenuMaker(object):
    """Creates the menubar and context menus.

    :param gui: Snippy GUI instance
    :type gui: snippy.presentation.gui.SnippyGui
    """
    def __init__(self, gui: SnippyGui):
        self.gui = gui

    def make_menubar(self):
        """Returns a menubar."""
        def _exit():
            self.gui.parent.quit()

        def _show_create_form():
            form = self.gui.form_maker.make_create_form()
            self.gui.add_tab(form, "Create snippet")
            self.gui.select_tab(form)

        menubar = tk.Menu(self.gui.parent)

        dropdown_file = tk.Menu(menubar)
        dropdown_file.add_command(label="Exit", command=_exit)
        menubar.add_cascade(label="File", menu=dropdown_file)

        menubar.add_command(label="Create snippet", command=_show_create_form)

        return menubar

    def make_context_menu(self):
        """Returns a context menu."""
        def _show_edit_form():
            form = self.gui.form_maker.make_edit_form(
                self.gui.get_row_id_context_menu())
            self.gui.add_tab(form, "Edit snippet")
            self.gui.select_tab(form)

        def _delete_confirm():
            result = messagebox.askquestion("Delete snippet", "Are you sure?")
            if result == 'yes':
                self.gui.delete_snippet(self.gui.get_row_id_context_menu())

        context_menu = tk.Menu(self.gui)

        context_menu.add_command(label="Edit", command=_show_edit_form)
        context_menu.add_command(label="Delete", command=_delete_confirm)

        return context_menu
