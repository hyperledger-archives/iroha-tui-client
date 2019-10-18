import re
from future.moves.itertools import zip_longest

from asciimatics.widgets import _BaseListBox, _enforce_width
from asciimatics.event import KeyboardEvent, MouseEvent


class MultiColumnCheckListBox(_BaseListBox):
    def __init__(
        self,
        height,
        columns,
        options,
        titles=None,
        label=None,
        name=None,
        add_scroll_bar=False,
        on_change=None,
        on_select=None,
    ):
        super(MultiColumnCheckListBox, self).__init__(
            height,
            options,
            titles=titles,
            label=label,
            name=name,
            on_change=on_change,
            on_select=on_select,
        )
        if self._titles:
            self._titles.insert(0, " ")
        columns.insert(0, "<4")
        self._selected = []
        self._columns = []
        self._align = []
        self._spacing = []
        self._add_scroll_bar = add_scroll_bar
        for i, column in enumerate(columns):
            if isinstance(column, int):
                self._columns.append(column)
                self._align.append("<")
            else:
                match = re.match(r"([<>^]?)(\d+)([%]?)", column)
                self._columns.append(
                    float(match.group(2)) / 100
                    if match.group(3)
                    else int(match.group(2))
                )
                self._align.append(match.group(1) if match.group(1) else "<")
            self._spacing.append(
                1
                if i > 0 and self._align[i] == "<" and self._align[i - 1] == ">"
                else 0
            )

    def _internal_select(self):
        if not len(self._options):
            return
        val = self._options[self._line][1]
        if val in self._selected:
            self._selected.remove(val)
        else:
            self._selected.append(val)
        if self._on_change:
            self._on_change()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord(" ")]:
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
                            if event.x < 5:
                                self._internal_select()
                            else:
                                if self._on_select:
                                    self._on_select()
                    return None
                # Check for scroll bar interactions:
                if self._scroll_bar:
                    event = self._scroll_bar.process_event(event)

            # Ignore other mouse events.
            return event
        else:
            return super().process_event(event)

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

    def _find_option(self, search_value):
        return None

    def _get_width(self, width, max_width):
        """
        Helper function to figure out the actual column width from the various options.

        :param width: The size of column requested
        :param max_width: The maximum width allowed for this widget.
        :return: the integer width of the column in characters
        """
        if isinstance(width, float):
            return int(max_width * width)
        if width == 0:
            width = (
                max_width
                - sum(self._spacing)
                - sum([self._get_width(x, max_width) for x in self._columns if x != 0])
            )
        return width

    def update(self, frame_no):
        self._draw_label()
        ellipsis = u"…" if self._frame.canvas.unicode_aware else "..."
        check_char = u"✓" if self._frame.canvas.unicode_aware else "X"
        borders = ("[", "]")

        # Calculate new visible limits if needed.
        height = self._h
        width = self._w
        dy = 0

        # Clear out the existing box content
        (colour, attr, bg) = self._frame.palette["field"]
        for i in range(height):
            self._frame.canvas.print_at(
                " " * width, self._x + self._offset, self._y + i + dy, colour, attr, bg
            )

        # Allow space for titles if needed.
        if self._titles:
            dy += 1
            height -= 1

        # Decide whether we need to show or hide the scroll bar and adjust width
        # accordingly.
        if self._add_scroll_bar:
            self._add_or_remove_scrollbar(width, height, dy)
        if self._scroll_bar:
            width -= 1

        # Now draw the titles if needed.
        if self._titles:
            row_dx = 0
            colour, attr, bg = self._frame.palette["title"]
            for i, [title, align, space] in enumerate(
                zip(self._titles, self._align, self._spacing)
            ):
                cell_width = max(0, self._get_width(self._columns[i], width))
                self._frame.canvas.print_at(
                    "{}{:{}{}}".format(
                        " " * space,
                        _enforce_width(
                            title, cell_width, self._frame.canvas.unicode_aware
                        ),
                        align,
                        cell_width,
                    ),
                    self._x + self._offset + row_dx,
                    self._y,
                    colour,
                    attr,
                    bg,
                )
                row_dx += cell_width + space

        # Don't bother with anything else if there are no options to render.
        if len(self._options) <= 0:
            return

        # Render visible portion of the text.
        self._start_line = max(
            0, max(self._line - height + 1, min(self._start_line, self._line))
        )
        for i, [row, value] in enumerate(self._options):
            if self._start_line <= i < self._start_line + height:
                colour, attr, bg = self._pick_colours("field", i == self._line)
                row_dx = 0
                row = list(row)
                row.insert(0, "")

                # Try to handle badly formatted data, where row lists don't
                # match the expected number of columns.
                first = True
                for text, cell_width, align, space in zip_longest(
                    row, self._columns, self._align, self._spacing, fillvalue=""
                ):
                    if cell_width == "":
                        break
                    cell_width = max(0, self._get_width(cell_width, width))
                    if len(text) > cell_width:
                        text = text[: cell_width - len(ellipsis)] + ellipsis
                    if first:
                        first = False
                        cb_fg, cb_attr, cb_bg = self._pick_colours(
                            "control", i == self._line
                        )
                        self._frame.canvas.print_at(
                            "{}{}{} ".format(
                                borders[0],
                                check_char if value in self._selected else " ",
                                borders[1],
                            ),
                            self._x + self._offset + row_dx,
                            self._y + i + dy - self._start_line,
                            cb_fg,
                            cb_attr,
                            cb_bg,
                        )
                    else:
                        self._frame.canvas.print_at(
                            "{}{:{}{}}".format(
                                " " * space,
                                _enforce_width(
                                    text, cell_width, self._frame.canvas.unicode_aware
                                ),
                                align,
                                cell_width,
                            ),
                            self._x + self._offset + row_dx,
                            self._y + i + dy - self._start_line,
                            colour,
                            attr,
                            bg,
                        )
                    row_dx += cell_width + space

        # And finally draw any scroll bar.
        if self._scroll_bar:
            self._scroll_bar.update()
