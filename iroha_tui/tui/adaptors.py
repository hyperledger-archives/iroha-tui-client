# TODO: refactor

from asciimatics.widgets import (
    Frame,
    Layout,
    Divider,
    Text,
    Widget,
    Label,
)

from iroha_tui.tui.checklistbox import CheckListBox, RadioListBox
from iroha_tui.app.validators import uint32_validator
import re


def field_label(field_descriptor):
    path = field_descriptor["field_path"][1:]
    path = path.replace(".", " / ").title().replace("_", " ")
    if field_descriptor["optional_primitive"]:
        path = "[" + path + "]"
    return path


class CommandTuiAdaptor:
    def __init__(self, message_model, frame: Frame, layout=None, layout_column=None):
        self._message_model = message_model
        self._frame = frame
        self._lay = layout
        self._lay_column = layout_column
        self._has_frame_filler = None

    def draw_ui(self):
        self._init_layout()
        descr = self._message_model.descriptor
        if len(descr):
            command_name = re.sub(
                r"([A-Z])", r" \1", self._message_model.descriptor[0]["message_path"]
            ).strip()
            self._lay.add_widget(
                Label("Current Command: {}".format(command_name)), self._lay_column
            )
            self._lay.add_widget(Divider(), self._lay_column)
        has_optional_primitive = False
        for field_descriptor in descr:
            if field_descriptor["optional_primitive"]:
                has_optional_primitive = True
            self._draw_component(field_descriptor)
        if has_optional_primitive:
            self._lay.add_widget(Divider(), self._lay_column)
            self._lay.add_widget(
                Label(
                    '* Fields, which names are enclosed into "[" and "]" are optional'
                ),
                self._lay_column,
            )

    """
    @
    @
    @ Private part
    @
    @
    """

    def _init_layout(self):
        if not self._lay:
            self._lay = Layout([1, 18, 1], fill_frame=True)
            self._lay_column = 1
            self._frame.add_layout(self._lay)

    def _draw_component(self, field_descriptor):
        switcher = {
            "CPPTYPE_STRING": "_draw_textline",
            "CPPTYPE_UINT32": "_draw_uint32",
            "CPPTYPE_ENUM": "_draw_enum",
        }
        painter_name = switcher.get(field_descriptor["cpp_type"], "_draw_unknown_field")
        painter_func = getattr(self, painter_name)
        painter_func(field_descriptor)

    def _draw_unknown_field(self, field_descriptor):
        self._lay.add_widget(
            Label(
                "Unable to display field: {}{} (unsupported type)".format(
                    field_descriptor["message_path"], field_descriptor["field_path"]
                )
            ),
            self._lay_column,
        )

    def _draw_textline(self, field_descriptor):
        self._lay.add_widget(
            Text(
                label=field_label(field_descriptor), name=field_descriptor["field_path"]
            ),
            self._lay_column,
        )

    def _draw_uint32(self, field_descriptor):
        self._lay.add_widget(
            Text(
                label=field_label(field_descriptor),
                name=field_descriptor["field_path"],
                validator=uint32_validator,
            ),
            self._lay_column,
        )

    def _draw_enum(self, field_descriptor):
        if not self._has_frame_filler:
            height = Widget.FILL_FRAME
            self._has_frame_filler = True
        else:
            height = 8
        if field_descriptor["repeated"]:
            # then we use checkboxes
            self._lay.add_widget(
                CheckListBox(
                    height=height,
                    options=field_descriptor["enum_options"],
                    label=field_label(field_descriptor),
                    add_scroll_bar=True,
                    name=field_descriptor["field_path"],
                ),
                self._lay_column,
            )
        else:
            # field is not repeated and we use radio buttons
            self._lay.add_widget(
                RadioListBox(
                    label=field_label(field_descriptor),
                    height=height,
                    options=field_descriptor["enum_options"],
                    add_scroll_bar=True,
                    name=field_descriptor["field_path"],
                ),
                self._lay_column,
            )


# TODO add names to fields, so make them collectable
