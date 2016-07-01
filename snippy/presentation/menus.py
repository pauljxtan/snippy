"""
The menubar and context menus.
"""

import tkinter as tk
from tkinter import messagebox

class MenuMaker(object):
    """
    Creates the menubar and context menus.
    """
    def __init__(self, gui):
        self.gui = gui

    def make_menubar(self):
        """
        Returns a menubar.
        """
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
        """
        Returns a context menu.
        """
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
