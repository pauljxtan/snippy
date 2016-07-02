"""Custom widgets."""

import tkinter as tk
from tkinter import ttk

from snippy.data.tabledefinitions import TABLE_STANDARD, TableDefinition
from snippy.utils.loggingtools import get_logger
from snippy.presentation.gui import SnippyGui
from collections.abc import Iterable

MODULE_NAME = "widgets"

class DataBox(ttk.Frame): # pylint: disable=too-many-ancestors
    """A wrapper around ttk.Treeview for displaying data.
    
    :param gui: Snippy GUI instance
    :type gui: snippy.presentation.gui.SnippyGui
    :param table_definition: Table definition
    :type table_definition: snippy.data.tabledefinitions.TableDefinition
    """
    def __init__(self, gui: SnippyGui,
                 table_definition: TableDefinition = TABLE_STANDARD):
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
        except tk.TclError as e:
            self._logger.error(e.__doc__)

    def clear_all_rows(self):
        """Deletes all rows in the tree."""
        self.tree.delete(*self.tree.get_children())

class MyNotebook(ttk.Frame): # pylint: disable=too-many-ancestors
    """A small wrapper around ttk.Notebook with a context menu."""
    def __init__(self, parent: tk.Widget, **kw):
        """
        :param parent: The parent widget
        :type parent: tkinter.Widget
        """
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
