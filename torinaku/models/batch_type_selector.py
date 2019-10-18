from torinaku.models.base import BaseModel


class BatchTypeSelectorModel(BaseModel):
    captions = {"proceed": "Proceed", "cancel": "Cancel", "window": "Batch type"}

    options = [("Atomic", True), ("Ordered", False)]

    def __init__(self, *args, **kwargs):
        self.on_type_selected = kwargs.pop("on_type_selected")
        super().__init__(*args, **kwargs)

    def proceed(self, is_atomic: bool):
        self.on_type_selected(is_atomic)
        self.cancel()
