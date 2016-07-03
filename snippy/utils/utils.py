"""
Utility functions.
"""
from snippy.data.snippytypes import Snippet


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


def get_row_from_snippet(snippet: Snippet):
    """Converts a Snippet instance to a row dict."""
    return {'creation_date': snippet.cdate,
            'snippet_type': snippet.stype,
            'language': snippet.lang,
            'title': snippet.title,
            'code': snippet.code}


def get_snippet_from_row(row: dict):
    """Converts a row dict to a Snippet instance."""
    return Snippet(row['creation_date'], row['snippet_type'],
                   row['language'], row['title'], row['code'])


def get_snippets_from_rows(rows: list):
    """Converts a list of row dicts to a list of Snippet instances."""
    return [get_snippet_from_row(row) for row in rows]
