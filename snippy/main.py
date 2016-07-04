"""
A simple tool for managing code snippets.
"""
import tkinter as tk
from snippy.presentation.gui import SnippyGui

ROOT_TITLE = "Snippy"


def main():
    root = tk.Tk()
    root.title = ROOT_TITLE
    snippy_gui = SnippyGui(root, clobber=True)
    snippy_gui.pack(fill=tk.BOTH, expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()