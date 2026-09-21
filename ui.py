from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFileDialog, QMessageBox
import os

from brick_widget import BrickWidget


UI_DIR = os.path.dirname(os.path.abspath(__file__))


def _ui_path(name):
    return os.path.join(UI_DIR, "ui", name)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._current_brick = None

        self.setWindowTitle("BrickEmuPy")

        self.actionOpen = QtWidgets.QAction("Open Brick File", self)
        self.actionOpen.triggered.connect(self._open_brick_file)
        self.menuBar().addMenu("File").addAction(self.actionOpen)

        self.actionExit = QtWidgets.QAction("Exit", self)
        self.actionExit.triggered.connect(self.close)
        self.menuBar().addMenu("File").addAction(self.actionExit)

    @Slot()
    def _open_brick_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Brick Game", "", "Brick files (*.brick);;All files (*)"
        )
        if not file_path:
            return
        self._load_game(file_path)

    def _load_game(self, path):
        if self._current_brick:
            self._current_brick.stop_emulator()
            self._current_brick.deleteLater()

        widget = BrickWidget(path)
        self.setCentralWidget(widget)
        self._current_brick = widget

    def closeEvent(self, event):
        if self._current_brick:
            self._current_brick.stop_emulator()
        event.accept()
