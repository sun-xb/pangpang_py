


from PySide6.QtCore import QObject, Signal, Slot

class Connection(QObject):
    def open(self):
        raise NotImplementedError()

    def invoke_shell(self):
        raise NotImplementedError()




class Shell(QObject):
    transform = Signal(str)

    @Slot()
    def open(self):
        raise NotImplementedError()

    @Slot(str)
    def receive(self, msg):
        raise NotImplementedError()

    @Slot(int, int)
    def onResize(self, cols, rows):
        raise NotImplementedError()



    