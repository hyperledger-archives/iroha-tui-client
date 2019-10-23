"""
Testing framework for interactive curses apps.
"""

import time
import pexpect
from pyte.screens import Screen
from pyte.streams import ByteStream
from termcolor import colored


class AppInstance:
    def __init__(self, shell_cmd):
        self._screen = Screen(80, 25)
        self._stream = ByteStream(self._screen)
        self._pexpect = pexpect.spawn("/bin/bash", ["-c", shell_cmd], use_poll=True)

    def send(self, input_: str):
        self._pexpect.send(input_)
        self._read_with_timeouts()

    def send_control(self, input_: str):
        self._pexpect.sendcontrol(input_)

    def send_movement(self, type_: str, n: int):
        codes = {
            "up": "\x1bOA",
            "down": "\033OB",
            "right": "\x1bOC",
            "left": "\x1bOD"
        }
        self.send(codes[type_] * n)

    def send_backspace(self, n: int):
        for _ in range(n):
            self.send_control("h")

    def expect_at(self, row: int, col: int, s: str):
        self._read_with_timeouts()
        ok = self._screen.display[row][col:].startswith(s)

        if not ok:
            self._dump_display()
            raise ValueError

    def expect(self, s: str):
        self.locate(s)

    def locate(self, s: str):
        for i, row in enumerate(self._screen.display):
            idx = row.find(s)
            if idx != -1:
                return i, idx

        self._dump_display()
        raise ValueError

    def close(self):
        self._pexpect.close()

    def _dump_display(self):
        good_colors = {"grey", "red", "green", "yellow", "blue", "magenta", "cyan",
                       "white"}

        print("-" * 80)
        for row in self._screen.buffer.values():
            for char in row.values():
                args = {}
                if char.fg in good_colors:
                    args["color"] = char.fg
                if char.bg in good_colors:
                    args["on_color"] = f"on_{char.bg}"
                print(colored(char.data, **args), end='')
            print("\r")
        print("-" * 80)

    def _read_with_timeouts(self, timeouts=1, overall_timeout=2):
        output = []
        begin = time.monotonic()
        try:
            while True:
                output.append(self._pexpect.read_nonblocking(timeout=timeouts))
                if time.monotonic() - begin > overall_timeout:
                    break
        except pexpect.exceptions.TIMEOUT:
            pass
        self._stream.feed(b"".join(output))


def main():
    instance = AppInstance("python3 -m torinaku")
    print(instance.locate("Iroha TUI"))
    instance.expect_at(3, 35, "Iroha TUI")


if __name__ == "__main__":
    main()
