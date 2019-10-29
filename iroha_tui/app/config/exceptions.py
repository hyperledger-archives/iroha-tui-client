class InvalidOptionValue(Exception):
    def __init__(self, option, message):
        self.option = option
        self.message = message

    def __str__(self):
        return f"Invalid option value for option '{self.option.name}': '{self.message}'"
