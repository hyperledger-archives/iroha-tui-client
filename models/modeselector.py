from asciimatics.exceptions import StopApplication


class ModeSelector:

  def __init__(self, model):
    self._model = model

  @property
  def captions(self):
    return {
        'window': 'Iroha TUI',
        'proceed': 'Select',
        'cancel': 'Quit'
    }

  @property
  def options(self):
    return [
        ('Transactions Browser', 0),
        ('Queries Browser', 1),
        ('Keys Manager', 2),
    ]

  def proceed(self, option):
    if isinstance(option, int):
      if 0 == option:
        self._model.nextscreen('Transactions Browser')

    self._model.popup(str(option))

  def cancel(self):
    raise StopApplication('exit requested')

  def esc(self):
    self._model.popup(
        'Exitting... Are you sure?',
        ['Yes', 'No'],
        self._quit_on_yes
    )

  @staticmethod
  def _quit_on_yes(selected):
    if selected == 0:
      raise StopApplication('exit requested')
