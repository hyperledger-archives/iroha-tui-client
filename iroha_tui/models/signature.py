from iroha_tui.models.base import BaseModel


class SignatureModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.signature = kwargs.pop("signature")
        super().__init__(*args, **kwargs)

    @property
    def data(self):
        return {
            "public_key": self.signature.public_key,
            "signature": self.signature.signature,
        }

    def back(self):
        self._application.screen_manager.back()
