import Tkinter as tk
import ttk
import tkMessageBox


class MenuMaker:
    def make_menubar(self, gui):
        def _show_create_form():
            form = gui._form_maker.make_create_form(gui)
            gui._notebook.add_tab(form, "Create snippet")
            gui._notebook.select(form)

        menubar = tk.Menu(gui._parent)

        dropdown_file = tk.Menu(menubar)
        dropdown_file.add_command(label="Exit")
        menubar.add_cascade(label="File", menu=dropdown_file)

        menubar.add_command(label="Create snippet", command=_show_create_form)

        return menubar
        
    def make_context_menu(self, gui):
        def _show_edit_form():
            form = gui._form_maker.make_edit_form(gui, gui._row_id_context_menu)
            gui._notebook.add_tab(form, "Edit snippet")
            gui._notebook.select(form)

        def _delete_confirm():
            result = tkMessageBox.askquestion("Delete snippet", "Are you sure?")
            if result == 'yes':
                gui.delete_row(gui._row_id_context_menu)

        context_menu = tk.Menu(gui)

        context_menu.add_command(label="Edit", command=_show_edit_form)
        context_menu.add_command(label="Delete", command=_delete_confirm)

        return context_menu
