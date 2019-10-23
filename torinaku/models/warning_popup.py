from torinaku.models.base import BaseModel


class WarningModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.value = kwargs.pop("value")
        super().__init__(*args, **kwargs)

    def get_init_data(self):
        return {
            "value": self.value
        }
