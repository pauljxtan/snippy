import datetime
import enum

class Language(enum.Enum):
    Python = 0

class Snippet:
    """Represents a code snippet.

    :param creation_date: Creation date
    :type creation_date: datetime.datetime
    :param snippet_type: Snippet type
    :type snippet_type: str
    :param language: Programming language
    :type language: str
    :param title: Title
    :type title: str
    :param code: Code
    :type code: str
    """
    def __init__(self, creation_date: datetime.datetime, snippet_type: str,
                 language: str, title: str, code: str):
        self.cdate = creation_date
        self.stype = snippet_type
        self.lang = language
        self.title = title
        self.code = code

    def __str__(self):
        return "Snippet: {0} / {1} / {2}".format(self.stype, self.lang,
                                                 self.title)