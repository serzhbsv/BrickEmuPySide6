import sys
import os

from PySide6 import QtWidgets

from ui import Window


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("BrickEmuPy")

    window = Window()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()