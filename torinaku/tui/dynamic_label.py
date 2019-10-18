from asciimatics.widgets import Label


class DynamicLabel(Label):
    def __init__(self, name, clip=True):
        super().__init__(label="")
        self._name = name
        self._clip = clip

    def update(self, frame_no):
        self._text = self._frame.data[self._name]

        if self._clip and len(self._text) > self._w:
            self._text = self._text[: self._w - 3] + "..."

        super().update(frame_no)

    @property
    def value(self):
        return self._text

    @value.setter
    def value(self, new_value):
        self._text = new_value
