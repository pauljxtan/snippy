import tkinter as tk

from snippy.logiclayer.snippydb import SnippyDb
from snippy.presentationlayer.gui import SnippyGui

DB_FILENAME = "snippy.db"
ROOT_TITLE = "Snippy"

snippy_db = SnippyDb(DB_FILENAME)

snippy_db._db_conn.execute("DELETE FROM snippy;")

root = tk.Tk()
root.title = ROOT_TITLE
snippy_gui = SnippyGui(root, snippy_db)
snippy_gui.pack(fill=tk.BOTH, expand=True)
root.mainloop()