import logging

class Snippet:
    """A code snippet."""
    def __init__(self, creation_date, snippet_type, language, title, code):
        self.cdate = creation_date
        self.stype = snippet_type
        self.lang = language
        self.title = title
        self.code = code
        logging.info("Initialized: {0}".format(self))

    def __str__(self):
        return "Snippet: {0} / {1} / {2}".format(self.stype, self.lang,
                                                 self.title)