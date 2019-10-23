from asciimatics.widgets import Widget, Label, Text, TextBox
from torinaku.tui.checklistbox import CheckListBox, RadioListBox


def get_proto_widget(field_descriptor, prefix, fill_frame) -> Widget:
    switcher = {
        "CPPTYPE_STRING": _build_textline,
        "CPPTYPE_UINT32": _build_uint32,
        "CPPTYPE_ENUM": _build_enum,
    }
    painter_func = switcher.get(field_descriptor["cpp_type"], _build_unknown_field)
    return painter_func(field_descriptor, prefix, fill_frame)


def _build_textline(field_descriptor, prefix, fill_frame):
    if field_descriptor["repeated"]:
        return TextBox(
            height=10,
            name=prefix + field_descriptor["field_path"]
        ), fill_frame
    else:
        return Text(
            name=prefix + field_descriptor["field_path"]
        ), fill_frame


def _build_uint32(field_descriptor, prefix, fill_frame):
    return (
        CoercingText(
            target_type=int,
            name=prefix + field_descriptor["field_path"]
        ),
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
