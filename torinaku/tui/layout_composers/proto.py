from typing import List
from asciimatics.widgets import Widget, Divider, Label, Layout, Text
from torinaku.proto.message import ProtoMessageProxy
from torinaku.tui.checklistbox import RadioListBox, CheckListBox
from torinaku.tui.layout_composers.base import BaseLayoutComposer
from torinaku.tui.layout_composers.kv import KVLayoutComposer
from torinaku.app.validators import uint32_validator


def _get_field_label(field_descriptor):
    path = field_descriptor["field_path"][1:]
    path = path.replace(".", " / ").title().replace("_", " ")
    if field_descriptor["optional_primitive"]:
        path = "[" + path + "]"
    return path


def _build_textline(field_descriptor, prefix, fill_frame):
    return Text(name=prefix + field_descriptor["field_path"]), fill_frame


def _build_uint32(field_descriptor, prefix, fill_frame):
    return (
        Text(name=prefix + field_descriptor["field_path"], validator=uint32_validator),
        fill_frame,
    )


def _build_enum(field_descriptor, prefix, fill_frame):
    height = Widget.FILL_FRAME if fill_frame else 8
    if field_descriptor["repeated"]:
        return (
            CheckListBox(
                height=height,
                options=field_descriptor["enum_options"],
                add_scroll_bar=True,
                name="prefix" + field_descriptor["field_path"],
            ),
            False,
        )
    else:
        return (
            RadioListBox(
                height=height,
                options=field_descriptor["enum_options"],
                add_scroll_bar=True,
                name="prefix" + field_descriptor["field_path"],
            ),
            False,
        )


def _build_unknown_field(field_descriptor, prefix, fill_frame):
    return (
        Label(
            "Unable to display field: {}{} (unsupported type)".format(
                field_descriptor["message_path"], field_descriptor["field_path"]
            )
        ),
        fill_frame,
    )


def _build_widget_for_component(field_descriptor, prefix, fill_frame) -> Widget:
    switcher = {
        "CPPTYPE_STRING": _build_textline,
        "CPPTYPE_UINT32": _build_uint32,
        "CPPTYPE_ENUM": _build_enum,
    }
    painter_func = switcher.get(field_descriptor["cpp_type"], _build_unknown_field)
    return painter_func(field_descriptor, prefix, fill_frame)


class ProtoLayoutComposer(BaseLayoutComposer):
    layout_columns = [*KVLayoutComposer.layout_columns, [1]]

    @classmethod
    def compose_on_layouts(
        cls, layouts: List[Layout], proxy: ProtoMessageProxy, prefix: str
    ):
        fields_layout, notes_layout = layouts

        widgets = {}
        has_optional_primitive = False
        fill_frame = True
        for field_descriptor in proxy.descriptor:
            if field_descriptor["optional_primitive"]:
                has_optional_primitive = True
            widget, fill_frame = _build_widget_for_component(
                field_descriptor, prefix, fill_frame
            )
            widgets[_get_field_label(field_descriptor)] = widget
        KVLayoutComposer.compose_on_layouts([fields_layout], widgets)

        if has_optional_primitive:
            notes_layout.add_widget(Divider())
            notes_layout.add_widget(
                Label(
                    "* Fields, whose names are enclosed into '[' and ']' are "
                    "optional"
                )
            )
