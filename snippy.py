import Tkinter as tk
import ttk


class SnippyGui(object):
    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.frame.pack(expand=True)

        self.frame_main = ttk.Frame(self.frame)
        self.frame_main.pack(expand=True)

        self.tree = ttk.Treeview(self.frame)
        self.tree.insert("", 0, text='test')
        self.tree.pack()


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
    root = tk.Tk()
    root.geometry('640x480')
    root.title("Snippy")
    snippy_gui = SnippyGui(root)
    root.mainloop()


if __name__ == '__main__':
    main()
