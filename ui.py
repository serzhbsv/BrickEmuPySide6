from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QMessageBox, QLabel
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

        # Central widget с кнопкой вместо невидимого меню
        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        label = QLabel("No game loaded.\nOpen a .brick file to start.")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px; color: #333;")
        layout.addWidget(label)

        self.btn_open = QtWidgets.QPushButton("Open .brick file")
        self.btn_open.setMinimumHeight(64)
        self.btn_open.setStyleSheet("font-size: 18px; padding: 12px;")
        self.btn_open.clicked.connect(self._open_brick_file)
        layout.addWidget(self.btn_open)

        self.setCentralWidget(central)

    @Slot()
    def _open_brick_file(self):
        # На Android стартуем из директории приложения
        start_dir = os.environ.get("ANDROID_ARGUMENT", ".")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Brick Game", start_dir, "Brick files (*.brick);;All files (*)"
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

