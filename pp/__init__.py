


from PySide6 import QtWidgets
from urllib.parse import urlparse

from .xtermView import XtermView
from .paramikoSSH import SSHConnection



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('pangpang shell')
        self._mdi = QtWidgets.QMdiArea(self)
        self._mdi.setViewMode(QtWidgets.QMdiArea.TabbedView)
        self._mdi.setTabsClosable(True)
        self.setCentralWidget(self._mdi)

        self._quick_connect_bar = QtWidgets.QToolBar(self)
        self.addToolBar(self._quick_connect_bar)
        quick_connect_label = QtWidgets.QLabel(self._quick_connect_bar)
        quick_connect_label.setText('Quick Connect:')
        self._quick_connect_bar.addWidget(quick_connect_label)
        self._quick_connect_edit = QtWidgets.QLineEdit(self._quick_connect_bar)
        self._quick_connect_edit.setClearButtonEnabled(True)
        self._quick_connect_edit.returnPressed.connect(self.quick_command)
        self._quick_connect_bar.addWidget(self._quick_connect_edit)

    def quick_command(self):
        cmd = self._quick_connect_edit.text().strip()
        self.open_url(cmd)

    def open_url(self, url):
        parse_result = urlparse(url)
        if parse_result.scheme == 'ssh':
            ssh = SSHConnection(self)
            ssh.open(parse_result.hostname, parse_result.port, parse_result.username, parse_result.password)
            shell = ssh.invoke_shell()
            shellView = XtermView(shell, self)
            shellView.setWindowTitle(parse_result.username + '@' + parse_result.hostname + ':' + str(parse_result.port))
            self._mdi.addSubWindow(shellView)
            shellView.show()
            shellView.setFocus()
        else:
            raise NotImplementedError()



def main(*argv):
    app = QtWidgets.QApplication(list(argv))
    win = MainWindow()
    win.show()
    win.resize(800, 600)
    return app.exec()


if __name__ == '__main__':
    import sys
    main(*sys.argv, '--single-process')
