from contextlib import contextmanager
from unittest.mock import MagicMock
from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen, Canvas
from termcolor import colored
from iroha_tui.app.screen_manager import ScreenManager
from iroha_tui.screens.selector import SelectorView
from iroha_tui.models.mode_selector import ModeSelectorModel
from tests.app import TestIrohaTUI


COLORS = dict(
    zip(
        range(8),
        [
            "grey",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
        ]
    )
)


class IrohaTUITestInstance:
    def __init__(self):
        self.instance = TestIrohaTUI()

        self.screen = MagicMock(spec=Screen, colours=8, unicode_aware=False)
        self.canvas = Canvas(self.screen, 25, 80, 0, 0)
        self.canvas.clear = lambda: self.canvas.reset()
        self.instance.screen_manager = ScreenManager.from_frame(
            SelectorView,
            ModeSelectorModel,
            screen=self.canvas,
            application=self.instance
        )

    def _update(self):
        for effect in self.instance.screen_manager.scene.effects:
            effect.update(0)

    def _send_raw(self, code):
        self.instance.screen_manager.scene.process_event(KeyboardEvent(code))

    def send_codes(self, s):
        for c in s:
            self._send_raw(ord(c))
        self._update()

    def send_tab(self, n=1):
        for _ in range(n):
            self._send_raw(Screen.KEY_TAB)
        self._update()

    def send_backspace(self, n=1):
        for _ in range(n):
            self._send_raw(Screen.KEY_BACK)
        self._update()

    def send_enter(self, n=1):
        for _ in range(n):
            self._send_raw("\r")
        self._update()

    def send(self, *sequence):
        new_sequence = []
        for i in sequence:
            if isinstance(i, tuple):
                new_sequence.extend([i[0]] * i[1])
            else:
                new_sequence.append(i)

        for i in new_sequence:
            if isinstance(i, str):
                code = getattr(Screen, "KEY_" + i.upper(), None)
                if code:
                    self._send_raw(code)
                else:
                    self.send_codes(i)
            elif isinstance(i, int):
                self._send_raw(code)
            else:
                raise ValueError(f"Wrong type: {i}")

    def expect(self, s):
        for y in range(self.canvas.height):
            chars = []
            for x in range(self.canvas.width):
                char, _, _, _ = self.canvas.get_from(x, y)
                chars.append(chr(char))
            if s in "".join(chars):
                return x, y

        self.dump_canvas()
        raise ValueError

    def dump_canvas(self):
        good_colors = {"grey", "red", "green", "yellow", "blue", "magenta", "cyan",
                       "white"}

        print("-" * 80)
        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                char, fg, _, bg = self.canvas.get_from(x, y)
                char = chr(char)

                fg = COLORS[fg]
                bg = COLORS[bg]

                args = {}
                if fg in good_colors:
                    args["color"] = fg
                if bg in good_colors:
                    args["on_color"] = f"on_{bg}"
                print(colored(char, **args), end='')
            print("\r")
        print("-" * 80)


@contextmanager
def make_tui_instance():
    instance = IrohaTUITestInstance()
    yield instance
