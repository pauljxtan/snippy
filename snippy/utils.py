"""
Utility functions.
"""

def center(win):
    """
    Centers the window on the screen.
    @param win: Tkinter window
    """
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    center_x = (win.winfo_screenwidth() // 2) - (width // 2)
    center_y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, center_x, center_y))
