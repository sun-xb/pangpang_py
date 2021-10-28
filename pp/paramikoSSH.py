

from .connection import Connection, Shell
from paramiko import client, Channel

from PySide6.QtCore import QSocketNotifier, QSocketDescriptor, QSocketNotifier


class SSHConnection(Connection):
    def open(self, host, port, user, password):
        self.ssh = client.SSHClient()
        self.ssh.set_missing_host_key_policy(client.WarningPolicy)
        self.ssh.connect(host, port, user, password)

    def invoke_shell(self):
        channel = self.ssh.invoke_shell('xterm-256color')
        shell = SSHShell(channel, self)
        return shell


class SSHShell(Shell):
    def __init__(self, channel: Channel, parent) -> None:
        super().__init__(parent)
        self.channel = channel
        self.read_notifier = QSocketNotifier(channel.fileno(), QSocketNotifier.Read, self)
        self.read_notifier.setEnabled(False)
        self.read_notifier.activated.connect(self.on_shell_data)

    def open(self):
        self.read_notifier.setEnabled(True)

    def receive(self, msg):
        self.channel.sendall(msg)

    def onResize(self, cols, rows):
        self.channel.resize_pty(cols, rows)

    def on_shell_data(self, socket: QSocketDescriptor, type: QSocketNotifier.Type):
        if socket.isValid():
            data = self.channel.recv(1024)
            data = str(data, 'utf8')
            self.transform.emit(data)
    

    


if __name__ == '__main__':
    ssh = SSHPty()
    ssh.open()
    