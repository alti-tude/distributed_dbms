class Attribute:
    def __init__(self, name, python_type, format_function):
        self.name = name
        self.python_type = python_type
        self.format = format_function