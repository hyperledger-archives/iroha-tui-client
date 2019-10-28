import sys

from asciimatics.screen import Screen, ResizeScreenError

from torinaku.app.screen_manager import ScreenManager
from torinaku.app.persistence import Persistence
from torinaku.models.mode_selector import ModeSelectorModel
from torinaku.screens.selector import SelectorView


class Torinaku:
    """
    Main application class
    """

    def __init__(self, config):
        self.screen_manager: ScreenManager = None

        self.config = config
        self.transactions = []
        self.queries = []
        self.last_chosen_peer = None

        self.persistence = None
        if config.get("persistence_file_path"):
            self.persistence = Persistence(config["persistence_file_path"])
            self.persistence.load(self)

        self.query_counter = 1

    def run(self):
        last_scene = None
        while True:
            try:
                Screen.wrapper(
                    self._run_with_screen, catch_interrupt=False, arguments=[last_scene]
                )
                if self.persistence:
                    self.persistence.dump(self)
                sys.exit(0)
            except ResizeScreenError as e:
                last_scene = e.scene
            except KeyboardInterrupt:
                if self.persistence:
                    self.persistence.dump(self)
                sys.exit(0)

    def _run_with_screen(self, screen, scene):
        if self.screen_manager is None:
            self.screen_manager = ScreenManager.from_frame(
                SelectorView, ModeSelectorModel, screen=screen, application=self
            )
        else:
            self.screen_manager = self.screen_manager.copy_with_screen(screen)
        screen.play([self.screen_manager.scene], stop_on_resize=True, allow_int=True)
