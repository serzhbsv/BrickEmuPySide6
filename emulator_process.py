import time
from interconnect import CMD_BTN_PRESS, CMD_BTN_RELEASE, CMD_QUIT


class EmulatorProcess:
    def __init__(self, game_path, cmd_queue, data_sink):
        self._game_path = game_path
        self._cmd_queue = cmd_queue
        self._data_sink = data_sink
        self._is_running = True
        self._buttons = set()

    def _write_data(self, msg):
        self._data_sink.emit_data(msg)

    def _process_command(self, cmd):
        cmd_type = cmd[0]
        if cmd_type == CMD_BTN_PRESS:
            self._buttons.add(cmd[1])
        elif cmd_type == CMD_BTN_RELEASE:
            self._buttons.discard(cmd[1])
        elif cmd_type == CMD_QUIT:
            self._is_running = False

    def run(self):
        self._write_data(["status", f"Loaded: {self._game_path}"])

        tick = 0
        while self._is_running:
            try:
                cmd = self._cmd_queue.get(timeout=0.01)
                self._process_command(cmd)
            except Exception:
                pass

            tick += 1
            if tick % 50 == 0:
                btns = ", ".join(sorted(self._buttons)) if self._buttons else "—"
                self._write_data(["lcd_update", f"tick {tick}\nbuttons: {btns}"])

            time.sleep(0.02)

