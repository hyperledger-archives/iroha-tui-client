from asciimatics.widgets import _BaseListBox, _enforce_width
from asciimatics.event import KeyboardEvent, MouseEvent


class CheckListBox(_BaseListBox):
    r"""
    A MultiListBox is a widget that displays a list from which the user can select
    multiple options.
    """

    def __init__(
        self,
        height,
        options,
        centre=False,
        label=None,
        name=None,
        add_scroll_bar=False,
        on_change=None,
        on_select=None,
        validator=None,
        type="check",
    ):
        super(CheckListBox, self).__init__(
            height,
            options,
            label=label,
            name=name,
            on_change=on_change,
            on_select=on_select,
            validator=validator,
        )
        self._centre = centre
        self._add_scroll_bar = add_scroll_bar
        self._selected = []
        self._type = type
        if self._type not in ["check", "radio"]:
            raise Exception('CheckListBox must be typed as "check" or "radio"')

    @property
    def value(self):
        return (self._value, self._selected)

    @value.setter
    def value(self, new_value):
        if isinstance(new_value, tuple):
            self._selected = new_value[1]
            new_value = new_value[0]

        # Only trigger change notification after we've changed selection
        old_value = self._value
        self._value = new_value
        for i, [_, value] in enumerate(self._options):
            if value == new_value:
                self._line = i
                break
        else:
            # No matching value - pick a default.
            if len(self._options) > 0:
                self._line = 0
                self._value = self._options[self._line][1]
            else:
                self._line = -1
                self._value = None
        if self._validator:
            self._is_valid = self._validator(self._value)
        if old_value != self._value and self._on_change:
            self._on_change()

        # Fix up the start line now that we've explicitly set a new value.
        self._start_line = max(
            0, max(self._line - self._h + 1, min(self._start_line, self._line))
        )

    def _internal_select(self):
        val = self._options[self._line][1]
        if self._type == "check":
            if val in self._selected:
                self._selected.remove(val)
            else:
                self._selected.append(val)
        elif self._type == "radio":
            self._selected = [val]
        if self._on_select:
            self._on_select()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord(" "), 10, 13]:
                self._internal_select()
            else:
                return super().process_event(event)
        elif isinstance(event, MouseEvent):
            # Mouse event - adjust for scroll bar as needed.
            if event.buttons != 0:
                # Check for normal widget.
                if len(self._options) > 0 and self.is_mouse_over(
                    event,
                    include_label=False,
                    width_modifier=1 if self._scroll_bar else 0,
                ):
                    # Figure out selected line
                    new_line = event.y - self._y + self._start_line
                    if self._titles:
                        new_line -= 1
                    new_line = min(new_line, len(self._options) - 1)

                    # Update selection and fire select callback if needed.
                    if new_line >= 0:
                        self._line = new_line
                        self.value = self._options[self._line][1]
                        if event.buttons & MouseEvent.DOUBLE_CLICK != 0:
                            self._internal_select()
                    return None
                # Check for scroll bar interactions:
                if self._scroll_bar:
                    event = self._scroll_bar.process_event(event)

            # Ignore other mouse events.
            return event
        else:
            return super().process_event(event)

    def update(self, frame_no):
        self._draw_label()

        # Prepare to calculate new visible limits
        height = self._h
        width = self._w

        # Clear out the existing box content
        (fg, attr, bg) = self._frame.palette["field"]
        for i in range(height):
            self._frame.canvas.print_at(
                " " * self.width, self._x + self._offset, self._y + i, fg, attr, bg
            )

        if 0 == len(self._options):
            return

        if self._add_scroll_bar:
            self._add_or_remove_scrollbar(width, height, 0)
        if self._scroll_bar:
            width -= 1
        if self._type == "radio":
            check_char = u"•" if self._frame.canvas.unicode_aware else "X"
            borders = ("(", ")")
        else:
            check_char = u"✓" if self._frame.canvas.unicode_aware else "X"
            borders = ("[", "]")
        ellipsis = u"…" if self._frame.canvas.unicode_aware else "..."

        # Render visible portion of the text
        y_offset = 0
        if self._centre:
            self._start_line = self._line - (height // 2)
        start_line = self._start_line
        if self._start_line < 0:
            y_offset = -self._start_line
            start_line = 0
        for i, (text, value) in enumerate(self._options):
            if start_line <= i < start_line + height - y_offset:
                fg, attr, bg = self._pick_colours("control", i == self._line)
                self._frame.canvas.print_at(
                    "{}{}{} ".format(
                        borders[0],
                        check_char if value in self._selected else " ",
                        borders[1],
                    ),
                    self._x + self._offset,
                    self._y + y_offset + i - start_line,
                    fg,
                    attr,
                    bg,
                )
                fg, attr, bg = self._pick_colours("field", i == self._line)
                if len(text) > width - 4:
                    text = text[: width - 4 - len(ellipsis)] + ellipsis
                self._frame.canvas.print_at(
                    "{:{}}".format(
                        _enforce_width(
                            text,
                            width - 4 - self._offset,
                            self._frame.canvas.unicode_aware,
                        ),
                        width - 4 - self._offset,
                    ),
                    self._x + self._offset + 4,
                    self._y + y_offset + i - start_line,
                    fg,
                    attr,
                    bg,
                )

        if self._scroll_bar:
            self._scroll_bar.update()

    def _find_option(self, search_value):
        for text, value in self._options:
            if search_value in text:
                return value
        return None


def RadioListBox(*args, **kwargs):
    r"""
   __        __     __             __  ___     __   __
  |__)  /\  |  \ | /  \    |    | /__`  |     |__) /  \ \_/
  |  \ /~~\ |__/ | \__/    |___ | .__/  |     |__) \__/ / \

  """
    return CheckListBox(*args, **kwargs, type="radio")
