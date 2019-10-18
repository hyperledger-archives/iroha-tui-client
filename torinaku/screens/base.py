from asciimatics.screen import Screen
from asciimatics.widgets import Frame
from asciimatics.event import KeyboardEvent


class BaseScreen(Frame):
    _title = ""

    def __init__(self, screen, model):
        self._screen = screen
        self._model = model

        super().__init__(**self.get_init_kwargs())

        self._compose_layout()
        self.fix()

    def get_title(self):
        return self._title

    def get_init_kwargs(self):
        return {
            "screen": self._screen,
            "height": self._screen.height,
            "width": self._screen.width,
            "has_border": "True",
            "has_shadow": "True",
            "title": self.get_title(),
            "data": self._model.data,
        }

    def update_data(self):
        self.save()
        self._model.update_data(self.data)
        self.data = self._model.data

    def update(self, frame_no):
        self.update_data()
        super().update(frame_no)

    def _compose_layout(self):
        raise NotImplementedError

    @property
    def is_skippable(self):
        """
        Whether this frame should be skipped when navigating back in frame
        history.
        Used to skip large selection screens (e.g. in command type selector).
        """
        return getattr(self._model, "is_skippable", False)

    def copy_with_screen(self, screen):
        copy = self.__class__(screen=screen, model=self._model)
        return copy

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == Screen.KEY_ESCAPE:
                self._model.cancel()
        super().process_event(event)
