from torinaku.models.base import BaseModel


class PeerPickerModel(BaseModel):
    is_skippable = True

    def __init__(self, *args, **kwargs):
        self.on_peer_chosen = kwargs.pop("on_peer_chosen")
        super().__init__(*args, **kwargs)

    def get_init_data(self):
        if self._application.last_chosen_peer:
            return {"address": self._application.last_chosen_peer}
        else:
            return {}

    def choose(self, address):
        self._application.last_chosen_peer = address
        self.on_peer_chosen(address)
