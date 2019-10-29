from typing import List
from asciimatics.widgets import Widget, Divider, Label, Layout, Text, TextBox
from iroha_tui.proto.message import ProtoMessageProxy
from iroha_tui.tui.checklistbox import RadioListBox, CheckListBox
from iroha_tui.tui.layout_composers.base import BaseLayoutComposer
from iroha_tui.tui.layout_composers.kv import KVLayoutComposer
from iroha_tui.tui.widgets.proto_field import get_proto_widget


def _get_field_label(field_descriptor):
    path = field_descriptor["field_path"][1:]
    path = path.replace(".", " / ").title().replace("_", " ")
    if field_descriptor["optional_primitive"]:
        path = "[" + path + "]"
    return path


class ProtoLayoutComposer(BaseLayoutComposer):
    layout_columns = [*KVLayoutComposer.layout_columns, [1]]

    @classmethod
    def compose_on_layouts(
        cls, layouts: List[Layout], proxy: ProtoMessageProxy, prefix: str
    ):
        fields_layout, notes_layout = layouts

        widgets = {}
        has_optional_primitive = False
        has_multiline = False
        fill_frame = True
        for field_descriptor in proxy.descriptor:
            if field_descriptor["optional_primitive"]:
                has_optional_primitive = True
            if (
                field_descriptor["repeated"] and
                field_descriptor["cpp_type"] == "CPPTYPE_STRING"
            ):
                has_multiline = True
            widget, fill_frame = get_proto_widget(
                field_descriptor, prefix, fill_frame
            )
            widgets[_get_field_label(field_descriptor)] = widget
        KVLayoutComposer.compose_on_layouts([fields_layout], widgets)

        if has_optional_primitive or has_multiline:
            notes_layout.add_widget(Divider())
        if has_optional_primitive:
            notes_layout.add_widget(
                Label(
                    "* Fields, whose names are enclosed into '[' and ']' are "
                    "optional"
                )
            )
        if has_multiline:
            notes_layout.add_widget(
                Label(
                    "* Multiline inputs are repeated fields which are used "
                    "line-by-line"
                )
            )
