

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QUrl

from os.path import abspath

from .connection import Shell


class XtermView(QWebEngineView):
    def __init__(self, shell: Shell, parent=...):
        super().__init__(parent)
        channel = QWebChannel(self)
        channel.registerObject('shell', shell)
        self.page().setWebChannel(channel)
        self.load(QUrl.fromLocalFile(abspath('assets/xterm/index.html')))




