import sys
import os

print("[DEBUG] main.py started", flush=True)

from PySide6 import QtWidgets
print("[DEBUG] PySide6 imported", flush=True)

from ui import Window
print("[DEBUG] Window imported", flush=True)


def main():
    print("[DEBUG] main() called", flush=True)
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("BrickEmuPy")

    window = Window()
    print("[DEBUG] Window created", flush=True)
    window.show()
    print("[DEBUG] Window shown", flush=True)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
