from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal, QThread, Slot
import queue
from functools import partial

from interconnect import CMD_BTN_PRESS, CMD_BTN_RELEASE, CMD_QUIT


class EmulatorThread(QThread):
    messageSignal = Signal(list)

    def __init__(self, game_path, cmd_queue):
        super().__init__()
        self._game_path = game_path
        self._cmd_queue = cmd_queue
        self._running = True

    def run(self):
        from emulator_process import EmulatorProcess
        proc = EmulatorProcess(self._game_path, self._cmd_queue, self)
        proc.run()

    def emit_data(self, msg):
        self.messageSignal.emit(msg)

    def send_command(self, cmd):
        self._cmd_queue.put(cmd)

    def stop(self):
        self._cmd_queue.put((CMD_QUIT,))
        self.wait(2000)


class BrickWidget(QtWidgets.QWidget):
    def __init__(self, game_path):
        super().__init__()

        self._game_path = game_path
        self._emulator_thread = None
        self._cmd_queue = queue.Queue()

        layout = QtWidgets.QVBoxLayout(self)

        self._lcd_label = QtWidgets.QLabel("Loading...")
        self._lcd_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._lcd_label.setMinimumSize(320, 240)
        self._lcd_label.setStyleSheet("background: #9ea7a6; color: #1a1a1a; font-family: monospace;")
        layout.addWidget(self._lcd_label)

        btn_layout = QtWidgets.QHBoxLayout()
        for name in ["left", "right", "up", "down", "a", "b", "start"]:
            btn = QtWidgets.QPushButton(name)
            btn.setMinimumSize(48, 48)
            btn.pressed.connect(partial(self._send_cmd, CMD_BTN_PRESS, name))
            btn.released.connect(partial(self._send_cmd, CMD_BTN_RELEASE, name))
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        self._start_emulator()

    def _send_cmd(self, cmd_type, name):
        self._cmd_queue.put((cmd_type, name))

    def _start_emulator(self):
        if self._emulator_thread:
            return
        self._emulator_thread = EmulatorThread(self._game_path, self._cmd_queue)
        self._emulator_thread.messageSignal.connect(self._process_message)
        self._emulator_thread.start()

    @Slot(list)
    def _process_message(self, msg):
        if not msg:
            return
        tag = msg[0]
        if tag == "lcd_update":
            text = msg[1] if len(msg) > 1 else ""
            self._lcd_label.setText(text)
        elif tag == "status":
            self._lcd_label.setText(msg[1] if len(msg) > 1 else "")

    def stop_emulator(self):
        if self._emulator_thread:
            self._emulator_thread.stop()
            self._emulator_thread = None
