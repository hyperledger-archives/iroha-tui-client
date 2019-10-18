from typing import Dict, List
from asciimatics.widgets import Layout, Widget, Label

from torinaku.tui.layout_composers.base import BaseLayoutComposer


class KVLayoutComposer(BaseLayoutComposer):
    layout_columns = [[5, 13]]

    @classmethod
    def compose_on_layouts(cls, layouts: List[Layout], widgets: Dict[str, Widget]):
        layout = layouts[0]
        for name, widget in widgets.items():
            layout.add_widget(Label(name), 0)
            layout.add_widget(widget, 1)
