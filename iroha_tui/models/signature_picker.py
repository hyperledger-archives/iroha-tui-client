from loguru import logger
from iroha_tui.models.base import BaseModel
from iroha_tui.tui.catch import catch


class SignaturePickerModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.on_private_key_entered = kwargs.pop("on_private_key_entered")
        super().__init__(*args, **kwargs)

    @catch()
    def on_file_selected(self):
        path = self.data["file_picker"]
        with open(path, "rb") as f:
            data = f.read()
        self.sign(data)

    @catch()
    def sign(self, private_key):
        self.on_private_key_entered(private_key)
        self.cancel()
