from asciimatics.widgets import Frame, Layout


class BaseLayoutComposer:
    layout_columns = []

    @classmethod
    def build_layouts(cls):
        return [Layout(x) for x in cls.layout_columns]

    @classmethod
    def compose_on_frame(cls, frame: Frame, *args, **kwargs):
        layouts = cls.build_layouts()
        for layout in layouts:
            frame.add_layout(layout)
        cls.compose_on_layouts(layouts, *args, **kwargs)
