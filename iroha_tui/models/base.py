import abc
from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from iroha_tui.app import IrohaTUI


class BaseModel(abc.ABC):
    """
    Base model
    """

    is_skippable = False

    def __init__(self, application: "IrohaTUI"):
        self._application: "IrohaTUI" = application
        self._data: Dict[str, Any] = {}
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
