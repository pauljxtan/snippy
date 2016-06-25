"""
Snippet creation and editing forms.
"""

import Tkinter as tk
import ttk


class FormMaker(object):
    """
    Creates snippet creation and editing forms.
    """
    def __init__(self, gui):
        self.gui = gui

    def make_create_form(self):
        """
        Returns a snippet creation form.
        """
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
            self.gui.insert_row(entry_type.get(), entry_lang.get(),
                                entry_title.get(), text_code.get("1.0", tk.END))
            self.gui.close_selected_tab()

        ttk.Button(form, text="Create", command=_create_snippet).grid(
            row=5, columnspan=2)

        return form

    def make_edit_form(self, row_id):
        """
        Returns a snippet editing form.
        """
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
        row = self.gui.get_row(row_id)
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
