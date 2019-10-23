import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from torinaku.app import Torinaku


class BaseModel(abc.ABC):
    """
    Base model
    """

    is_skippable = False

    def __init__(self, application: "Torinaku"):
        self._application: "Torinaku" = application
        self._data = {}
        self.update_data(self.get_init_data())

    def get_init_data(self):
        return {}

    def update_data(self, frame_data):
        self._data.update(**frame_data)

    @property
    def data(self):
        return self._data

    def go_to(self, frame_cls, model_cls, keep=True, **model_kwargs):
        self._application.screen_manager.to(frame_cls, model_cls, keep,
                                            **model_kwargs)

    def go_back(self):
        self._application.screen_manager.back()

    def cancel(self):
        self.go_back()
