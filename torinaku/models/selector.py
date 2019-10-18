from torinaku.models.base import BaseModel


class BaseSelectorModel(BaseModel):
    options = {}

    @property
    def screen_options(self):
        return {x: x for x in self.options.keys()}

    def select(self, x):
        self.options[x]()
