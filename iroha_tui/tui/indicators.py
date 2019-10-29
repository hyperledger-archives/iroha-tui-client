from asciimatics.widgets import Label


class Indicators:
    """
    Allows to create and handle dynamic labels

    The values might me read from indicators_data
    property as a dictionary.

    Assigning a dictionary to
    indicators_data will cause an updated of existing
    labels which keys were matched with passed dictionary keys.

    The reason to create the class is: use asciimatics.widgets.Label
    as a dynamic read-only fields. The interface allows to read and
    set values the same way as for asciimatics.widgets.Frame.
    """

    def init_indicators(self):
        self._indicators = {}
        self._indicators_data = {}

    def Indicator(self, name, label="", *args, **kwargs):
        indicator = Label(label, *args, **kwargs)
        self._indicators[name] = indicator
        return indicator

    @property
    def indicators_data(self):
        result = {}
        for name, label in self._indicators.items():
            result[name] = label.text
        return result

    @indicators_data.setter
    def indicators_data(self, value):
        for name, text in value.items():
            if name in self._indicators:
                self._indicators[name].text = text
