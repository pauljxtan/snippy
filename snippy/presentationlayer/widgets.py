"""
Custom widgets.
"""

import tkinter as tk
from tkinter import ttk

from snippy.utils.loggingtools import get_logger

# TODO: import these
TABLE_COLUMNS = ('creation_date', 'type', 'lang', 'title')
TABLE_TITLES = ('Creation date', 'Snippet Type', 'Language', 'Title')

class DataBox(ttk.Frame): # pylint: disable=too-many-ancestors
    """
    A wrapper around ttk.Treeview for displaying data.
    """
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self._logger = get_logger('widgets')
        self._parent = parent
        self.tree = ttk.Treeview(self, columns=TABLE_COLUMNS)
        for column, title in zip(TABLE_COLUMNS, TABLE_TITLES):
            self.tree.heading(column, text=title)
        # TODO: scrollbars?
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<Button-3>', parent.show_context_menu)

    def insert_row(self, row):
        """
        Inserts a row into the tree.
        """
        #values = row[:-1]
        #iid = row[-1]
        values = (row['creation_date'], row['snippet_type'], row['language'],
                  row['title'])
        rowid = row['rowid']
        try:
            self.tree.insert("", tk.END, iid=rowid, text=rowid, values=values)
        except tk.TclError as e:
            self._logger.error(e.__doc__)

    def clear_all_rows(self):
        """
        Deletes all rows in the tree.
        """
        self.tree.delete(*self.tree.get_children())

class MyNotebook(ttk.Frame): # pylint: disable=too-many-ancestors
    """
    A small wrapper around ttk.Notebook with a context menu for closing tabs.
    """
    def __init__(self, parent, **kw):
        """
        :param parent: The parent widget
        :type parent: Tkinter.Widget
        """
        ttk.Frame.__init__(self, parent)
        self._notebook = ttk.Notebook(self, **kw)
        self._notebook.pack(fill=tk.BOTH, expand=True)

        self._index_right_clicked = None

        self._context_menu = self._make_context_menu()
        self._notebook.bind('<Button-3>', self._on_right_click)

    def add_tab(self, tab_content, tab_label, **kw):
        """
        Adds a new tab to the notebook.

        :param tab_content: Stuff to put in the tab (typically a Frame)
        :type tab_content: Tkinter.Widget
        :param tab_label: Tab label
        :type tab_label: String
        """
        self._notebook.add(tab_content, text=tab_label, **kw)

    def _make_context_menu(self):
        """
        Returns a context menu.
        """
        menu = tk.Menu(self)

        def _close_tab_right_clicked():
            self._notebook.forget(self._index_right_clicked)
            self._index_right_clicked = None

        menu.add_command(label="Close tab", command=_close_tab_right_clicked)
        return menu

    def _on_right_click(self, event):
        """
        Handles a right-click event.
        """
        if event.widget.identify(event.x, event.y) == 'label':
            index = event.widget.index('@%d,%d' % (event.x, event.y))
            self._index_right_clicked = index
            self._context_menu.post(event.x_root, event.y_root)

    def select(self, tab_id):
        """
        Selects a tab.
        """
        self._notebook.select(tab_id)

    def close_selected_tab(self):
        """
        Closes the selected tab.
        """
        self._notebook.forget(self._notebook.select())
