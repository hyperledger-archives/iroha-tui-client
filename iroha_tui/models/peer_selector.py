from iroha_tui.models.base import BaseModel


_ADD_NEW_PEER = "Enter peer details manually ..."


class PeerSelectorModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.on_peer_chosen = kwargs.pop("on_peer_chosen")
        super().__init__(*args, **kwargs)

    @property
    def options(self):
        return [(x, x) for x in self._application.peers] + [_ADD_NEW_PEER]

    def proceed(self, address: str) -> None:
        if address == _ADD_NEW_PEER:
            # TODO: implement
            raise NotImplementedError
        else:
            self.on_peer_chosen(address)
