from loguru import logger
from torinaku.models.base import BaseModel


class SignaturePickerModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.on_private_key_entered = kwargs.pop("on_private_key_entered")
        super().__init__(*args, **kwargs)

    def sign(self, private_key):
        try:
            self.on_private_key_entered(private_key)
            self.cancel()
        except Exception as e:
            logger.debug(e)
            pass
