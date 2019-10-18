"""
Testing framework for interactive curses apps.
"""

import pexpect
from pyte.screens import Screen
from pyte.streams import ByteStream


class AppInstance:
    def __init__(self, shell_cmd):
        self._screen = Screen(80, 25)
        self._stream = ByteStream(self._screen)
        self._pexpect = pexpect.spawn("/bin/bash", ["-c", shell_cmd], use_poll=True)

    def send(self, input_: str):
        self._pexpect.send(input_)

    def send_control(self, input_: str):
        self._pexpect.sendcontrol(input_)

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
        self._read_with_timeouts()

        for i, row in enumerate(self._screen.display):
            idx = row.find(s)
            if idx != -1:
                return i, idx

        self._dump_display()
        raise ValueError

    def close(self):
        self._pexpect.close()

    def _dump_display(self):
        print("-" * 80)
        print("\n".join(self._screen.display))
        print("-" * 80)
        print(self._screen.cursor.x, self._screen.cursor.y)
        print("-" * 80)

    def _read_with_timeouts(self, timeouts=1):
        output = []
        try:
            while True:
                output.append(self._pexpect.read_nonblocking(timeout=timeouts))
        except pexpect.exceptions.TIMEOUT:
            pass
        self._stream.feed(b"".join(output))


def main():
    instance = AppInstance("python3 -m torinaku")
    print(instance.locate("Iroha TUI"))
    instance.expect_at(3, 35, "Iroha TUI")


if __name__ == "__main__":
    main()
